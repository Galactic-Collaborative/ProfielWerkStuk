"""
This type stub file was generated by pyright.
"""

class Display:
    """A display device supporting one or more screens.

    .. versionadded:: 1.2
    """
    name = ...
    x_screen:str = ...
    def __init__(self, name:str=..., x_screen=...) -> None:
        """Create a display connection for the given name and screen.

        On X11, :attr:`name` is of the form ``"hostname:display"``, where the
        default is usually ``":1"``.  On X11, :attr:`x_screen` gives the X
        screen number to use with this display.  A pyglet display can only be
        used with one X screen; open multiple display connections to access
        multiple X screens.

        Note that TwinView, Xinerama, xrandr and other extensions present
        multiple monitors on a single X screen; this is usually the preferred
        mechanism for working with multiple monitors under X11 and allows each
        screen to be accessed through a single pyglet`~pyglet.canvas.Display`

        On platforms other than X11, :attr:`name` and :attr:`x_screen` are
        ignored; there is only a single display device on these systems.

        :Parameters:
            name : str
                The name of the display to connect to.
            x_screen : int
                The X11 screen number to use.

        """
        ...

    def get_screens(self):
        """Get the available screens.

        A typical multi-monitor workstation comprises one :class:`Display`
        with multiple :class:`Screen` s.  This method returns a list of
        screens which can be enumerated to select one for full-screen display.

        For the purposes of creating an OpenGL config, the default screen
        will suffice.

        :rtype: list of :class:`Screen`
        """
        ...

    def get_default_screen(self):
        """Get the default (primary) screen as specified by the user's operating system
        preferences.

        :rtype: :class:`Screen`
        """
        ...

    def get_windows(self): # -> list[Unknown]:
        """Get the windows currently attached to this display.

        :rtype: sequence of :class:`~pyglet.window.Window`
        """
        ...



class Screen:
    """A virtual monitor that supports fullscreen windows.

    Screens typically map onto a physical display such as a
    monitor, television or projector.  Selecting a screen for a window
    has no effect unless the window is made fullscreen, in which case
    the window will fill only that particular virtual screen.

    The :attr:`width` and :attr:`height` attributes of a screen give the
    current resolution of the screen.  The :attr:`x` and :attr:`y` attributes
    give the global location of the top-left corner of the screen.  This is
    useful for determining if screens are arranged above or next to one
    another.

    Use :func:`~Display.get_screens` or :func:`~Display.get_default_screen`
    to obtain an instance of this class.
    """

    display: Display
    x: int
    y: int
    width: int
    height: int



    def __init__(self, display, x, y, width, height) -> None:
        """

        :parameters:
            `display` : `~pyglet.canvas.Display`
                :attr:`display`
            `x` : int
                Left edge :attr:`x`
            `y` : int
                Top edge :attr:`y`
            `width` : int
                :attr:`width`
            `height` : int
                :attr:`height`
        """
        ...

    def __repr__(self): # -> str:
        ...

    def get_best_config(self, template=...):
        """Get the best available GL config.

        Any required attributes can be specified in `template`.  If
        no configuration matches the template,
        :class:`~pyglet.window.NoSuchConfigException` will be raised.

        :deprecated: Use :meth:`pyglet.gl.Config.match`.

        :Parameters:
            `template` : `pyglet.gl.Config`
                A configuration with desired attributes filled in.

        :rtype: :class:`~pyglet.gl.Config`
        :return: A configuration supported by the platform that best
            fulfils the needs described by the template.
        """
        ...

    def get_matching_configs(self, template):
        """Get a list of configs that match a specification.

        Any attributes specified in `template` will have values equal
        to or greater in each returned config.  If no configs satisfy
        the template, an empty list is returned.

        :deprecated: Use :meth:`pyglet.gl.Config.match`.

        :Parameters:
            `template` : `pyglet.gl.Config`
                A configuration with desired attributes filled in.

        :rtype: list of :class:`~pyglet.gl.Config`
        :return: A list of matching configs.
        """
        ...

    def get_modes(self):
        """Get a list of screen modes supported by this screen.

        :rtype: list of :class:`ScreenMode`

        .. versionadded:: 1.2
        """
        ...

    def get_mode(self):
        """Get the current display mode for this screen.

        :rtype: :class:`ScreenMode`

        .. versionadded:: 1.2
        """
        ...

    def get_closest_mode(self, width, height): # -> None:
        """Get the screen mode that best matches a given size.

        If no supported mode exactly equals the requested size, a larger one
        is returned; or ``None`` if no mode is large enough.

        :Parameters:
            `width` : int
                Requested screen width.
            `height` : int
                Requested screen height.

        :rtype: :class:`ScreenMode`

        .. versionadded:: 1.2
        """
        ...

    def set_mode(self, mode):
        """Set the display mode for this screen.

        The mode must be one previously returned by :meth:`get_mode` or
        :meth:`get_modes`.

        :Parameters:
            `mode` : `ScreenMode`
                Screen mode to switch this screen to.

        """
        ...

    def restore_mode(self):
        """Restore the screen mode to the user's default.
        """
        ...



class ScreenMode:
    """Screen resolution and display settings.

    Applications should not construct `ScreenMode` instances themselves; see
    :meth:`Screen.get_modes`.

    The :attr:`depth` and :attr:`rate` variables may be ``None`` if the
    operating system does not provide relevant data.

    .. versionadded:: 1.2

    """
    width = ...
    height = ...
    depth = ...
    rate = ...
    def __init__(self, screen) -> None:
        """

        :parameters:
            `screen` : `Screen`
        """
        ...

    def __repr__(self): # -> str:
        ...



class Canvas:
    """Abstract drawing area.

    Canvases are used internally by pyglet to represent drawing areas --
    either within a window or full-screen.

    .. versionadded:: 1.2
    """
    def __init__(self, display) -> None:
        """

        :parameters:
            `display` : `Display`
                :attr:`display`

        """
        ...
