"""
This type stub file was generated by pyright.
"""

from pyglet import event

_is_pyglet_doc_run = ...
class PlatformEventLoop:
    """ Abstract class, implementation depends on platform.

    .. versionadded:: 1.2
    """
    def __init__(self) -> None:
        ...
    
    def is_running(self): # -> bool:
        """Return True if the event loop is currently processing, or False
        if it is blocked or not activated.

        :rtype: bool
        """
        ...
    
    def post_event(self, dispatcher, event, *args): # -> None:
        """Post an event into the main application thread.

        The event is queued internally until the :py:meth:`run` method's thread
        is able to dispatch the event.  This method can be safely called
        from any thread.

        If the method is called from the :py:meth:`run` method's thread (for
        example, from within an event handler), the event may be dispatched
        within the same runloop iteration or the next one; the choice is
        nondeterministic.

        :Parameters:
            `dispatcher` : EventDispatcher
                Dispatcher to process the event.
            `event` : str
                Event name.
            `args` : sequence
                Arguments to pass to the event handlers.

        """
        ...
    
    def dispatch_posted_events(self): # -> None:
        """Immediately dispatch all pending events.

        Normally this is called automatically by the runloop iteration.
        """
        ...
    
    def notify(self):
        """Notify the event loop that something needs processing.

        If the event loop is blocked, it will unblock and perform an iteration
        immediately.  If the event loop is running, another iteration is
        scheduled for immediate execution afterwards.
        """
        ...
    
    def start(self): # -> None:
        ...
    
    def step(self, timeout=...):
        ...
    
    def set_timer(self, func, interval): # -> None:
        ...
    
    def stop(self): # -> None:
        ...
    


class EventLoop(event.EventDispatcher):
    """The main run loop of the application.

    Calling `run` begins the application event loop, which processes
    operating system events, calls :py:func:`pyglet.clock.tick` to call
    scheduled functions and calls :py:meth:`pyglet.window.Window.on_draw` and
    :py:meth:`pyglet.window.Window.flip` to update window contents.

    Applications can subclass :py:class:`EventLoop` and override certain methods
    to integrate another framework's run loop, or to customise processing
    in some other way.  You should not in general override :py:meth:`run`, as
    this method contains platform-specific code that ensures the application
    remains responsive to the user while keeping CPU usage to a minimum.
    """
    _has_exit_condition = ...
    _has_exit = ...
    def __init__(self) -> None:
        ...
    
    def run(self, interval=...): # -> None:
        """Begin processing events, scheduled functions and window updates.

        This method returns when :py:attr:`has_exit` is set to True.

        Developers are discouraged from overriding this method, as the
        implementation is platform-specific.
        """
        ...
    
    def enter_blocking(self): # -> None:
        """Called by pyglet internal processes when the operating system
        is about to block due to a user interaction.  For example, this
        is common when the user begins resizing or moving a window.

        This method provides the event loop with an opportunity to set up
        an OS timer on the platform event loop, which will continue to
        be invoked during the blocking operation.

        The default implementation ensures that :py:meth:`idle` continues to be
        called as documented.

        .. versionadded:: 1.2
        """
        ...
    
    @staticmethod
    def exit_blocking(): # -> None:
        """Called by pyglet internal processes when the blocking operation
        completes.  See :py:meth:`enter_blocking`.
        """
        ...
    
    def idle(self): # -> float | None:
        """Called during each iteration of the event loop.

        The method is called immediately after any window events (i.e., after
        any user input).  The method can return a duration after which
        the idle method will be called again.  The method may be called
        earlier if the user creates more input events.  The method
        can return `None` to only wait for user events.

        For example, return ``1.0`` to have the idle method called every
        second, or immediately after any user events.

        The default implementation dispatches the
        :py:meth:`pyglet.window.Window.on_draw` event for all windows and uses
        :py:func:`pyglet.clock.tick` and :py:func:`pyglet.clock.get_sleep_time`
        on the default clock to determine the return value.

        This method should be overridden by advanced users only.  To have
        code execute at regular intervals, use the
        :py:func:`pyglet.clock.schedule` methods.

        :rtype: float
        :return: The number of seconds before the idle method should
            be called again, or `None` to block for user input.
        """
        ...
    
    @property
    def has_exit(self): # -> bool:
        """Flag indicating if the event loop will exit in
        the next iteration.  When set, all waiting threads are interrupted (see
        :py:meth:`sleep`).
        
        Thread-safe since pyglet 1.2.
    
        :see: `exit`
        :type: bool
        """
        ...
    
    @has_exit.setter
    def has_exit(self, value): # -> None:
        ...
    
    def exit(self): # -> None:
        """Safely exit the event loop at the end of the current iteration.

        This method is a thread-safe equivalent for setting
        :py:attr:`has_exit` to ``True``.  All waiting threads will be
        interrupted (see :py:meth:`sleep`).
        """
        ...
    
    def sleep(self, timeout): # -> bool:
        """Wait for some amount of time, or until the :py:attr:`has_exit` flag
        is set or :py:meth:`exit` is called.

        This method is thread-safe.

        :Parameters:
            `timeout` : float
                Time to wait, in seconds.

        .. versionadded:: 1.2

        :rtype: bool
        :return: ``True`` if the `has_exit` flag is set, otherwise ``False``.
        """
        ...
    
    def on_window_close(self, window): # -> None:
        """Default window close handler."""
        ...
    
    if _is_pyglet_doc_run:
        def on_window_close(self, window): # -> None:
            """A window was closed.

            This event is dispatched when a window is closed.  It is not
            dispatched if the window's close button was pressed but the
            window did not close.

            The default handler calls :py:meth:`exit` if no more windows are
            open.  You can override this handler to base your application exit
            on some other policy.

            :event:
            """
            ...
        
        def on_enter(self): # -> None:
            """The event loop is about to begin.

            This is dispatched when the event loop is prepared to enter
            the main run loop, and represents the last chance for an
            application to initialise itself.

            :event:
            """
            ...
        
        def on_exit(self): # -> None:
            """The event loop is about to exit.

            After dispatching this event, the :py:meth:`run` method returns (the
            application may not actually exit if you have more code
            following the :py:meth:`run` invocation).

            :event:
            """
            ...
        

