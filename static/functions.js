function fix_match_links() {
	var view_buttons = $(".match-feed-entry .view-button-parent a")
	view_buttons.attr("href", "#")
	view_buttons.bind("click", function() {
		$.get("/ladders/leaderboard/content/matches/" + $(this).attr("data-id"), function(data) {
			$("#match-bucket").append(data)	
		}).error(function() {
			alert("ERROR")
		})
	})
}

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

function setupMatchEntry() {
	$("#match-entry-span input").attr("autocomplete", "off")
	$(".player-name-autocomplete").typeahead({
        source: $("#player-name-autocomplete-data").text().split(","), items: 10
    });
	setupAjaxLoad()
}

