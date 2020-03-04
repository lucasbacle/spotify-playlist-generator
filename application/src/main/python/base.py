from fbs_runtime.application_context.PyQt5 import ApplicationContext, cached_property
from MainWindow import MyApp

class _AppContext(ApplicationContext):
    def run(self):
        self.window.resize(640, 480)
        self.window.show()
        return self.app.exec_()

    def get_design(self):
        return self.get_resource("gui.ui")

    @cached_property
    def window(self):
        return MyApp(self.get_design())

# Color constants
RGB_SAD = (255, 0, 255)
RGB_HAPPY = (20, 255, 255)
RGB_CALM = (0, 255, 197)
RGB_EXCITED = (250, 243, 62)
RGB_SLOW = (144, 190, 109)
RGB_FAST = (232, 226, 136)

# Pages constants
LOGIN_PAGE = 0
SEARCH_PAGE = 1
PLAYER_PAGE = 2

# Search view constants
MIN_TRACKS_NUMBER = 5

# Context (needed by fbs)
context = _AppContext()
