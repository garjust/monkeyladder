from django.contrib.auth.forms import forms, _

from core.logic import get_ladder_or_404
from leaderboard.logic import get_ladder_player_dictionary
from leaderboard.models import Match

class MatchCreationForm(forms.Form):
    """
    A form that creates a match without game information
    """
    error_messages = {
        'invalid_scores': _("Scores must be positive integers"),
        'invalid_player': _("Players must be on the ladder"),
    }

    ladder_id = forms.IntegerField(label=_("Ladder Id"), widget=forms.HiddenInput, min_value=1)
    player_one = forms.CharField(label=_("Player One"), max_length=30)
    player_two = forms.CharField(label=_("Player Two"), max_length=30)
    player_one_score = forms.IntegerField(label=_("Score"), min_value=0)
    player_two_score = forms.IntegerField(label=_("Score"), min_value=0)

    def clean_ladder_id(self):
        return self.cleaned_data['ladder_id']

    def clean_player_one(self):
        ladder = get_ladder_or_404(pk=self.cleaned_data['ladder_id'])
        player_one = self.cleaned_data['player_one']
        player_dictionary = get_ladder_player_dictionary(ladder)
        for player in player_dictionary:
            if player_one == player:
                self.cleaned_data['player_one'] = player_dictionary[player]
                return player_dictionary[player]
        raise forms.ValidationError(self.error_messages['invalid_player'])

    def clean_player_two(self):
        ladder = get_ladder_or_404(pk=self.cleaned_data['ladder_id'])
        player_two = self.cleaned_data['player_two']
        player_dictionary = get_ladder_player_dictionary(ladder)
        for player in player_dictionary:
            if player_two == player:
                self.cleaned_data['player_two'] = player_dictionary[player]
                return player_dictionary[player]
        raise forms.ValidationError(self.error_messages['invalid_player'])

    def save(self, commit=False):
        if self.cleaned_data['player_one_score'] >= self.cleaned_data['player_two_score']:
            winner = 'player_one'
            loser = 'player_two'
        else:
            winner = 'player_two'
            loser = 'player_one'
        ranking_change = not self.cleaned_data['player_one_score'] == self.cleaned_data['player_two_score']
        match = Match(ladder=get_ladder_or_404(pk=self.cleaned_data['ladder_id']), ranking_change=ranking_change,
            winner=self.cleaned_data[winner], winner_score=self.cleaned_data['{}_score'.format(winner)],
            loser=self.cleaned_data[loser], loser_score=self.cleaned_data['{}_score'.format(loser)]
        )
        match.save()
        return match

class GamesCreationForm(forms.Form):
    """
    A form that creates the games for a match
    """
    error_messages = {
        'invalid_scores': _("Scores must be positive integers"),
        'invalid_score_sum': _("Scores for games must make sense")
    }
    
    def __init__(self, match, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)
        self._match = match
        self._number_of_games = match.winner_score + match.loser_score
        for i in range(self._number_of_games):
            setattr(self, 'game_{}_player_one_score'.format(i), forms.IntegerField(min_value=0))
            setattr(self, 'game_{}_player_two_score'.format(i), forms.IntegerField(min_value=0))

    def save(self, commit=False):
        print "SAVING GAMES"