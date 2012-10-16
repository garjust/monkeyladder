from django.contrib.auth.forms import forms, _
from django.contrib.auth.models import User

from core.logic.util import int_or_404, get_lowest_rank
from core.forms import LadderConfigurationForm, LadderRankingEditForm
from core.models import LadderConfiguration, LadderConfigurationKey
from leaderboard.logic.rankings import get_ladder_players, get_ladder_watchers_not_playing
from leaderboard.models import Match, Game, MatchPlayer, GamePlayer, Player

def get_match_form(ladder, post_dictionary=None, number_of_games=None):
    arguments = {'ladder': ladder}
    form_class = MatchCreationForm
    if number_of_games:
        arguments['number_of_games'] = number_of_games
        form_class = GameCreationForm
    if post_dictionary:
        return form_class(post_dictionary, **arguments)
    return form_class(**arguments)

class BaseMatchCreationForm(forms.Form):
    error_messages = {
        'invalid_player': _("Players must be on the ladder"),
        'same_players': _("Players must be different"),
    }

    def __init__(self, *args, **kwargs):
        self.ladder = kwargs.pop('ladder')
        forms.Form.__init__(self, *args, **kwargs)

    player_one = forms.CharField(label=_("Player One"), max_length=30, widget=forms.TextInput(attrs={'class': 'player-name-autocomplete'}))
    player_two = forms.CharField(label=_("Player Two"), max_length=30, widget=forms.TextInput(attrs={'class': 'player-name-autocomplete'}))

    def clean_player_one(self):
        player_dictionary = get_ladder_players(self.ladder)
        for player in player_dictionary:
            if self.cleaned_data['player_one'] == player:
                self.cleaned_data['player_one'] = player_dictionary[player]
                return player_dictionary[player]
        raise forms.ValidationError(self.error_messages['invalid_player'])

    def clean_player_two(self):
        player_dictionary = get_ladder_players(self.ladder)
        for player in player_dictionary:
            if self.cleaned_data['player_two'] == player:
                self.cleaned_data['player_two'] = player_dictionary[player]
                return player_dictionary[player]
        raise forms.ValidationError(self.error_messages['invalid_player'])

    def clean(self):
        if 'player_one' in self.cleaned_data and 'player_two' in self.cleaned_data:
            if self.cleaned_data['player_one'] == self.cleaned_data['player_two']:
                raise forms.ValidationError(self.error_messages['same_players'])
        return self.cleaned_data

class MatchCreationForm(BaseMatchCreationForm):
    """
    A form that creates a match without game information
    """

    player_one_score = forms.IntegerField(label=_("Score"), min_value=0, widget=forms.TextInput(attrs={'class': 'input-mini'}))
    player_two_score = forms.IntegerField(label=_("Score"), min_value=0, widget=forms.TextInput(attrs={'class': 'input-mini'}))

    def save(self):
        ranking_change = not self.cleaned_data['player_one_score'] == self.cleaned_data['player_two_score']
        match = Match.objects.create(ladder=self.ladder, ranking_change=ranking_change)
        MatchPlayer.objects.create(match=match, user=self.cleaned_data['player_one'], score=self.cleaned_data['player_one_score'])
        MatchPlayer.objects.create(match=match, user=self.cleaned_data['player_two'], score=self.cleaned_data['player_two_score'])
        return match

class GameCreationForm(BaseMatchCreationForm):
    """
    A form that creates the a match with games
    """

    def __init__(self, *args, **kwargs):
        self.number_of_games = int_or_404(kwargs.pop('number_of_games'))
        BaseMatchCreationForm.__init__(self, *args, **kwargs)
        for i in range(self.number_of_games):
            self.fields['game_{}_player_one_score'.format(i)] = forms.IntegerField(label=_("Game {} Player One Score".format(i)), min_value=0, widget=forms.TextInput(attrs={'class': 'input-mini'}))
            self.fields['game_{}_player_two_score'.format(i)] = forms.IntegerField(label=_("Game {} Player Two Score".format(i)), min_value=0, widget=forms.TextInput(attrs={'class': 'input-mini'}))

    def games(self, values=False):
        games = []
        for i in range(self.number_of_games):
            if values:
                games.append((self.cleaned_data['game_{}_player_one_score'.format(i)], self.cleaned_data['game_{}_player_two_score'.format(i)]))
            else:
                games.append((self['game_{}_player_one_score'.format(i)], self['game_{}_player_two_score'.format(i)]))
        return games

    def calculate_match_scores(self, game_scores):
        player_one_games = 0
        player_two_games = 0
        for game_score in game_scores:
            if game_score[0] >= game_score[1]:
                player_one_games += 1
            else:
                player_two_games += 1
        return player_one_games, player_two_games

    def save(self):
        game_scores = self.games(values=True)
        player_one_games, player_two_games = self.calculate_match_scores(game_scores)
        ranking_change = not player_one_games == player_two_games
        match = Match.objects.create(ladder=self.ladder, ranking_change=ranking_change)
        player_one = MatchPlayer.objects.create(match=match, user=self.cleaned_data['player_one'], score=player_one_games)
        player_two = MatchPlayer.objects.create(match=match, user=self.cleaned_data['player_two'], score=player_two_games)
        i = 1
        for player_one_score, player_two_score in game_scores:
            game = Game.objects.create(match=match, game_number=i)
            GamePlayer.objects.create(game=game, player=player_one, score=player_one_score)
            GamePlayer.objects.create(game=game, player=player_two, score=player_two_score)
            i += 1
        return match

class LeaderboardConfigurationForm(LadderConfigurationForm):

    def __init__(self, ladder, *args, **kwargs):
        LadderConfigurationForm.__init__(self, ladder, *args, **kwargs)
        self.ladder = ladder
        for key in ['swap_range', 'advancement_distance', 'auto_take_first']:
            config_key = LadderConfigurationKey.objects.get(key='leaderboard.%s' % key)
            try:
                self.fields[key].initial = LadderConfiguration.objects.get(ladder=self.ladder, key=config_key).value()
            except LadderConfiguration.DoesNotExist:
                self.fields[key].initial = LadderConfiguration.objects.get(ladder=None, key=config_key).value()

    swap_range = forms.IntegerField(label=_("Swap Range"), min_value=0, widget=forms.TextInput(attrs={'class': 'input-mini'}))
    advancement_distance = forms.IntegerField(label=_("Advance Distance"), min_value=1, widget=forms.TextInput(attrs={'class': 'input-mini'}))
    auto_take_first = forms.BooleanField(label=_("Automatically Take First"))

    def clean_auto_take_first(self):
        return int(self.cleaned_data['auto_take_first'])

    def save(self):
        super(LeaderboardConfigurationForm, self).save()
        for key in ['swap_range', 'advancement_distance', 'auto_take_first']:
            config_key = LadderConfigurationKey.objects.get(key='leaderboard.%s' % key)
            try:
                config = LadderConfiguration.objects.get(ladder=self.ladder, key=config_key)
                config.raw_value = self.cleaned_data[key]
            except LadderConfiguration.DoesNotExist:
                config = LadderConfiguration(ladder=self.ladder, key=config_key, raw_value=self.cleaned_data[key])
            config.save()

class LadderRankingAndPlayerEditForm(LadderRankingEditForm):

    def __init__(self, ladder, *args, **kwargs):
        LadderRankingEditForm.__init__(self, ladder, *args, **kwargs)
        self.fields['new_player'] = forms.ChoiceField(label=_("New Player"), choices=(('0', 'None'),) + get_ladder_watchers_not_playing(ladder), required=False, widget=forms.Select)
        for i, ranking in enumerate(self.ranking):
            self.fields['rank_%s_remove' % i] = forms.BooleanField(required=False)
            ranking['remove_field'] = self['rank_%s_remove' % i]

    def clean_new_player(self):
        return int(self.cleaned_data['new_player'])

    def clean(self):
        return self.cleaned_data

    def save(self):
        super(LadderRankingAndPlayerEditForm, self).save()
        for i, ranked in enumerate(self.ranking):
            if self.cleaned_data['rank_%s_remove' % i]:
                print "REMOVE A RANKED OBJECT WITH ID = %s" % ranked['ranked']
                ranked['ranked'].delete()
        if self.cleaned_data['new_player'] and self.cleaned_data['new_player'] != 0:
            print "ADDING PLAYER WITH ID=%s" % self.cleaned_data['new_player']
            Player.objects.create(ladder=self.ladder, rank=get_lowest_rank(self.ladder) + 1, user=User.objects.get(pk=self.cleaned_data['new_player']))

