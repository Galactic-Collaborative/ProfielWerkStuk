"""
This type stub file was generated by pyright.
"""

"""Events for :py:mod:`pyglet.window`.

See :py:class:`~pyglet.window.Window` for a description of the window event types.
"""
class WindowEventLogger:
    """Print all events to a file.

    When this event handler is added to a window it prints out all events
    and their parameters; useful for debugging or discovering which events
    you need to handle.

    Example::

        win = window.Window()
        event_logger = WindowEventLogger()
        win.push_handlers(event_logger)

    """
    def __init__(self, logfile=...) -> None:
        """Create a `WindowEventLogger` which writes to `logfile`.

        :Parameters:
            `logfile` : file-like object
                The file to write to.  If unspecified, stdout will be used.

        """
        ...
    
    def on_key_press(self, symbol, modifiers): # -> None:
        ...
    
    def on_key_release(self, symbol, modifiers): # -> None:
        ...
    
    def on_text(self, text): # -> None:
        ...
    
    def on_text_motion(self, motion): # -> None:
        ...
    
    def on_text_motion_select(self, motion): # -> None:
        ...
    
    def on_mouse_motion(self, x, y, dx, dy): # -> None:
        ...
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers): # -> None:
        ...
    
    def on_mouse_press(self, x, y, button, modifiers): # -> None:
        ...
    
    def on_mouse_release(self, x, y, button, modifiers): # -> None:
        ...
    
    def on_mouse_scroll(self, x, y, dx, dy): # -> None:
        ...
    
    def on_close(self): # -> None:
        ...
    
    def on_mouse_enter(self, x, y): # -> None:
        ...
    
    def on_mouse_leave(self, x, y): # -> None:
        ...
    
    def on_expose(self): # -> None:
        ...
    
    def on_resize(self, width, height): # -> None:
        ...
    
    def on_move(self, x, y): # -> None:
        ...
    
    def on_activate(self): # -> None:
        ...
    
    def on_deactivate(self): # -> None:
        ...
    
    def on_show(self): # -> None:
        ...
    
    def on_hide(self): # -> None:
        ...
    
    def on_context_lost(self): # -> None:
        ...
    
    def on_context_state_lost(self): # -> None:
        ...
    
    def on_draw(self): # -> None:
        ...
    


