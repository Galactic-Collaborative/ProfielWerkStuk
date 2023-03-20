"""
This type stub file was generated by pyright.
"""

from enum import Enum

class OpenGLAPI(Enum):
    OPENGL = ...
    OPENGL_ES = ...


class Config:
    """Graphics configuration.

    A Config stores the preferences for OpenGL attributes such as the
    number of auxiliary buffers, size of the colour and depth buffers,
    double buffering, stencilling, multi- and super-sampling, and so on.

    Different platforms support a different set of attributes, so these
    are set with a string key and a value which is integer or boolean.

    :Ivariables:
        `double_buffer` : bool
            Specify the presence of a back-buffer for every color buffer.
        `stereo` : bool
            Specify the presence of separate left and right buffer sets.
        `buffer_size` : int
            Total bits per sample per color buffer.
        `aux_buffers` : int
            The number of auxiliary color buffers.
        `sample_buffers` : int
            The number of multisample buffers.
        `samples` : int
            The number of samples per pixel, or 0 if there are no multisample
            buffers.
        `red_size` : int
            Bits per sample per buffer devoted to the red component.
        `green_size` : int
            Bits per sample per buffer devoted to the green component.
        `blue_size` : int
            Bits per sample per buffer devoted to the blue component.
        `alpha_size` : int
            Bits per sample per buffer devoted to the alpha component.
        `depth_size` : int
            Bits per sample in the depth buffer.
        `stencil_size` : int
            Bits per sample in the stencil buffer.
        `accum_red_size` : int
            Bits per pixel devoted to the red component in the accumulation
            buffer.
        `accum_green_size` : int
            Bits per pixel devoted to the green component in the accumulation
            buffer.
        `accum_blue_size` : int
            Bits per pixel devoted to the blue component in the accumulation
            buffer.
        `accum_alpha_size` : int
            Bits per pixel devoted to the alpha component in the accumulation
            buffer.
    """
    _attribute_names = ...
    major_version = ...
    minor_version = ...
    forward_compatible = ...
    opengl_api = ...
    debug = ...
    def __init__(self, **kwargs) -> None:
        """Create a template config with the given attributes.

        Specify attributes as keyword arguments, for example::

            template = Config(double_buffer=True)

        """
        ...
    
    def get_gl_attributes(self): # -> list[tuple[str, Any]]:
        """Return a list of attributes set on this config.

        :rtype: list of tuple (name, value)
        :return: All attributes, with unset attributes having a value of
            ``None``.
        """
        ...
    
    def match(self, canvas):
        """Return a list of matching complete configs for the given canvas.

        .. versionadded:: 1.2

        :Parameters:
            `canvas` : `Canvas`
                Display to host contexts created from the config.

        :rtype: list of `CanvasConfig`
        """
        ...
    
    def create_context(self, share):
        """Create a GL context that satisifies this configuration.

        :deprecated: Use `CanvasConfig.create_context`.

        :Parameters:
            `share` : `Context`
                If not None, a context with which to share objects with.

        :rtype: `Context`
        :return: The new context.
        """
        ...
    
    def is_complete(self): # -> bool:
        """Determine if this config is complete and able to create a context.

        Configs created directly are not complete, they can only serve
        as templates for retrieving a supported config from the system.
        For example, `pyglet.window.Screen.get_matching_configs` returns
        complete configs.

        :deprecated: Use ``isinstance(config, CanvasConfig)``.

        :rtype: bool
        :return: True if the config is complete and can create a context.
        """
        ...
    
    def __repr__(self): # -> str:
        ...
    


class CanvasConfig(Config):
    """OpenGL configuration for a particular canvas.

    Use `Config.match` to obtain an instance of this class.

    .. versionadded:: 1.2

    :Ivariables:
        `canvas` : `Canvas`
            The canvas this config is valid on.

    """
    def __init__(self, canvas, base_config) -> None:
        ...
    
    def compatible(self, canvas):
        ...
    
    def create_context(self, share):
        """Create a GL context that satisifies this configuration.

        :Parameters:
            `share` : `Context`
                If not None, a context with which to share objects with.

        :rtype: `Context`
        :return: The new context.
        """
        ...
    
    def is_complete(self): # -> Literal[True]:
        ...
    


class ObjectSpace:
    def __init__(self) -> None:
        ...
    


class Context:
    """OpenGL context for drawing.

    Use `CanvasConfig.create_context` to create a context.

    :Ivariables:
        `object_space` : `ObjectSpace`
            An object which is shared between all contexts that share
            GL objects.

    """
    _info = ...
    def __init__(self, config, context_share=...) -> None:
        ...
    
    def __repr__(self): # -> str:
        ...
    
    def attach(self, canvas): # -> None:
        ...
    
    def detach(self): # -> None:
        ...
    
    def set_current(self): # -> None:
        ...
    
    def destroy(self): # -> None:
        """Release the context.

        The context will not be useable after being destroyed.  Each platform
        has its own convention for releasing the context and the buffer(s)
        that depend on it in the correct order; this should never be called
        by an application.
        """
        ...
    
    def delete_texture(self, texture_id): # -> None:
        """Safely delete a Texture belonging to this context.

        Usually, the Texture is released immediately using
        ``glDeleteTextures``, however if another context that does not share
        this context's object space is currently active, the deletion will
        be deferred until an appropriate context is activated.

        :Parameters:
            `texture_id` : int
                The OpenGL name of the Texture to delete.

        """
        ...
    
    def delete_buffer(self, buffer_id): # -> None:
        """Safely delete a Buffer object belonging to this context.

        This method behaves similarly to `delete_texture`, though for
        ``glDeleteBuffers`` instead of ``glDeleteTextures``.

        :Parameters:
            `buffer_id` : int
                The OpenGL name of the buffer to delete.

        .. versionadded:: 1.1
        """
        ...
    
    def delete_vao(self, vao_id): # -> None:
        """Safely delete a Vertex Array Object belonging to this context.

        This method behaves similarly to `delete_texture`, though for
        ``glDeleteVertexArrays`` instead of ``glDeleteTextures``.

        :Parameters:
            `vao_id` : int
                The OpenGL name of the Vertex Array to delete.

        .. versionadded:: 2.0
        """
        ...
    
    def delete_shader_program(self, program_id): # -> None:
        """Safely delete a Shader Program belonging to this context.

        This method behaves similarly to `delete_texture`, though for
        ``glDeleteProgram`` instead of ``glDeleteTextures``.

        :Parameters:
            `program_id` : int
                The OpenGL name of the Shader Program to delete.

        .. versionadded:: 2.0
        """
        ...
    
    def get_info(self): # -> GLInfo | None:
        """Get the OpenGL information for this context.

        .. versionadded:: 1.2

        :rtype: `GLInfo`
        """
        ...
    


