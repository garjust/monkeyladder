from robot_mixin.simple_mixin import SimpleMixin

class _Dictionaries(SimpleMixin):
    """
    Common keyword library
    """
    
    def __init__(self):
        super(_Dictionaries, self).__init__()

    def create_dictionary(self, *keyvalues):
        return self._list_to_dictionary(keyvalues)

    def create_dictionary_and_set(self, variable, *keyvalues):
        print "*WARN*%s" % variable
        dictionary = self._run("Create Dictionary", *keyvalues)
        self._set_variable(variable, dictionary)
        return dictionary