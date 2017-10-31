import ctypes
from ctypes.wintypes import LPCVOID
from ctypes.wintypes import LPVOID
from ctypes.wintypes import HANDLE
from ctypes.wintypes import POINTER
from ctypes.wintypes import BOOL
from ctypes.wintypes import DWORD
from pointers import all_pointers
from singleton import Singleton

k32 = ctypes.WinDLL('kernel32', use_last_error=True)

ReadProcessMemory = k32.ReadProcessMemory
ReadProcessMemory.argtypes = [
    HANDLE, LPCVOID, LPVOID, ctypes.c_size_t, POINTER(ctypes.c_size_t)
]
ReadProcessMemory.restype = BOOL

GetLastError = k32.GetLastError
GetLastError.argtypes = None
GetLastError.restype = DWORD


class MemoryWatch(object):
    __metaclass__ = Singleton

    def __init__(self, application):
        self.application = application
        self.registry = []
        self.POLL_RATE = 500

    def find_all_pointers(self):
        """
        Updates/resolves all pointer addresses so they can be referenced for
        immediate memory reads
        """
        for name, pointer in all_pointers.items():
            pointer.address = read_address_pointers(
                self.application.py_handle.handle,
                self.application.base_address,
                pointer.offsets,
            )

    def register(self, registry_entry):
        self.registry.append(registry_entry)

    def scan_for_updates(self):
        """
        1. read item from registry
        2. update item via reference
        3. sleep after updating all items for POLL_RATE
        """
        pass


def read_address(handle_id, address, data_buffer):
    bytesRead = ctypes.c_ulonglong()
    success = ReadProcessMemory(
        handle_id, address,
        ctypes.byref(data_buffer), ctypes.sizeof(data_buffer), ctypes.byref(bytesRead)
    )
    error = GetLastError()
    assert(success)
    return data_buffer.value


def read_address_pointers(handle_id, base_address, offsets):
    """
    Return final address pointer from list of pointer offsets
    """
    temp_buffer = ctypes.c_ulonglong()
    address = base_address + offsets[0]
    result = read_address(handle_id, address, temp_buffer)

    for idx, offset in enumerate(offsets):
        if not idx:
            continue

        result = read_address(handle_id, result + offset, temp_buffer)

    return result
