import sys
import os
import platform
import importlib


def resource_path(relative_path):
    myos = platform.system()

    if (myos == 'Windows'):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    elif (myos == 'Darwin') or (myos == 'Linux'):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(
            os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    return None


class Splash:
    def __init__(self):
        if '_PYIBoot_SPLASH' in os.environ and \
                importlib.util.find_spec('pyi_splash'):
            import pyi_splash  # type: ignore
            self.splash = pyi_splash
        else:
            self.splash = None

    def close(self):
        if self.splash:
            self.splash.close()

    def update(self, text):
        if self.splash:
            self.splash.update_text(text)
