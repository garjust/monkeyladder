from django.contrib.auth.forms import forms, _

from leaderboard.models import Match, MatchPlayer

class MatchCreationForm(forms.Form):
    """
    A form that creates a match
    """
    error_messages = {
        'invalid_scores': _("Scores must be positive integers"),
        'password_mismatch': _("The two password fields didn't match."),
    }
        
    player_one = forms.CharField(label=_("Player One"), max_length=30)
    player_two = forms.CharField(label=_("Player TWo"), max_length=30)
    player_one_score = forms.IntegerField(label=_("Score"))
    player_two_score = forms.IntegerField(label=_("Score"))
    
    def clean_player_one(self):
        player_one = self.cleaned_data['player_one']
    
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
        match = Match(ladder=ladder).save()
        MatchPlayer(match=match, user=self.cleaned_data['player_one'], score=self.cleaned_data['player_one_score']).save()
        MatchPlayer(match=match, user=self.cleaned_data['player_two'], score=self.cleaned_data['player_two_score']).save()        
        return match
'''
    def _validate_players(self, user, player_names, *players):
        logger.debug("Validating players: {}".format(players))
        if get_best_name(user) not in players:
            raise AssertionError("Cannot create match on the behalf of other players")
        for player in players:
            if players.count(player) != 1:
                logger.error("Match has the same player more than once")
                raise AssertionError("Players must be unique")
            if player not in player_names:
                logger.error("A player was not on the ladder")
                raise AssertionError("Players must be on the ladder")
    
    def _get_player_names(self, ladder):
        player_names = {}
        for player in ladder.ranking():
            player_names[player.name()] = player.user
        return player_names
'''