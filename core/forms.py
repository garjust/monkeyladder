from django.contrib.auth.forms import forms, _
from django.contrib.auth.models import User

from core.models import Ladder, Watcher

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
    is_private = forms.BooleanField(label=_("Private"), required=False)
    type = forms.ChoiceField(label=_("Type"), choices=Ladder.TYPES, widget=forms.Select)

    def clean_user_id(self):
        user = User.objects.get(pk=self.cleaned_data['user_id'])
        if not user:
            raise forms.ValidationError(self.error_messages['invalid_user'])
        return user

    def clean_rungs(self):
        if self.cleaned_data['rungs'] > 100:
            raise forms.ValidationError(self.error_messages['too_many_rungs'])
        return self.cleaned_data['rungs']

    def save(self):
        ladder = Ladder(
            name=self.cleaned_data['name'],
            rungs=self.cleaned_data['rungs'],
            is_private=self.cleaned_data['is_private'],
            type=self.cleaned_data['type']
        )
        ladder.save()
        watcher = Watcher(ladder=ladder, user=self.cleaned_data['user_id'], type='ADMIN')
        watcher.save()
        return ladder

class LadderEditForm(forms.Form):
    """
    A form that edits an existing ladder
    """
    error_messages = {
        'invalid_ranks': _("Ranks be unique and consistent")
    }

    def __init__(self, ladder, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)
        self.fields['name'] = forms.CharField(initial=ladder.name, required=False)
        self.fields['rungs'] = forms.IntegerField(initial=ladder.rungs, min_value=1, required=False)
        self.fields['is_private'] = forms.BooleanField(initial=ladder.is_private, required=False)
        ladder_ranking = ladder.ranking()
        self.ranking = []
        for i, ranked in enumerate(ladder_ranking):
            self.fields['rank_{}'.format(i)] = forms.IntegerField(initial=ranked.rank, min_value=1, widget=forms.TextInput(attrs={'class': 'input-mini'}))
            self.ranking.append({'ranked': ranked, 'field': self['rank_{}'.format(i)]})

    def ranked(self, values=False):
        if values:
            return map(lambda r: self.cleaned_data['rank_{}'.format(r['ranked'].rank)], self.ranking)
        return self.ranking

    def clean(self):
        return self.cleaned_data

    def save(self, ladder):
        ladder.name = self.cleaned_data['name']
        ladder.rungs = self.cleaned_data['rungs']
        ladder.is_private = self.cleaned_data['is_private']
        ladder.save()
        for i, ranked in enumerate(ladder.ranking()):
            ranked.rank = self.cleaned_data['rank_{}'.format(i)]
            ranked.save()
