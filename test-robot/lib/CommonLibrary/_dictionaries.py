from robot_mixin.simple_mixin import SimpleMixin

import random

class _Dictionaries(SimpleMixin):
    """
    Keywords handling dictionary tasks
    """
    
    def __init__(self):
        super(_Dictionaries, self).__init__()

    def random_string(self, length=6):
        string = ''
        for i in range(length):
            string += str(random.randint(0, 9))
        return string

    def create_dictionary(self, *keyvalues):
        return self._list_to_dictionary(keyvalues)

    def create_dictionary_and_set(self, variable, *keyvalues):
        dictionary = self._run("Create Dictionary", *keyvalues)
        self._set_variable(variable, dictionary)
        return dictionary

    def append_random_string_to_dictionary_values(self, dictionary, *keys):
        for key in keys:
            dictionary[key] = '%s_%s' % (dictionary[key], self.random_string())