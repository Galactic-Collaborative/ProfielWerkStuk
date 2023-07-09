"""
This type stub file was generated by pyright.
"""

import unicodedata
import urllib.parse
import pyglet
from ctypes import *
from functools import lru_cache
from pyglet.window import BaseWindow, DefaultMouseCursor, ImageMouseCursor, MouseCursor, MouseCursorException, WindowException, _PlatformEventHandler, _ViewEventHandler, key, mouse
from pyglet.event import EventDispatcher
from pyglet.canvas.xlib import XlibCanvas
from pyglet.libs.x11 import cursorfont, xlib
from pyglet.util import asbytes

class mwmhints_t(Structure):
    _fields_ = ...


XkbSetDetectableAutoRepeat = ...
_can_detect_autorepeat = ...
XA_CARDINAL = ...
XA_ATOM = ...
XDND_VERSION = ...
_have_utf8 = ...
_motion_map = ...
class XlibException(WindowException):
    """An X11-specific exception.  This exception is probably a programming
    error in pyglet."""
    ...


class XlibMouseCursor(MouseCursor):
    gl_drawable = ...
    hw_drawable = ...
    def __init__(self, cursor) -> None:
        ...
    


XlibEventHandler = ...
ViewEventHandler = ...
class XlibWindow(BaseWindow):
    _x_display = ...
    _x_screen_id = ...
    _x_ic = ...
    _window = ...
    _override_redirect = ...
    _x = ...
    _y = ...
    _mouse_exclusive_client = ...
    _mouse_buttons = ...
    _active = ...
    _applied_mouse_exclusive = ...
    _applied_keyboard_exclusive = ...
    _mapped = ...
    _lost_context = ...
    _lost_context_state = ...
    _enable_xsync = ...
    _current_sync_value = ...
    _current_sync_valid = ...
    _default_event_mask = ...
    def __init__(self, *args, **kwargs) -> None:
        ...
    
    def close(self): # -> None:
        ...
    
    def switch_to(self): # -> None:
        ...
    
    def flip(self): # -> None:
        ...
    
    def set_vsync(self, vsync: bool) -> None:
        ...
    
    def set_caption(self, caption): # -> None:
        ...
    
    def set_wm_class(self, name): # -> None:
        ...
    
    def get_caption(self): # -> str:
        ...
    
    def set_size(self, width: int, height: int) -> None:
        ...
    
    def set_location(self, x, y): # -> None:
        ...
    
    def get_location(self): # -> tuple[int, int]:
        ...
    
    def activate(self): # -> None:
        ...
    
    def set_visible(self, visible: bool = ...) -> None:
        ...
    
    def set_minimum_size(self, width: int, height: int) -> None:
        ...
    
    def set_maximum_size(self, width: int, height: int) -> None:
        ...
    
    def minimize(self): # -> None:
        ...
    
    def maximize(self): # -> None:
        ...
    
    def set_mouse_platform_visible(self, platform_visible=...): # -> None:
        ...
    
    def set_mouse_position(self, x, y): # -> None:
        ...
    
    def set_exclusive_mouse(self, exclusive=...): # -> None:
        ...
    
    def set_exclusive_keyboard(self, exclusive=...): # -> None:
        ...
    
    def get_system_mouse_cursor(self, name): # -> DefaultMouseCursor | XlibMouseCursor:
        ...
    
    def set_icon(self, *images): # -> None:
        ...
    
    def dispatch_events(self): # -> None:
        ...
    
    def dispatch_pending_events(self): # -> None:
        ...
    
    def dispatch_platform_event(self, e): # -> None:
        ...
    
    def dispatch_platform_event_view(self, e): # -> None:
        ...
    
    def get_single_property(self, window, atom_property, atom_type): # -> tuple[_Pointer[c_ubyte], int]:
        """ Returns the length and data of a window property. """
        ...
    
    @staticmethod
    def parse_filenames(decoded_string): # -> list[Unknown]:
        """All of the filenames from file drops come as one big string with
            some special characters (%20), this will parse them out.
        """
        ...
    


__all__ = ["XlibEventHandler", "XlibWindow"]