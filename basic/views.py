from core import logic
from core.decorators import can_view_ladder, login_required_and_ladder_admin
from core.forms import LadderRankingEditForm, LadderConfigurationForm
from core.generic_views import handle_form_and_redirect_to_ladder, view_with_ladder


@can_view_ladder
def view_ladder(request, ladder_id):
    ladder = logic.util.get_ladder_or_404(pk=ladder_id)
    return view_with_ladder(request, ladder, 'core/view_ladder.html', {'navbar_active': 'ladder'})


@can_view_ladder
def ladder_display(request, ladder_id):
    ladder = logic.util.get_ladder_or_404(pk=ladder_id)
    return view_with_ladder(request, ladder, 'core/content/ladder_display.html')


@login_required_and_ladder_admin
def edit_ladder(request, ladder_id):
    return handle_form_and_redirect_to_ladder(request, ladder_id, LadderRankingEditForm, 'core/content/ladder_display.html',
        form_name='ladder_edit_form'
    )


@login_required_and_ladder_admin
def configure_ladder(request, ladder_id):
    return handle_form_and_redirect_to_ladder(request, ladder_id, LadderConfigurationForm, 'core/configure_ladder.html',
        context={'navbar_active': 'config'}
    )
