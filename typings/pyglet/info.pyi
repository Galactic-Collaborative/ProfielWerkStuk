"""
This type stub file was generated by pyright.
"""

"""Get environment information useful for debugging.

Intended usage is to create a file for bug reports, e.g.::

    python -m pyglet.info > info.txt

"""
_first_heading = ...
def dump_platform(): # -> None:
    """Dump OS specific """
    ...

def dump_python(): # -> None:
    """Dump Python version and environment to stdout."""
    ...

def dump_pyglet(): # -> None:
    """Dump pyglet version and options."""
    ...

def dump_window(): # -> None:
    """Dump display, window, screen and default config info."""
    ...

def dump_gl(context=...): # -> None:
    """Dump GL info."""
    ...

def dump_glx(): # -> None:
    """Dump GLX info."""
    ...

def dump_media(): # -> None:
    """Dump pyglet.media info."""
    ...

def dump_ffmpeg(): # -> None:
    """Dump FFmpeg info."""
    ...

def dump_al(): # -> None:
    """Dump OpenAL info."""
    ...

def dump_wintab(): # -> None:
    """Dump WinTab info."""
    ...

def dump(): # -> None:
    """Dump all information to stdout."""
    ...

if __name__ == '__main__':
    ...
