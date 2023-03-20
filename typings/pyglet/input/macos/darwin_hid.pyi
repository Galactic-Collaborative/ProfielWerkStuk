"""
This type stub file was generated by pyright.
"""

import sys
from ctypes import c_int, c_uint32
from pyglet.event import EventDispatcher
from pyglet.input.base import ControllerManager, Device

__LP64__ = (sys.maxsize > 2 ** 32)
iokit = ...
kIOHIDOptionsTypeNone = ...
kIOHIDOptionsTypeSeizeDevice = ...
kIOHIDElementTypeInput_Misc = ...
kIOHIDElementTypeInput_Button = ...
kIOHIDElementTypeInput_Axis = ...
kIOHIDElementTypeInput_ScanCodes = ...
kIOHIDElementTypeOutput = ...
kIOHIDElementTypeFeature = ...
kIOHIDElementTypeCollection = ...
kHIDPage_GenericDesktop = ...
kHIDPage_Consumer = ...
kHIDUsage_GD_SystemSleep = ...
kHIDUsage_GD_SystemWakeUp = ...
kHIDUsage_GD_SystemAppMenu = ...
kHIDUsage_GD_SystemMenu = ...
kHIDUsage_GD_SystemMenuRight = ...
kHIDUsage_GD_SystemMenuLeft = ...
kHIDUsage_GD_SystemMenuUp = ...
kHIDUsage_GD_SystemMenuDown = ...
kHIDUsage_Csmr_Menu = ...
kHIDUsage_Csmr_FastForward = ...
kHIDUsage_Csmr_Rewind = ...
kHIDUsage_Csmr_Eject = ...
kHIDUsage_Csmr_Mute = ...
kHIDUsage_Csmr_VolumeIncrement = ...
kHIDUsage_Csmr_VolumeDecrement = ...
IOReturn = c_int
IOOptionBits = c_uint32
IOHIDElementType = c_int
IOHIDElementCollectionType = c_int
IOHIDElementCookie = ...
HIDManagerCallback = ...
HIDDeviceCallback = ...
HIDDeviceValueCallback = ...
_device_lookup = ...
class HIDValue:
    def __init__(self, value_ref) -> None:
        ...
    


class HIDDevice:
    @classmethod
    def get_device(cls, device_ref): # -> HIDDevice:
        ...
    
    def __init__(self, device_ref) -> None:
        ...
    
    def get_guid(self): # -> str:
        """Generate an SDL2 style GUID from the product guid."""
        ...
    
    def get_property(self, name): # -> str | int | float | c_void_p | None:
        ...
    
    def open(self, exclusive_mode=...): # -> bool:
        ...
    
    def close(self): # -> bool:
        ...
    
    def schedule_with_run_loop(self): # -> None:
        ...
    
    def unschedule_from_run_loop(self): # -> None:
        ...
    
    def conforms_to(self, page, usage): # -> bool:
        ...
    
    def is_pointer(self): # -> bool:
        ...
    
    def is_mouse(self): # -> bool:
        ...
    
    def is_joystick(self): # -> bool:
        ...
    
    def is_gamepad(self): # -> bool:
        ...
    
    def is_keyboard(self): # -> bool:
        ...
    
    def is_keypad(self): # -> bool:
        ...
    
    def is_multi_axis(self): # -> bool:
        ...
    
    def py_value_callback(self, context, result, sender, value): # -> None:
        ...
    
    def add_value_observer(self, observer): # -> None:
        ...
    
    def get_value(self, element): # -> HIDValue | None:
        ...
    
    def __repr__(self): # -> str:
        ...
    


class HIDDeviceElement:
    @classmethod
    def get_element(cls, element_ref): # -> HIDDeviceElement:
        ...
    
    def __init__(self, element_ref) -> None:
        ...
    


class HIDManager(EventDispatcher):
    def __init__(self) -> None:
        """Create an instance of an HIDManager."""
        ...
    
    def open(self): # -> None:
        ...
    
    def close(self): # -> None:
        ...
    
    def schedule_with_run_loop(self): # -> None:
        ...
    
    def unschedule_from_run_loop(self): # -> None:
        ...
    


_axis_names = ...
_button_names = ...
class PygletDevice(Device):
    def __init__(self, display, device) -> None:
        ...
    
    def open(self, window=..., exclusive=...): # -> None:
        ...
    
    def close(self): # -> None:
        ...
    
    def get_controls(self): # -> list[Unknown]:
        ...
    
    def get_guid(self):
        ...
    
    def device_value_changed(self, hid_device, hid_value): # -> None:
        ...
    
    def __repr__(self): # -> str:
        ...
    


_hid_manager = ...
class DarwinControllerManager(ControllerManager):
    def __init__(self, display=...) -> None:
        ...
    
    def get_controllers(self): # -> list[Unknown]:
        ...
    


def get_devices(display=...): # -> list[PygletDevice]:
    ...

def get_joysticks(display=...): # -> list[Joystick]:
    ...

def get_apple_remote(display=...): # -> AppleRemote | None:
    ...

def get_controllers(display=...): # -> list[Controller]:
    ...

