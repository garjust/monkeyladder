from django.contrib.auth.forms import forms, _

from django.contrib.auth.models import User
from core.logic import get_ladder_or_404
from core.models import Ladder, Watcher
from leaderboard.logic import get_ladder_player_dictionary
from leaderboard.models import Match
from django.shortcuts import get_object_or_404

class LadderCreationForm(forms.Form):
    """
    A form that creates a ladder and a ladder admin
    """
    error_messages = {
        'too_many_rungs': _("Ladder can have a maximum 100 rungs"),
        'invalid_user': _("User does not exist"),
    }

    user_id = forms.IntegerField(label=_("User Id"), widget=forms.HiddenInput, min_value=1)
    name = forms.CharField(label=_("Ladder Name"))
    rungs = forms.IntegerField(label=_("Rungs"), min_value=1)
    is_private = forms.BooleanField(label=_("Private"))
    type = forms.Select(label=_("Type"), choices=Ladder.TYPES)

    def clean_user_id(self):
        user = User.objects.get(pk=self.cleaned_data['user_id'])
        if not user:
            raise forms.ValidationError(self.error_messages['invalid_user'])
        return user

    def clean_rungs(self):
        if self.cleaned_data['rungs'] > 100:
            raise forms.ValidationError(self.error_messages['too_many_rungs'])

    def save(self, commit=False):
        ladder = Ladder(name=self.cleaned_data['name'],
            rungs=self.cleaned_data['rungs'],
            is_private=self.cleaned_data['is_private'],
            type=self.cleaned_data['type']
        )
        ladder.save()
        ladder_admin = Watcher(ladder=ladder, user=self.cleaned_data['user_id'])
        ladder_admin.save()
        return ladder, ladder_admin

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
