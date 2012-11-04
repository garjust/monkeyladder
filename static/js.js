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

function errorTooltip(id, content) {
    var group = $("#" + id)
    group.addClass("form-error")
    group.tooltip({
        placement: "right", title: content
    });
}

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