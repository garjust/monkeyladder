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