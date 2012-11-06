from core.logic.util import get_ladder_or_404
from core.decorators import can_view_ladder, login_required_and_ladder_admin, ladder_is_active
from core.forms import LadderRankingEditForm, LadderConfigurationForm
from core.generic_views import handle_form_and_redirect_to_ladder, handle_form, view_with_ladder


@ladder_is_active
@can_view_ladder
def ladder_page(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    return view_with_ladder(request, ladder, 'basic/ladder_page.html', {'navbar_active': 'ladder'})


@ladder_is_active
@login_required_and_ladder_admin
def configure_ladder_page(request, ladder_id):
    return handle_form_and_redirect_to_ladder(request, ladder_id, LadderConfigurationForm, 'basic/configure_ladder_page.html',
        context={'navbar_active': 'config'}
    )


@ladder_is_active
@can_view_ladder
def display_ladder(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    return view_with_ladder(request, ladder, 'basic/content/ladder_display.html')


@ladder_is_active
@login_required_and_ladder_admin
def edit_ladder(request, ladder_id):
    return handle_form(request, ladder_id, LadderRankingEditForm, 'basic/content/edit_ladder.html',
        form_name='ladder_edit_form',
    ) if not request.POST else display_ladder(request, ladder_id)
