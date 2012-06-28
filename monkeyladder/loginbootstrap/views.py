from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

def login(request):
    return render_to_response(
        'loginbootstrap/login.html',
        {'app': 'Monkeyladder', 'navbar_active': 'login'},
        context_instance=RequestContext(request)
    )

def auth(request):
    return render_to_response(
        'loginbootstrap/login.html',
        {'app': 'Monkeyladder', 'navbar_active': 'home'},
        context_instance=RequestContext(request)
    )