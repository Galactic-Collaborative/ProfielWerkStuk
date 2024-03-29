"""
This type stub file was generated by pyright.
"""

from ctypes import *
from pyglet.libs.egl.egl import *
from .base import CanvasConfig, Config, Context

_fake_gl_attributes = ...
class HeadlessConfig(Config):
    def match(self, canvas): # -> list[HeadlessCanvasConfig]:
        ...
    


class HeadlessCanvasConfig(CanvasConfig):
    attribute_ids = ...
    def __init__(self, canvas, egl_config, config) -> None:
        ...
    
    def compatible(self, canvas): # -> bool:
        ...
    
    def create_context(self, share): # -> HeadlessContext:
        ...
    


class HeadlessContext(Context):
    def __init__(self, config, share) -> None:
        ...
    
    def attach(self, canvas): # -> None:
        ...
    
    def set_current(self): # -> None:
        ...
    
    def detach(self): # -> None:
        ...
    
    def destroy(self): # -> None:
        ...
    
    def flip(self): # -> None:
        ...
    


