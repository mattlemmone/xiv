import ctypes
from ctypes.wintypes import LPCVOID
from ctypes.wintypes import LPVOID
from ctypes.wintypes import HANDLE
from ctypes.wintypes import POINTER
from ctypes.wintypes import BOOL
from ctypes.wintypes import DWORD
from pointers import all_pointers
from singleton import Singleton


# Ctype RPM constants
k32 = ctypes.WinDLL('kernel32', use_last_error=True)

ReadProcessMemory = k32.ReadProcessMemory
ReadProcessMemory.argtypes = [
    HANDLE, LPCVOID, LPVOID, ctypes.c_size_t, POINTER(ctypes.c_size_t)
]
ReadProcessMemory.restype = BOOL

GetLastError = k32.GetLastError
GetLastError.argtypes = None
GetLastError.restype = DWORD
# end Ctype RPM constants

DEFAULT_POLL_RATE = 1


class RegistryEntry(object):
    def __init__(self, reference, attribute_path, address, offset, data_type):
        self.reference = reference
        self.attribute_path = attribute_path
        self.address = address + offset
        self.data_type = data_type

    def register(self):
        MemoryWatch.register(self)


class MemoryWatch(object):
    __metaclass__ = Singleton
    _registry = []

    def __init__(self, application):
        self.application = application

    def find_all_pointers(self):
        """
        Updates/resolves all pointer addresses so they can be referenced for
        immediate memory reads
        """
        print "Finding pointers..."
        for name, pointer in all_pointers.items():
            print "Resolving %s pointer @ %s..." % (name, pointer.offsets)
            pointer.address = read_address_pointers(
                self.application.py_handle.handle,
                self.application.base_address,
                pointer.offsets,
            )

    @classmethod
    def register(cls, registry_entry):
        reference = registry_entry.reference
        class_name = reference.__class__.__name__

        assert(isinstance(registry_entry, RegistryEntry))
        print "%s: registering %s%r" % (
            cls.__name__, class_name, registry_entry.attribute_path
        )
        cls._registry.append(registry_entry)

    def start(self, poll_rate=DEFAULT_POLL_RATE):
        """
        Reads items from registry, updates them via reference, sleeps, repeats
        """
        while True:
            print '-' * 40
            for entry in self._registry:
                new_value = read_address(
                    self.application.py_handle.handle, entry.address, entry.data_type
                )
                _reference_update(
                    entry.reference.__dict__, entry.attribute_path, new_value
                )
                print 'Updated %s --> %s' % (entry.attribute_path, str(new_value))

            import time
            time.sleep(poll_rate)


def _reference_update(reference_dict, attribute_path, new_value):
    # Very sneaky way of updating an instance reference via __dict__ and nested keys
    attr = attribute_path[0]
    if isinstance(reference_dict[attr], dict):
        cloned_path = list(attribute_path[1:])
        _reference_update(
            reference_dict[attr], cloned_path, new_value
        )
    else:
        reference_dict[attr] = new_value


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
    output = '1) %s' % hex(result)

    for idx, offset in enumerate(offsets):
        if not idx:
            continue
        result = read_address(handle_id, result + offset, temp_buffer)
        output = '%s -> %d) %s' % (output, idx + 1, hex(result))
    print output
    print "Resolved --> %s" % hex(result)
    return result
