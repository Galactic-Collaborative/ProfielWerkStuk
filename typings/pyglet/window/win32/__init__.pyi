"""
This type stub file was generated by pyright.
"""

import unicodedata
import pyglet
from ctypes import *
from functools import lru_cache
from pyglet import compat_platform
from pyglet.window import BaseWindow, DefaultMouseCursor, MouseCursor, WindowException, _PlatformEventHandler, _ViewEventHandler, key, mouse
from pyglet.event import EventDispatcher
from pyglet.canvas.win32 import Win32Canvas
from pyglet.libs.win32 import _dwmapi, _gdi32, _kernel32, _shell32, _user32
from pyglet.libs.win32.constants import *
from pyglet.libs.win32.winkey import *
from pyglet.libs.win32.types import *

if compat_platform not in ('cygwin', 'win32'):
    ...
_motion_map = ...
class Win32MouseCursor(MouseCursor):
    gl_drawable = ...
    hw_drawable = ...
    def __init__(self, cursor) -> None:
        ...
    


_win32_cursor_visible = ...
Win32EventHandler = ...
ViewEventHandler = ...
class Win32Window(BaseWindow):
    _window_class = ...
    _hwnd = ...
    _dc = ...
    _wgl_context = ...
    _tracking = ...
    _hidden = ...
    _has_focus = ...
    _exclusive_keyboard = ...
    _exclusive_keyboard_focus = ...
    _exclusive_mouse = ...
    _exclusive_mouse_focus = ...
    _exclusive_mouse_screen = ...
    _exclusive_mouse_lpos = ...
    _exclusive_mouse_buttons = ...
    _mouse_platform_visible = ...
    _pending_click = ...
    _in_title_bar = ...
    _keyboard_state = ...
    _ws_style = ...
    _ex_ws_style = ...
    _minimum_size = ...
    _maximum_size = ...
    def __init__(self, *args, **kwargs) -> None:
        ...
    
    def close(self): # -> None:
        ...
    
    vsync = ...
    def set_vsync(self, vsync): # -> None:
        ...
    
    def switch_to(self): # -> None:
        ...
    
    def update_transparency(self): # -> None:
        ...
    
    def flip(self): # -> None:
        ...
    
    def set_location(self, x, y): # -> None:
        ...
    
    def get_location(self): # -> tuple[LONG, LONG]:
        ...
    
    def set_size(self, width, height): # -> None:
        ...
    
    def get_size(self): # -> tuple[int, int]:
        ...
    
    def set_minimum_size(self, width, height): # -> None:
        ...
    
    def set_maximum_size(self, width, height): # -> None:
        ...
    
    def activate(self): # -> None:
        ...
    
    def set_visible(self, visible=...): # -> None:
        ...
    
    def minimize(self): # -> None:
        ...
    
    def maximize(self): # -> None:
        ...
    
    def set_caption(self, caption): # -> None:
        ...
    
    def set_mouse_platform_visible(self, platform_visible=...): # -> None:
        ...
    
    def set_exclusive_mouse(self, exclusive=...): # -> None:
        ...
    
    def set_mouse_position(self, x, y, absolute=...): # -> None:
        ...
    
    def set_exclusive_keyboard(self, exclusive=...): # -> None:
        ...
    
    def get_system_mouse_cursor(self, name): # -> DefaultMouseCursor | Win32MouseCursor:
        ...
    
    def set_icon(self, *images): # -> None:
        ...
    
    def dispatch_events(self): # -> None:
        """Legacy or manual dispatch."""
        ...
    
    def dispatch_pending_events(self): # -> None:
        """Legacy or manual dispatch."""
        ...
    


__all__ = ["Win32EventHandler", "Win32Window"]
