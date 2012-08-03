from django.contrib.auth.forms import forms, _

from core.logic import int_or_404
from core.forms import LadderConfigurationForm
from core.models import LadderConfiguration, LadderConfigurationKey
from leaderboard.logic import get_ladder_players
from leaderboard.models import Match, Game

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
        player_one = self.cleaned_data['player_one']
        player_dictionary = get_ladder_players(self.ladder)
        for player in player_dictionary:
            if player_one == player:
                self.cleaned_data['player_one'] = player_dictionary[player]
                return player_dictionary[player]
        raise forms.ValidationError(self.error_messages['invalid_player'])

    def clean_player_two(self):
        player_two = self.cleaned_data['player_two']
        player_dictionary = get_ladder_players(self.ladder)
        for player in player_dictionary:
            if player_two == player:
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
        if self.cleaned_data['player_one_score'] >= self.cleaned_data['player_two_score']:
            winner = 'player_one'
            loser = 'player_two'
        else:
            winner = 'player_two'
            loser = 'player_one'
        ranking_change = not self.cleaned_data['player_one_score'] == self.cleaned_data['player_two_score']
        match = Match(ladder=self.ladder, ranking_change=ranking_change,
            winner=self.cleaned_data[winner], winner_score=self.cleaned_data['{}_score'.format(winner)],
            loser=self.cleaned_data[loser], loser_score=self.cleaned_data['{}_score'.format(loser)]
        )
        match.save()
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
        print "SAVING GAMES"
        game_scores = self.games(values=True)
        player_one_games, player_two_games = self.calculate_match_scores(game_scores)
        if player_one_games >= player_two_games:
            winner = 'player_one'
            loser = 'player_two'
            winner_score = player_one_games
            loser_score = player_two_games
        else:
            winner = 'player_two'
            loser = 'player_one'
            winner_score = player_two_games
            loser_score = player_one_games
        ranking_change = not player_one_games == player_two_games
        match = Match(ladder=self.ladder, ranking_change=ranking_change,
            winner=self.cleaned_data[winner], winner_score=winner_score,
            loser=self.cleaned_data[loser], loser_score=loser_score
        )
        match.save()
        print "MATCH CREATED"
        i = 1
        for game_score in game_scores:
            if winner == 'player_one':
                winner_score = game_score[0]
                loser_score = game_score[1]
            else:
                winner_score = game_score[1]
                loser_score = game_score[0]
            game = Game(match=match, game_number=i,
               winner_score=winner_score, loser_score=loser_score
            )
            game.save()
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
