from django.contrib.auth.forms import forms, _

from core.models import Ladder, Watcher

class LadderCreationForm(forms.Form):
    """
    A form that creates a ladder and a ladder admin
    """
    error_messages = {
        'too_many_rungs': _("Ladder can have a maximum 100 rungs"),
        'invalid_user': _("User does not exist"),
    }

    def __init__(self, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)

    name = forms.CharField(label=_("Ladder Name"))
    rungs = forms.IntegerField(label=_("Rungs"), min_value=1)
    is_private = forms.BooleanField(label=_("Private"), required=False)
    type = forms.ChoiceField(label=_("Type"), choices=Ladder.TYPES, widget=forms.Select)

    def clean_rungs(self):
        if self.cleaned_data['rungs'] > 100:
            raise forms.ValidationError(self.error_messages['too_many_rungs'])
        return self.cleaned_data['rungs']

    def save(self, user):
        ladder = Ladder.objects.create(
            name=self.cleaned_data['name'],
            rungs=self.cleaned_data['rungs'],
            is_private=self.cleaned_data['is_private'],
            type=self.cleaned_data['type'],
            created_by=user
        )
        Watcher.objects.create(ladder=ladder, user=user, type='ADMIN')
        return ladder

class LadderRankingEditForm(forms.Form):
    """
    A form to edit the rankings of a ladder
    """
    error_messages = {
        'invalid_ranks': _("Ranks must be unique and consistent")
    }

    def __init__(self, ladder, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)
        self.ladder = ladder
        self.ladder_ranking = ladder.ranking()
        self.ranking = []
        for i, ranked in enumerate(self.ladder_ranking):
            self.fields['rank_%s' % i] = forms.IntegerField(initial=ranked.rank, min_value=1, widget=forms.TextInput(attrs={'class': 'input-mini'}))
            self.ranking.append({'ranked': ranked, 'field': self['rank_%s' % i]})

    def ranked(self, values=False):
        if values:
            return map(lambda r: self.cleaned_data['rank_%s' % r['ranked'].rank], self.ranking)
        return self.ranking

    def clean(self):
        return self.cleaned_data

    def save(self):
        for i, ranked in enumerate(self.ladder_ranking):
            ranked.rank = self.cleaned_data['rank_%s' % i]
            ranked.save()

class LadderConfigurationForm(forms.Form):
    """
    A form that edits an existing ladder
    """

    def __init__(self, ladder, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)
        self.ladder = ladder
        self.fields['name'].initial = ladder.name
        self.fields['rungs'].initial = ladder.rungs
        self.fields['is_private'].initial = ladder.is_private

    name = forms.CharField(required=False)
    rungs = forms.IntegerField(min_value=1, required=False)
    is_private = forms.BooleanField(required=False)

    def clean(self):
        return self.cleaned_data

    def save(self):
        if self.cleaned_data['name']:
            self.ladder.name = self.cleaned_data['name']
        if self.cleaned_data['rungs']:
            self.ladder.rungs = self.cleaned_data['rungs']
        self.ladder.is_private = self.cleaned_data['is_private']
        self.ladder.save()
