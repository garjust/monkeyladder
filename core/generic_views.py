from django.http import Http404
from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist

from core.logic.util import get_ladder_or_404, get_watcher

def handle_form_and_redirect_to_ladder(request, ladder_id, form_class, template, extra_context=None, form_name='form'):
    if not extra_context:
        extra_context = {}
    ladder = get_ladder_or_404(pk=ladder_id)
    if request.POST:
        form = form_class(ladder, request.POST)
        if form.is_valid():
            form.save()
            return redirect(ladder)
    else:
        form = form_class(ladder)
    context = {'ladder': ladder, form_name: form, 'watcher': get_watcher(request.user, ladder)}
    context.update(extra_context)
    try:
        return render(request, template, context)
    except TemplateDoesNotExist:
        raise Http404("Template does not exist")
