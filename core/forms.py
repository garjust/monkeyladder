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
    is_private = forms.BooleanField(label=_("Private"))
    type = forms.ChoiceField(label=_("Type"), widget=forms.Select(choices=('BASIC', 'LEADEBOARD',)))

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
