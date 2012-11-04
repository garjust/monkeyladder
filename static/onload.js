// =======
// GENERAL
// =======


$(function() {
	setupAjaxLoad()
})

/*
 * Transforms the contents of every element with the class "right-side-tooltip-error"
 * into a tooltip attached to the elements parent
 */
function createRightSideErrorTooltips() {
	$(".right-side-tooltip-error").map(function() {
		errorTooltip($(this).parent().attr("id"), $(this).text())
	})
}
$(function() {
	createRightSideErrorTooltips()
})


/*
 * Applies a class to make forms display properly
 */
$(function() {
	$(".control-group label").addClass("control-label");
})


// ========
// ACCOUNTS
// ========


/*
 * Disable autocomplete for the register form
 */
$(function() {
    $("#register-page input").attr("autocomplete", "off")
})


// ===========
// LEADERBOARD
// ===========