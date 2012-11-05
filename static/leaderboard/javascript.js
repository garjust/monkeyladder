function fixMatchLinks() {
	var view_buttons = $(".match-feed-entry .fix-view-match a")
	view_buttons.attr("href", "#")
	view_buttons.bind("click", function() {
		$.get("/ladders/leaderboard/content/matches/" + $(this).attr("data-id"), function(data) {
			$("#match-bucket").append(data)	
		}).error(function() {
			alert("ERROR")
		})
	})
}

function setupMatchEntry() {
	$("#match-entry-span input").attr("autocomplete", "off")
	$(".player-name-autocomplete").typeahead({
        source: $("#player-name-autocomplete-data").text().split(","), items: 10
    });
}