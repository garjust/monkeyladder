__version__ = '1.0'

from robot.libraries.BuiltIn import BuiltIn


class CommonLibrary(object):
    """
    Common keyword library
    """
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    
    def __init__(self):
        super(CommonLibrary, self).__init__()

    def do_nothing(self):
        pass