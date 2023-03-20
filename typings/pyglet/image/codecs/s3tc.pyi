"""
This type stub file was generated by pyright.
"""

from pyglet.gl import *
from pyglet.image import AbstractImage

"""Software decoder for S3TC compressed texture (i.e., DDS).

http://oss.sgi.com/projects/ogl-sample/registry/EXT/texture_compression_s3tc.txt
"""
split_8byte = ...
split_16byte = ...
class PackedImageData(AbstractImage):
    _current_texture = ...
    def __init__(self, width, height, fmt, packed_format, data) -> None:
        ...
    
    def unpack(self): # -> None:
        ...
    
    texture = ...
    def get_texture(self, rectangle=..., force_rectangle=...): # -> Texture:
        """The parameters 'rectangle' and 'force_rectangle' are ignored.
           See the documentation of the method 'AbstractImage.get_texture' for
           a more detailed documentation of the method. """
        ...
    


def decode_dxt1_rgb(data, width, height): # -> PackedImageData:
    ...

def decode_dxt1_rgba(data, width, height): # -> PackedImageData:
    ...

def decode_dxt3(data, width, height): # -> PackedImageData:
    ...

def decode_dxt5(data, width, height): # -> PackedImageData:
    ...

