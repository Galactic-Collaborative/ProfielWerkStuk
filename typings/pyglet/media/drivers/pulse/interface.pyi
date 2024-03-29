"""
This type stub file was generated by pyright.
"""

import pyglet
from pyglet.media.exceptions import MediaException

_debug = ...
def get_uint32_or_none(value): # -> None:
    ...

def get_bool_or_none(value): # -> bool | None:
    ...

def get_ascii_str_or_none(value): # -> None:
    ...

class PulseAudioException(MediaException):
    def __init__(self, error_code, message) -> None:
        ...
    
    def __str__(self) -> str:
        ...
    
    __repr__ = ...


class PulseAudioMainLoop:
    def __init__(self) -> None:
        ...
    
    def __del__(self): # -> None:
        ...
    
    def start(self): # -> None:
        """Start running the mainloop."""
        ...
    
    def delete(self): # -> None:
        """Clean up the mainloop."""
        ...
    
    def lock(self): # -> None:
        """Lock the threaded mainloop against events.  Required for all
        calls into PA."""
        ...
    
    def unlock(self): # -> None:
        """Unlock the mainloop thread."""
        ...
    
    def signal(self): # -> None:
        """Signal the mainloop thread to break from a wait."""
        ...
    
    def wait(self): # -> None:
        """Wait for a signal."""
        ...
    
    def create_context(self): # -> PulseAudioContext:
        ...
    
    def __enter__(self): # -> None:
        ...
    
    def __exit__(self, exc_type, exc_value, traceback): # -> None:
        ...
    


class PulseAudioLockable:
    def __init__(self, mainloop) -> None:
        ...
    
    def lock(self): # -> None:
        """Lock the threaded mainloop against events.  Required for all
        calls into PA."""
        ...
    
    def unlock(self): # -> None:
        """Unlock the mainloop thread."""
        ...
    
    def signal(self): # -> None:
        """Signal the mainloop thread to break from a wait."""
        ...
    
    def wait(self): # -> None:
        """Wait for a signal."""
        ...
    
    def __enter__(self): # -> None:
        ...
    
    def __exit__(self, exc_type, exc_value, traceback): # -> None:
        ...
    


class PulseAudioContext(PulseAudioLockable):
    """Basic object for a connection to a PulseAudio server."""
    _state_name = ...
    def __init__(self, mainloop, pa_context) -> None:
        ...
    
    def __del__(self): # -> None:
        ...
    
    def delete(self): # -> None:
        """Completely shut down pulseaudio client."""
        ...
    
    @property
    def is_ready(self):
        ...
    
    @property
    def is_failed(self):
        ...
    
    @property
    def is_terminated(self):
        ...
    
    @property
    def server(self): # -> None:
        ...
    
    @property
    def protocol_version(self): # -> None:
        ...
    
    @property
    def server_protocol_version(self): # -> None:
        ...
    
    @property
    def is_local(self): # -> bool | None:
        ...
    
    def connect(self, server=...): # -> None:
        """Connect the context to a PulseAudio server.

        :Parameters:
            `server` : str
                Server to connect to, or ``None`` for the default local
                server (which may be spawned as a daemon if no server is
                found).
        """
        ...
    
    def create_stream(self, audio_format): # -> PulseAudioStream:
        """
        Create a new audio stream.
        """
        ...
    
    def create_sample_spec(self, audio_format): # -> pa_sample_spec:
        """
        Create a PulseAudio sample spec from pyglet audio format.
        """
        ...
    
    def set_input_volume(self, stream, volume): # -> PulseAudioOperation:
        """
        Set the volume for a stream.
        """
        ...
    
    def check(self, result):
        ...
    
    def check_not_null(self, value):
        ...
    
    def check_ptr_not_null(self, value):
        ...
    
    def raise_error(self):
        ...
    


class PulseAudioStream(PulseAudioLockable, pyglet.event.EventDispatcher):
    """PulseAudio audio stream."""
    _state_name = ...
    def __init__(self, mainloop, context, pa_stream) -> None:
        ...
    
    def __del__(self): # -> None:
        ...
    
    def delete(self): # -> None:
        ...
    
    @property
    def is_unconnected(self):
        ...
    
    @property
    def is_creating(self):
        ...
    
    @property
    def is_ready(self):
        ...
    
    @property
    def is_failed(self):
        ...
    
    @property
    def is_terminated(self):
        ...
    
    @property
    def writable_size(self):
        ...
    
    @property
    def index(self):
        ...
    
    @property
    def is_corked(self): # -> bool | None:
        ...
    
    @property
    def audio_format(self):
        ...
    
    def connect_playback(self): # -> None:
        ...
    
    def write(self, audio_data, length=..., seek_mode=...):
        ...
    
    def update_timing_info(self, callback=...): # -> PulseAudioOperation:
        ...
    
    def get_timing_info(self):
        ...
    
    def trigger(self, callback=...): # -> PulseAudioOperation:
        ...
    
    def prebuf(self, callback=...): # -> PulseAudioOperation:
        ...
    
    def resume(self, callback=...): # -> PulseAudioOperation:
        ...
    
    def pause(self, callback=...): # -> PulseAudioOperation:
        ...
    
    def update_sample_rate(self, sample_rate, callback=...): # -> PulseAudioOperation:
        ...
    
    def on_write_needed(self, nbytes, underflow): # -> None:
        """A write is requested from PulseAudio.
        Called from the PulseAudio mainloop, so no locking required.

        :event:
        """
        ...
    


class PulseAudioOperation(PulseAudioLockable):
    """Asynchronous PulseAudio operation"""
    _state_name = ...
    def __init__(self, context, callback=..., pa_operation=..., succes_cb_t=...) -> None:
        ...
    
    def __del__(self): # -> None:
        ...
    
    def delete(self): # -> None:
        ...
    
    def execute(self, pa_operation): # -> Self@PulseAudioOperation:
        ...
    
    def cancel(self): # -> Self@PulseAudioOperation:
        ...
    
    @property
    def is_running(self):
        ...
    
    @property
    def is_done(self):
        ...
    
    @property
    def is_cancelled(self):
        ...
    
    def wait(self): # -> Self@PulseAudioOperation:
        """Wait until operation is either done or cancelled."""
        ...
    


