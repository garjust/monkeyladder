from ladders.logic.util import get_ladder_or_404
from ladders.decorators import can_view_ladder, login_required_and_ladder_admin, ladder_is_active
from ladders.forms import LadderRankingEditForm
from ladders.generic_views import handle_form, view_with_ladder


@ladder_is_active
@can_view_ladder
def display_ladder(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    return view_with_ladder(request, ladder, 'basic/content/ladder.html')


@ladder_is_active
@login_required_and_ladder_admin
def edit_ladder(request, ladder_id):
    form_result = handle_form(request, ladder_id, LadderRankingEditForm, 'basic/content/edit_ladder.html',
        form_name='ladder_edit_form',
    )
    return form_result if not request.POST else display_ladder(request, ladder_id)
