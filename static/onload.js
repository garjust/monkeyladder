// =======
// GENERAL
// =======

/*
$(function() {
	$("a.ajax-load").map(function() {
		var target = $(this).attr("href")
		$(this).attr("href", "#")
		$(this).click(function() {
			$("#match-entry-span").load($(this).attr("data-load-destination"))
		})
	})
})
*/

/*
 * Transforms the contents of every element with the class "right-side-tooltip-error"
 * into a tooltip attached to the elements parent
 */
$(function() {
	$(".right-side-tooltip-error").map(function() {
		errorTooltip($(this).parent().attr("id"), $(this).text())
	})
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