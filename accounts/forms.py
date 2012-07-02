
from django.contrib.auth.forms import UserCreationForm, forms, _

class ExtendedUserCreationForm(UserCreationForm):
    
    email = forms.EmailField(label=_("Email"))
    first_name = forms.CharField(label=_("First Name"), max_length=20)
    last_name = forms.CharField(label=_("Last Name"), max_length=20)
    
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user