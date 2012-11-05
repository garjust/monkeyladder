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


/*
 * Changes all anchor tags with the ajax-load class to ajax loads
 */
function setupAjaxLoad() {
	$("a.ajax-load").map(function() {
		$(this).removeClass("ajax-load").addClass("ajax-load-ready")
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
$(function() {
	setupAjaxLoad()
})


/*
 * 
 */
function setupAjaxLoadSpans() {
	$("div.ajax-load").map(function() {
		$(this).load($(this).attr("data-load"), function(response, status, xhr) {
			if (status == "error") {
				if (xhr.status == 403) {
	            	// Do nothing
	            } else if (xhr.status == 405) {
	            	alert("ERROR LOADING")
	            } else {
	            	alert("ERROR LOADING")
	            }
			} else {
				
			}
		})
	})
}
$(function() {
	setupAjaxLoadSpans()
})


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


function clickOnload() {
	$(".click-onload").map(function() {
		$(this).click()
	})
}
$(function() {
	clickOnload()
})