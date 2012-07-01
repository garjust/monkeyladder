from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from django.contrib.admin.models import User
from core.models import Ladder
from matches.models import Match, MatchPlayer

@login_required(login_url="/accounts/login")
def matches(request, ladder_id):
    if request.POST:
        return _new_match(request, ladder_id)
    ladder = get_object_or_404(Ladder, pk=ladder_id)
    matches = ladder.matches()
    return render_to_response(
        'ladders/matches.html',
        {'navbar_active': 'matches', 'ladder': ladder, 'matches': matches},
        context_instance=RequestContext(request)
    )
    
def _new_match(request, ladder_id):
    ladder = get_object_or_404(Ladder, pk=ladder_id)
    player_one = (request.POST['match-first-player-name'], request.POST['match-first-player-score'])
    player_two = (request.POST['match-second-player-name'], request.POST['match-second-player-score'])     
    return _handle_update(request, ladder, player_one, player_two)    
    
def _handle_update(request, ladder, player_one, player_two):
    try:
        if int(player_one[1]) < 0 or int(player_two[1]) < 0:
            raise ValueError()
    except ValueError:
        return _update_error(request, ladder, ladder.ranking, "Scores must be positive integers")
    player_names = {}
    for player in ladder.ranking():
        player_names[player.user.get_full_name()] = player.user
    if player_one[0] not in player_names or player_two[0] not in player_names:
        return _update_error(request, ladder, ladder.ranking, "Players must be on the ladder")
    match = Match(ladder=ladder)
    match.save()
    match_player_one = MatchPlayer(match=match, user=player_names[player_one[0]], score=player_one[1])
    match_player_one.save()
    match_player_two = MatchPlayer(match=match, user=player_names[player_two[0]], score=player_two[1])
    match_player_two.save()
    return _update_error(request, ladder, ladder.ranking, match)
    #_adjust_rankings(players, match.winner.player, match.loser.player)
    return HttpResponseRedirect(reverse('/ladders/{}/ladder'.format(ladder.id)))

def _get_player_from_full_name(player_name):
    pass

def _update_error(request, ladder, players, error_message="Unexpected error posting match"):
    return render_to_response(
        'ladders/ladder.html',
        {'navbar_active': 'ladder', 'ladder': ladder, 'players': players, 'site_error': error_message},
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