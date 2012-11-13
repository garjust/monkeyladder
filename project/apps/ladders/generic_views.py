from django.http import Http404
from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist

from ladders.logic.util import get_ladder_or_404, get_watcher


def handle_form_and_redirect_to_ladder(request, ladder_id, form_class, template, context=None, form_name='form'):
    if not context:
        context = {}
    ladder = get_ladder_or_404(pk=ladder_id)
    if request.POST:
        form = form_class(ladder, request.POST)
        if form.is_valid():
            form.save()
            return redirect(ladder)
    else:
        form = form_class(ladder)
    context[form_name] = form
    return view_with_ladder(request, ladder, template, context=context)


def handle_form(request, ladder_id, form_class, template, context=None, form_name='form'):
    if not context:
        context = {}
    ladder = get_ladder_or_404(pk=ladder_id)
    if request.POST:
        form = form_class(ladder, request.POST)
        if form.is_valid():
            form.save()
            form.success = "Form submitted successfully"
    else:
        form = form_class(ladder)
    context[form_name] = form
    return view_with_ladder(request, ladder, template, context=context)


def view_with_ladder(request, ladder, template, context=None):
    if not context:
        context = {}
    context.update({'ladder': ladder, 'watcher': get_watcher(request.user, ladder)})
    try:
        return render(request, template, context)
    except TemplateDoesNotExist:
        raise Http404("Template does not exist: %s" % template)
