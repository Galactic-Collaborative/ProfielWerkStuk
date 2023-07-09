"""
This type stub file was generated by pyright.
"""

import ctypes
from ctypes import *
from ctypes.wintypes import *
from . import com

_int_types = ...
if hasattr(ctypes, 'c_int64'):
    ...
class c_void(Structure):
    _fields_ = ...


def POINTER_(obj): # -> Type[_Pointer[Unknown]]:
    ...

c_void_p = ...
INT = ...
UBYTE = c_ubyte
LPVOID = ...
HCURSOR = HANDLE
LRESULT = LPARAM
COLORREF = DWORD
PVOID = c_void_p
WCHAR = ...
BCHAR = c_wchar
LPRECT = ...
LPPOINT = ...
LPMSG = ...
UINT_PTR = HANDLE
LONG_PTR = HANDLE
HDROP = HANDLE
LPTSTR = LPWSTR
LPSTREAM = c_void_p
LF_FACESIZE = ...
CCHDEVICENAME = ...
CCHFORMNAME = ...
WNDPROC = ...
TIMERPROC = ...
TIMERAPCPROC = ...
MONITORENUMPROC = ...
def MAKEINTRESOURCE(i): # -> c_wchar_p:
    ...

class WNDCLASS(Structure):
    _fields_ = ...


class SECURITY_ATTRIBUTES(Structure):
    _fields_ = ...
    __slots__ = ...


class PIXELFORMATDESCRIPTOR(Structure):
    _fields_ = ...


class RGBQUAD(Structure):
    _fields_ = ...
    __slots__ = ...


class CIEXYZ(Structure):
    _fields_ = ...
    __slots__ = ...


class CIEXYZTRIPLE(Structure):
    _fields_ = ...
    __slots__ = ...


class BITMAPINFOHEADER(Structure):
    _fields_ = ...


class BITMAPV5HEADER(Structure):
    _fields_ = ...


class BITMAPINFO(Structure):
    _fields_ = ...
    __slots__ = ...


class LOGFONT(Structure):
    _fields_ = ...


class LOGFONTW(Structure):
    _fields_ = ...


class TRACKMOUSEEVENT(Structure):
    _fields_ = ...
    __slots__ = ...


class MINMAXINFO(Structure):
    _fields_ = ...
    __slots__ = ...


class ABC(Structure):
    _fields_ = ...
    __slots__ = ...


class TEXTMETRIC(Structure):
    _fields_ = ...
    __slots__ = ...


class MONITORINFOEX(Structure):
    _fields_ = ...
    __slots__ = ...


class _DUMMYSTRUCTNAME(Structure):
    _fields_ = ...


class _DUMMYSTRUCTNAME2(Structure):
    _fields_ = ...


class _DUMMYDEVUNION(Union):
    _anonymous_ = ...
    _fields_ = ...


class DEVMODE(Structure):
    _anonymous_ = ...
    _fields_ = ...


class ICONINFO(Structure):
    _fields_ = ...
    __slots__ = ...


class RAWINPUTDEVICE(Structure):
    _fields_ = ...


PCRAWINPUTDEVICE = ...
HRAWINPUT = HANDLE
class RAWINPUTHEADER(Structure):
    _fields_ = ...


class _Buttons(Structure):
    _fields_ = ...


class _U(Union):
    _anonymous_ = ...
    _fields_ = ...


class RAWMOUSE(Structure):
    _anonymous_ = ...
    _fields_ = ...


class RAWKEYBOARD(Structure):
    _fields_ = ...


class RAWHID(Structure):
    _fields_ = ...


class _RAWINPUTDEVICEUNION(Union):
    _fields_ = ...


class RAWINPUT(Structure):
    _fields_ = ...


class _VarTable(Union):
    """Must be in an anonymous union or values will not work across various VT's."""
    _fields_ = ...


class PROPVARIANT(Structure):
    _anonymous_ = ...
    _fields_ = ...


class _VarTableVariant(Union):
    """Must be in an anonymous union or values will not work across various VT's."""
    _fields_ = ...


class VARIANT(Structure):
    _anonymous_ = ...
    _fields_ = ...


class DWM_BLURBEHIND(Structure):
    _fields_ = ...


class STATSTG(Structure):
    _fields_ = ...


class TIMECAPS(Structure):
    _fields_ = ...


class IStream(com.pIUnknown):
    _methods_ = ...


class DEV_BROADCAST_HDR(Structure):
    _fields_ = ...


class DEV_BROADCAST_DEVICEINTERFACE(Structure):
    _fields_ = ...

