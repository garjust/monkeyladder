__version__ = '1.0'

from robot.libraries.BuiltIn import BuiltIn

from _dictionaries import _Dictionaries

class CommonLibrary(_Dictionaries):
    """
    Common keyword library
    """
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    
    def __init__(self):
        super(CommonLibrary, self).__init__()

    def run_keyword_if_true(self, expression, *args, **kwargs):
        if expression:
            self._run(*args, **kwargs)

    def run_keyword_if_false(self, expression, *args, **kwargs):
        self.run_keyword_if_true(not expression, *args, **kwargs)
