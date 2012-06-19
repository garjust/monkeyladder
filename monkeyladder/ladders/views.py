from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from ladders.models import *

def home(request):
    newest_ladders = Ladder.objects.all().order_by('-created')[:5]
    return render_to_response('ladders/home.html', {'newest_ladders': newest_ladders, 'navbar_active': 'home'})

def watched(request):
    return render_to_response('ladders/watched.html', {'navbar_active': 'watched'})

def climbing(request):
    return render_to_response('ladders/climbing.html', {'navbar_active': 'climbing'})

def ladder(request, ladder_id):
    ladder = get_object_or_404(Ladder, pk=ladder_id)
    players = _get_players(ladder)
    return render_to_response('ladders/ladder.html', {'ladder': ladder, 'players': players}, context_instance=RequestContext(request))

def update(request, ladder_id):
    ladder = get_object_or_404(Ladder, pk=ladder_id)
    players = _get_players(ladder)
    try:
        winner = ladder.player_set.get(pk=int(request.POST['winner']))
        loser = ladder.player_set.get(pk=int(request.POST['loser']))
    except KeyError, Player.DoesNotExist:
        return render_to_response(
            'ladders/ladder.html',
            {'ladder': ladder, 'players': players, 'error_message': "Must select a winner and loser"},
            context_instance=RequestContext(request)
        )
    else:
        if winner.id == loser.id:
            return render_to_response(
                'ladders/ladder.html',
                {'ladder': ladder, 'players': players, 'error_message': "One person cannot win and lose a game at the same time"},
                context_instance=RequestContext(request)
            )
        _adjust_rankings(players, winner, loser)
    return HttpResponseRedirect(reverse('ladders.views.ladder', args=(ladder.id,)))

def _get_players(ladder):
    return ladder.player_set.filter().order_by('rank')

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