import logging
logger = logging.getLogger('monkeyladder')

class LadderPlayerAutocomplete(object):
    """
    Class to get the autocomplete list for match entry
    """
    
    def __init__(self, *args, **kwargs):
        object.__init__(self, *args, **kwargs)
        
    def get_autocomplete_list(self, ladder):
        players = ladder.player_set.order_by('rank')
        names = []
        for player in players:
            names.append(player.name())
        return self._format_for_injection(names)
    
    def _format_for_injection(self, names):
        """
        Formats the list of names into a string that can be injected into javascript
        """
        return ','.join(map(lambda n: '"{}"'.format(n), names))
    
class LadderAccessPermission(object):
    
    def __init__(self, user, *args, **kwargs):
        object.__init__(self, *args, **kwargs)
        self.user = user
        
    def has_permission(self, ladder):
        return self.user.is_authenticated() and (len(ladder.player_set.filter(user=self.user)) != 0 or len(ladder.watcher_set.filter(user=self.user)) != 0)
    
class LadderContext(object):
    
    def __init__(self, *args, **kwargs):
        object.__init__(self, *args, **kwargs)
        
    def get(self, ladder, *partial_contexts):
        context = {'navbar_active': 'ladder', 'ladder': ladder, 'player_names': LadderPlayerAutocomplete().get_autocomplete_list(ladder), 'match_feed': ladder.match_feed()}
        for partial_context in partial_contexts:
            context.update(partial_context)
        return context
    
def get_best_name(user):
    if user.get_full_name():
        return user.get_full_name()
    return user.username