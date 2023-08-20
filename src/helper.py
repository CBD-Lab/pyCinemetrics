import sys
import os
import platform


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
