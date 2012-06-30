from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils import simplejson

from django.contrib.admin.models import User
from core.models import Ladder, Player, Watcher, Match, MatchPlayer

def home(request):
    newest_ladders = Ladder.objects.filter(is_private=False).order_by('-created')[:50]
    return render_to_response(
        'ladders/home.html',
        {'newest_ladders': newest_ladders, 'navbar_active': 'home'},
        context_instance=RequestContext(request),
    )

def ladder(request, ladder_id):
    ladder = get_object_or_404(Ladder, pk=ladder_id)
    if ladder.is_private:
        if not request.user.is_authenticated() or (len(ladder.player_set.filter(user=request.user)) == 0 and len(ladder.watcher_set.filter(user=request.user)) == 0):
            raise Exception() 
    return render_to_response(
        'ladders/ladder.html',
        {'navbar_active': 'ladder', 'ladder': ladder, 'players': ladder.ranking(), 'player_names': _get_autocomplete_player_list(ladder)},
        context_instance=RequestContext(request),
    )
    
def watchers(request, ladder_id):
    ladder = get_object_or_404(Ladder, pk=ladder_id)
    watchers = ladder.watcher_set.filter()
    return render_to_response(
        'ladders/watchers.html',
        {'navbar_active': 'watchers', 'ladder': ladder, 'watchers': watchers},
        context_instance=RequestContext(request),
    )

@login_required(login_url="/accounts/login")
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

@login_required(login_url="/accounts/login")
def matches(request, ladder_id):
    ladder = get_object_or_404(Ladder, pk=ladder_id)
    matches = ladder.matches()
    return render_to_response(
        'ladders/matches.html',
        {'navbar_active': 'matches', 'ladder': ladder, 'matches': matches},
        context_instance=RequestContext(request)
    )
    
@login_required(login_url='/accounts/login/')
def watched(request):
    watchers = Watcher.objects.filter(user=User.objects.filter(pk=request.user.id))
    return render_to_response(
        'ladders/watched.html',
        {'watchers': watchers, 'navbar_active': 'watched'},
        context_instance=RequestContext(request),
    )

@login_required(login_url='/accounts/login/')
def climbing(request):
    players = Player.objects.filter(user=User.objects.filter(pk=request.user.id))
    return render_to_response(
        'ladders/climbing.html',
        {'players': players, 'navbar_active': 'climbing'},
        context_instance=RequestContext(request),
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
    return _update_error(request, ladder, players, match)
    #_adjust_rankings(players, match.winner.player, match.loser.player)
    return HttpResponseRedirect(reverse('ladders.views.ladder', args=(ladder.id,)))


def _update_error(request, ladder, players, error_message="Unexpected error posting match"):
    return render_to_response(
        'ladders/ladder.html',
        {'navbar_active': 'ladder', 'ladder': ladder, 'players': players, 'error_message': error_message},
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
            
def _get_autocomplete_player_list(ladder):
    players = ladder.player_set.order_by('rank')
    names = []
    for player in players:
        names.append(player.user.get_full_name())
    return ','.join(map(lambda n: '"{}"'.format(n), names))