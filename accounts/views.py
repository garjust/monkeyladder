from django.shortcuts import render_to_response
from django.template import RequestContext

from accounts.forms import ExtendedUserCreationForm

def register(request):
    if request.POST:
        return _do_registration(request)
    return render_to_response('accounts/register.html',
        {'form': ExtendedUserCreationForm()},
        context_instance=RequestContext(request)
    )
    
def _do_registration(request):
    form = ExtendedUserCreationForm(request.POST)
    if form.is_valid():
        print "GOOD FORM"
        form = ExtendedUserCreationForm()
        form.success = True
    else:
        print "BAD FORM"
    return render_to_response('accounts/register.html',
        {'form': form},
        context_instance=RequestContext(request)
    )

def profile(request):
    return render_to_response('accounts/profile.html',
        {},
        context_instance=RequestContext(request)
    )