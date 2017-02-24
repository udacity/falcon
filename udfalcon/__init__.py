"""
Imports the rest of the modules in the Falcon dir.
"""

from os.path import dirname, basename, isfile
import glob
from udfalcon.falcon import main

MODULES = glob.glob(dirname(__file__)+"/*.py")
__all__ = [basename(f)[:-3] for f in MODULES if isfile(f) and not f.startswith('_')]

def fly(args={}):
    return main(args)
