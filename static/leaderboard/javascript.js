function fixMatchLinks() {
	$(".match-feed-entry .view-match-link").attr("href", "#").bind("click", function() {
		$.get("/ladders/leaderboard/content/matches/" + $(this).attr("data-id"), function(data) {
			$("#match-bucket").append(data)	
		}).error(function() {
			alert("ERROR")
		})
	})
}


function setupMatchEntry() {
	$("#match-entry-span fieldset input").attr("autocomplete", "off")
	$(".player-name-autocomplete").removeClass("player-name-autocomplete").addClass("player-name-autocompleted").typeahead({
        source: $("#player-name-autocomplete-data").text().split(","), items: 10
    })
}