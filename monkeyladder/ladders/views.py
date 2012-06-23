from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from ladders.models import *

def home(request):
    newest_ladders = Ladder.objects.all().order_by('-created')[:50]
    return render_to_response(
        'ladders/home.html',
        {'newest_ladders': newest_ladders, 'navbar_active': 'home'}
    )

def watched(request):
    return render_to_response(
        'ladders/watched.html',
        {'navbar_active': 'watched'}
    )

def climbing(request):
    return render_to_response(
        'ladders/climbing.html',
        {'navbar_active': 'climbing'}
    )

def ladder(request, ladder_id):
    ladder = get_object_or_404(Ladder, pk=ladder_id)
    return render_to_response(
        'ladders/ladder.html',
        {'ladder': ladder, 'players': ladder.ranking()},
        context_instance=RequestContext(request)
    )

def update(request, ladder_id):
    ladder = get_object_or_404(Ladder, pk=ladder_id)
    players = ladder.ranking()
    match_players = []
    try:
        for player in players:
            player_score = request.POST['match-entry-player-{}-score'.format(player.id)]
            if len(player_score) > 0:
                match_players.append((player, int(player_score)))
    except ValueError:
        return _update_error(request, ladder, players, "Scores must be positive integers")
    return _handle_update(request, ladder, players, match_players)

def matches(request, ladder_id):
    ladder = get_object_or_404(Ladder, pk=ladder_id)
    matches = ladder.matches()
    return render_to_response(
        'ladders/matches.html',
        {'ladder': ladder, 'matches': matches}
    )

def _handle_update(request, ladder, players, match_players):
    for match_player in match_players:
        if match_player[1] < 0:
            return _update_error(request, ladder, players, "Scores must be positive integers")
    if len(match_players) != 2:
        return _update_error(request, ladder, players, "Only two players per match")
    match = Match(ladder=ladder)
    match.save()
    for match_player in match_players:
        match_player = MatchPlayer(match=match, player=match_player[0], score=match_player[1])
        match_player.save()
    return _update_error(request, ladder, players, '{}//{}'.format(match, match_players))
    #_adjust_rankings(players, winner, loser)
    return HttpResponseRedirect(reverse('ladders.views.ladder', args=(ladder.id,)))


def _update_error(request, ladder, players, error_message="Unexpected error posting match"):
    return render_to_response(
        'ladders/ladder.html',
        {'ladder': ladder, 'players': players, 'error_message': error_message},
        context_instance=RequestContext(request)
    )

def _adjust_rankings(players, winner, loser):
    rank_diff = winner.rank - loser.rank
    if rank_diff <= 0:
        return
    elif rank_diff <= 2:
        temp = winner.rank
        winner.rank = loser.rank
        loser.rank = temp
        winner.save()
        loser.save()
    else:
        players_slice = players[loser.rank-1:winner.rank]
        players_slice[0].rank += 1
        players_slice[1].rank -= 1
        players_slice[len(players_slice)-1].rank -= 2
        players_slice[len(players_slice)-2].rank += 1
        players_slice[len(players_slice)-3].rank += 1
        for player in players_slice:
            player.save()