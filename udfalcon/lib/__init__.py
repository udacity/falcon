import os

_ROOT = os.path.abspath(os.path.dirname(__file__))

def get_lib(path):
    return os.path.join(_ROOT, path)

__all__ = ['get_lib']
