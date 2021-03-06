from ladders.logic.util import get_ladder_or_404
from ladders.decorators import can_view_ladder, login_required_and_ladder_admin, ladder_is_active
from ladders.forms import LadderConfigurationForm
from ladders.generic_views import handle_form_and_redirect_to_ladder, view_with_ladder


@ladder_is_active
@can_view_ladder
def ladder_page(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    return view_with_ladder(request, ladder, 'basic/ladder_page.html',
        {'navbar_active': 'ladder'}
    )


@ladder_is_active
@login_required_and_ladder_admin
def configure_ladder_page(request, ladder_id):
    return handle_form_and_redirect_to_ladder(request,
        ladder_id,
        LadderConfigurationForm,
        'basic/configure_ladder_page.html',
        context={'navbar_active': 'config'}
    )
