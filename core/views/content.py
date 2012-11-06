from core import logic
from core.decorators import can_view_ladder, login_required_and_ladder_admin, ladder_is_active
from core.models import Watcher
from django.shortcuts import redirect

import logging
logger = logging.getLogger('monkeyladder')


@ladder_is_active
@can_view_ladder
def watch_ladder(request, ladder_id):
    ladder = logic.util.get_ladder_or_404(pk=ladder_id)
    watcher = Watcher.objects.create(ladder=ladder, user=request.user, type='NORMAL', created_by=request.user)
    logger.info("Watcher created: %s" % watcher)
    return redirect(ladder)


@ladder_is_active
@login_required_and_ladder_admin
def delete_ladder(request, ladder_id):
    ladder = logic.util.get_ladder_or_404(pk=ladder_id)
    ladder.is_active = False
    ladder.save()
    logger.info("Ladder state set to inactive: %s" % ladder)
    return redirect('/home/')
