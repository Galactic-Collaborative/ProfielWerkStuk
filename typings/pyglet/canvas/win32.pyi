"""
This type stub file was generated by pyright.
"""

from .base import Canvas, Display, Screen, ScreenMode
from pyglet.libs.win32.constants import *
from pyglet.libs.win32.types import *

class Win32Display(Display):
    def get_screens(self): # -> list[Unknown]:
        ...
    


class Win32Screen(Screen):
    _initial_mode = ...
    def __init__(self, display, handle, x, y, width, height) -> None:
        ...
    
    def get_matching_configs(self, template):
        ...
    
    def get_device_name(self): # -> Any:
        ...
    
    def get_modes(self): # -> list[Unknown]:
        ...
    
    def get_mode(self): # -> Win32ScreenMode:
        ...
    
    def set_mode(self, mode): # -> None:
        ...
    
    def restore_mode(self): # -> None:
        ...
    


class Win32ScreenMode(ScreenMode):
    def __init__(self, screen, mode) -> None:
        ...
    
    def __repr__(self): # -> str:
        ...
    


class Win32Canvas(Canvas):
    def __init__(self, display, hwnd, hdc) -> None:
        ...
    


