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