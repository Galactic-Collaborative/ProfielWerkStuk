"""
This type stub file was generated by pyright.
"""

import sys
import weakref
from pyglet.canvas.base import Canvas, Display, Screen, ScreenMode
from pyglet import compat_platform, options

"""Display and screen management.

Rendering is performed on a :class:`Canvas`, which conceptually could be an
off-screen buffer, the content area of a :class:`pyglet.window.Window`, or an
entire screen. Currently, canvases can only be created with windows (though
windows can be set fullscreen).

Windows and canvases must belong to a :class:`Display`. On Windows and Mac OS X
there is only one display, which can be obtained with :func:`get_display`.
Linux supports multiple displays, corresponding to discrete X11 display
connections and screens.  :func:`get_display` on Linux returns the default
display and screen 0 (``localhost:0.0``); if a particular screen or display is
required then :class:`Display` can be instantiated directly.

Within a display one or more screens are attached.  A :class:`Screen` often
corresponds to a physical attached monitor, however a monitor or projector set
up to clone another screen will not be listed.  Use :meth:`Display.get_screens`
to get a list of the attached screens; these can then be queried for their
sizes and virtual positions on the desktop.

The size of a screen is determined by its current mode, which can be changed
by the application; see the documentation for :class:`Screen`.

.. versionadded:: 1.2
"""
_is_pyglet_doc_run = ...
_displays = ...
def get_display(): # -> Display | HeadlessDisplay | CocoaDisplay | Win32Display | XlibDisplay:
    """Get the default display device.

    If there is already a :class:`Display` connection, that display will be
    returned. Otherwise, a default :class:`Display` is created and returned.
    If multiple display connections are active, an arbitrary one is returned.

    .. versionadded:: 1.2

    :rtype: :class:`Display`
    """
    ...

if _is_pyglet_doc_run:
    ...
else:
    ...