from core.models import Ladder

import logging
logger = logging.getLogger('monkeyladder')
      
def get_autocomplete_list(ladder):
    """
    Returns a list of names of players on the given ladder
    """
    players = ladder.player_set.order_by('rank')
    names = []
    for player in players:
        names.append(player.user.get_profile().name())
    return _format_names_for_injection(names)

def _format_names_for_injection(names):
    """
    Formats the list of names into a string that can be injected into javascript
    """
    return ','.join(map(lambda n: '"{}"'.format(n), names))
        
def has_ladder_permission(user, ladder):
    return user.is_authenticated() and (len(ladder.player_set.filter(user=user)) != 0 or len(ladder.watcher_set.filter(user=user)) != 0)
        
def get_ladder_context(ladder, *partial_contexts):
    context = {'navbar_active': 'ladder', 'ladder': ladder, 'player_names': get_autocomplete_list(ladder), 'match_feed': ladder.match_feed()}
    for partial_context in partial_contexts:
        context.update(partial_context)
    return context
    
def public_ladder_feed(order='-created', size=5):
    return Ladder.objects.filter(is_private=False).order_by[order][:size]

def watched_ladder_feed(user, order='-created', size=5):
    return Ladder.objects.filter(is_private=True).order_by[order][:size]