from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.POST:
        return _do_registration(request)
    return render_to_response('accounts/register.html',
        {'form': UserCreationForm()},
        context_instance=RequestContext(request)
    )
    
def _do_registration(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        print "GOOD FORM"
    return render_to_response('accounts/register.html',
        {'form': UserCreationForm()},
        context_instance=RequestContext(request)
    )

def profile(request):
    return render_to_response('accounts/profile.html',
        {},
        context_instance=RequestContext(request)
    )