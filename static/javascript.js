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

function setupAjaxLoad() {
	$("a.ajax-load").map(function() {
		var target = $(this).attr("href")
		$(this).attr("href", "#")
		$(this).click(function() {
			$("#" + $(this).attr("data-load-destination-id")).load(target, function(response, status, xhr) {
				if (status == "error") {
		            if (xhr.status == 403) {
		            	// Do nothing
		            } else if (xhr.status == 405) {
		            	alert("ERROR LOADING: " + target)
		            } else {
		            	alert("ERROR LOADING: " + target)
		            }
		        }
			})
		})
	})
}

/*
 * Creates a tooltip with content attached to the right of the element identified by id
 */
function errorTooltip(id, content) {
    var group = $("#" + id)
    group.addClass("form-error")
    group.tooltip({
        placement: "right", title: content
    });
}