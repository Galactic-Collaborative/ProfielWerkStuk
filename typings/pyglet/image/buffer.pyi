"""
This type stub file was generated by pyright.
"""

from pyglet.gl import *

def get_max_color_attachments(): # -> int:
    """Get the maximum allow Framebuffer Color attachements"""
    ...

class Renderbuffer:
    """OpenGL Renderbuffer Object"""
    def __init__(self, width, height, internal_format, samples=...) -> None:
        """Create an instance of a Renderbuffer object."""
        ...
    
    @property
    def id(self): # -> int:
        ...
    
    @property
    def width(self): # -> Unknown:
        ...
    
    @property
    def height(self): # -> Unknown:
        ...
    
    def bind(self): # -> None:
        ...
    
    @staticmethod
    def unbind(): # -> None:
        ...
    
    def delete(self): # -> None:
        ...
    
    def __del__(self): # -> None:
        ...
    
    def __repr__(self): # -> str:
        ...
    


class Framebuffer:
    """OpenGL Framebuffer Object"""
    def __init__(self, target=...) -> None:
        """Create an OpenGL Framebuffer object.

        :rtype: :py:class:`~pyglet.image.Framebuffer`

        .. versionadded:: 2.0
        """
        ...
    
    @property
    def id(self): # -> int:
        ...
    
    @property
    def width(self): # -> int:
        """The width of the widest attachment."""
        ...
    
    @property
    def height(self): # -> int:
        """The width of the widest attachment."""
        ...
    
    def bind(self): # -> None:
        ...
    
    def unbind(self): # -> None:
        ...
    
    def clear(self): # -> None:
        ...
    
    def delete(self): # -> None:
        ...
    
    @property
    def is_complete(self): # -> Any:
        ...
    
    @staticmethod
    def get_status(): # -> str:
        ...
    
    def attach_texture(self, texture, target=..., attachment=...): # -> None:
        """Attach a Texture to the Framebuffer

        :Parameters:
            `texture` : pyglet.image.Texture
                Specifies the texture object to attach to the framebuffer attachment
                point named by attachment.
            `target` : int
                Specifies the framebuffer target. target must be GL_DRAW_FRAMEBUFFER,
                GL_READ_FRAMEBUFFER, or GL_FRAMEBUFFER. GL_FRAMEBUFFER is equivalent
                to GL_DRAW_FRAMEBUFFER.
            `attachment` : int
                Specifies the attachment point of the framebuffer. attachment must be
                GL_COLOR_ATTACHMENTi, GL_DEPTH_ATTACHMENT, GL_STENCIL_ATTACHMENT or
                GL_DEPTH_STENCIL_ATTACHMENT.
        """
        ...
    
    def attach_texture_layer(self, texture, layer, level, target=..., attachment=...): # -> None:
        """Attach a Texture layer to the Framebuffer

        :Parameters:
            `texture` : pyglet.image.TextureArray
                Specifies the texture object to attach to the framebuffer attachment
                point named by attachment.
            `layer` : int
                Specifies the layer of texture to attach.
            `level` : int
                Specifies the mipmap level of texture to attach.
            `target` : int
                Specifies the framebuffer target. target must be GL_DRAW_FRAMEBUFFER,
                GL_READ_FRAMEBUFFER, or GL_FRAMEBUFFER. GL_FRAMEBUFFER is equivalent
                to GL_DRAW_FRAMEBUFFER.
            `attachment` : int
                Specifies the attachment point of the framebuffer. attachment must be
                GL_COLOR_ATTACHMENTi, GL_DEPTH_ATTACHMENT, GL_STENCIL_ATTACHMENT or
                GL_DEPTH_STENCIL_ATTACHMENT.
        """
        ...
    
    def attach_renderbuffer(self, renderbuffer, target=..., attachment=...): # -> None:
        """"Attach a Renderbuffer to the Framebuffer

        :Parameters:
            `renderbuffer` : pyglet.image.Renderbuffer
                Specifies the Renderbuffer to attach to the framebuffer attachment
                point named by attachment.
            `target` : int
                Specifies the framebuffer target. target must be GL_DRAW_FRAMEBUFFER,
                GL_READ_FRAMEBUFFER, or GL_FRAMEBUFFER. GL_FRAMEBUFFER is equivalent
                to GL_DRAW_FRAMEBUFFER.
            `attachment` : int
                Specifies the attachment point of the framebuffer. attachment must be
                GL_COLOR_ATTACHMENTi, GL_DEPTH_ATTACHMENT, GL_STENCIL_ATTACHMENT or
                GL_DEPTH_STENCIL_ATTACHMENT.
        """
        ...
    
    def __del__(self): # -> None:
        ...
    
    def __repr__(self): # -> str:
        ...
    

