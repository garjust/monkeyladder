from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.template import Context, loader

from ladders.models import Ladder

def collection(request):
    newest_ladders = Ladder.objects.all().order_by('-created')[:5]
    template = loader.get_template('ladders/collection.html')
    context = Context({
        'newest_ladders': newest_ladders
    })
    return HttpResponse(template.render(context))

def element(request, ladder_id):
    ladder = get_object_or_404(Ladder, pk=ladder_id)
    template = loader.get_template('ladders/element.html')
    context = Context({
        'ladder': ladder
    })
    return HttpResponse(template.render(context))

def change(request, ladder_id):
    return HttpResponse("Attempt to change ladders {}".format(ladder_id))