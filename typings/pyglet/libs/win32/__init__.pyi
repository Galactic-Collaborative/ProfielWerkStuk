"""
This type stub file was generated by pyright.
"""

import atexit
import struct
import warnings
import pyglet
import traceback
from . import com, constants
from .types import *

IS64 = ...
_debug_win32 = ...
DebugLibrary = ...
_gdi32 = ...
_kernel32 = ...
_user32 = ...
_dwmapi = ...
_shell32 = ...
_ole32 = ...
_oleaut32 = ...
if IS64:
    ...
else:
    ...
if _debug_win32:
    _log_win32 = ...
    def win32_errcheck(result, func, args):
        ...
    
    def set_errchecks(lib): # -> None:
        """Set errcheck hook on all functions we have defined."""
        ...
    
