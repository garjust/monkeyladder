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
 * 
 */
function loadAjaxSpans() {
	$("div.ajax-load").map(function() {
		$(this).bind("loaded", function() {
			linkAjaxAnchorLoad()
			linkAjaxSubmit()
		    linkAjaxSelectChange()
		})
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
				$(this).trigger("loaded")
			}
		})
	})
}
$(function() {
	loadAjaxSpans()
})


/*
 * Changes all anchor tags with the ajax-load class to ajax loads
 */
function linkAjaxAnchorLoad() {
	$("a.ajax-load").map(function() {
		var loadUrl = $(this).attr("href")
		$(this).removeClass("ajax-load").addClass("ajax-load-ready").attr("href", "#").click(function() {
			$("#" + $(this).attr("data-load-target")).load(loadUrl, function(response, status, xhr) {
				if (status == "error") {
		            if (xhr.status == 403) {
		            	// Do nothing
		            } else if (xhr.status == 405) {
		            	alert("ERROR LOADING: " + loadUrl)
		            } else {
		            	alert("ERROR LOADING: " + loadUrl)
		            }
		        } else {
		        	$(this).trigger("loaded")
		        }
			})
		})
	})
}
$(function() {
	linkAjaxAnchorLoad()
})


/*
 * 
 */
function linkAjaxSelectChange() {
	$("div.ajax-change").removeClass("ajax-change").addClass("ajax-change-ready").change(function () {
		$("#" + $(this).attr("data-load-target")).load($(this).attr("data-load-url") + "" + $(this).find("option:selected").attr("value"), function(response, status, xhr) {
			$(this).trigger("loaded")
		})
	})
}
$(function() {
	linkAjaxSelectChange()
})


/*
 * 
 */
function linkAjaxSubmit() {
	$("form.ajax-submit").map(function() {
		var form = $(this)
		form.removeClass("ajax-submit").addClass("ajax-submit-ready").submit(function(e) {
			var submitButton = $(".monkey-form-actions input")
			submitButton.attr('disabled', true)
			$("#" + submitButton.attr("data-load-target")).load(form.attr('action'), form.serializeArray(), function(response, status, xhr) {
	        	submitButton.attr('disabled', false)
	            if (status == "error") {
	                alert("Failed to submit form: " + form)
	            } else {
	            	$(this).trigger("loaded").trigger("submitted")
	            }
	            createRightSideErrorTooltips()
	        });
	        e.preventDefault();
		})
	})
}
$(function() {
	linkAjaxSubmit()
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


/*
 * 
 */
function clickOnload() {
	$(".click-onload").map(function() {
		$(this).click()
	})
}
$(function() {
	clickOnload()
})