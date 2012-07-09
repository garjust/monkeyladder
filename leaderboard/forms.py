from django.contrib.auth.forms import forms, _

from core.logic import get_ladder_or_404
from leaderboard.logic import get_ladder_player_dictionary
from leaderboard.models import Match

class SimpleMatchCreationForm(forms.Form):
    """
    A form that creates a match without game information
    """
    error_messages = {
        'invalid_scores': _("Scores must be positive integers"),
        'invalid_player': _("Players must be on the ladder"),
    }
        
    player_one = forms.CharField(label=_("Player One"), max_length=30)
    player_two = forms.CharField(label=_("Player Two"), max_length=30)
    player_one_score = forms.IntegerField(label=_("Score"))
    player_two_score = forms.IntegerField(label=_("Score"))
    ladder_id = forms.IntegerField(label=_("Hidden ladder id field"))
    
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
        ladder = get_ladder_or_404(pk=self.ladder_id)
        player_two = self.cleaned_data['player_two']
        player_dictionary = get_ladder_player_dictionary(ladder)
        for player in player_dictionary:
            if player_two == player:
                self.cleaned_data['player_two'] = player_dictionary[player]
                return player_dictionary[player]
        raise forms.ValidationError(self.error_messages['invalid_player'])
    
    def clean_player_one_score(self):
        score = self.cleaned_data['player_one_score']
        if score < 0:
            raise forms.ValidationError(self.error_messages['invalid_scores'])
        return score
    
    def clean_player_two_score(self):
        score = self.cleaned_data['player_two_score']
        if score < 0:
            raise forms.ValidationError(self.error_messages['invalid_scores'])
        return score

    def save(self, ladder):
        if self.cleaned_data['player_one_score'] >= self.cleaned_data['player_two_score']:
            winner = 'one'
            loser = 'two'
        else:
            winner = 'two'
            loser = 'one'
        match = Match(ladder=ladder, 
            winner=self.cleaned_data[winner], winner_score=self.cleaned_data['{}_score'].format(winner),
            loser=self.cleaned_data[loser], loser_score=self.cleaned_data['{}_score'].format(loser)
        ).save()   
        return match