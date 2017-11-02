from collections import defaultdict
from ctypes.wintypes import BOOL
from ctypes.wintypes import DWORD
from ctypes.wintypes import HANDLE
from ctypes.wintypes import LPCVOID
from ctypes.wintypes import LPVOID
from ctypes.wintypes import POINTER
import ctypes
import logging
import time
from threading import Thread

import client
from pointers import base_pointers
from singleton import Singleton

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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

# Milliseconds
DEFAULT_POLL_RATE = 100


class RegistryEntry(object):
    def __init__(
        self, description,
        reference, attribute_path, address, offset, data_type,
        is_lvl1_ptr=False
    ):
        assert address, 'Address must exist in order to create RegistryEntry'
        self.description = description
        self.reference = reference
        self.attribute_path = attribute_path
        self.data_type = data_type
        self.address = address + offset

        # First-level pointers need to be added to process base address
        if is_lvl1_ptr:
            self.address += client.base_address


class MemoryWatch(Thread):
    __metaclass__ = Singleton
    _registry = defaultdict(list)

    def __init__(self, poll_rate):
        self.poll_rate = poll_rate
        Thread.__init__(self)
        self.daemon = True

    def find_base_pointers(self):
        """
        Updates/resolves all pointer addresses so they can be referenced for
        immediate memory reads
        """
        logger.debug("Finding pointers...")
        for name, pointer in base_pointers.items():
            logger.debug("Resolving %s pointer @ %s...", name, pointer.offsets)
            pointer.address = read_address_pointers(
                client.py_handle.handle,
                client.base_address,
                pointer.offsets,
            )

    @classmethod
    def register(cls, registry_entry):
        reference = registry_entry.reference
        class_name = reference.__class__.__name__

        assert isinstance(registry_entry, RegistryEntry)
        logger.debug(
            "%s: registering %s%r",
            cls.__name__, class_name, registry_entry.attribute_path
        )
        cls._registry[reference].append(registry_entry)

    @classmethod
    def unregister_by_ref(cls, reference):
        removed = cls._registry.pop(reference, None)
        assert removed, 'Couldnt remove reference from registry!'

    def run(self, poll_rate=DEFAULT_POLL_RATE):
        """
        Reads items from registry, updates them via reference, sleeps, repeats
        """
        logger.debug('memwatch started')
        handle = client.py_handle.handle
        while True:
            for reference, entry_dict in self._registry.items():
                for entry in entry_dict:
                    new_value = read_address(handle, entry.address, entry.data_type)
                    _reference_update(
                        entry.reference, entry.attribute_path, new_value
                    )
                    # logger.debug('Updated {:22s} {:29s} --> {:15s}'.format(
                    #     entry.description, entry.attribute_path, str(new_value)
                    # ))
            # logger.debug('-' * 40)

            time.sleep(poll_rate / 1000)


def _reference_update(reference, attribute_path, new_value):
    # Update reference attributes
    attr = attribute_path[0]
    if len(attribute_path) > 1:
        cloned_path = list(attribute_path[1:])
        _reference_update(
            getattr(reference, attr), cloned_path, new_value
        )
    else:
        setattr(reference, attr, new_value)


def read_address(handle_id, address, data_buffer):
    bytesRead = ctypes.c_ulonglong()
    success = ReadProcessMemory(
        handle_id, address,
        ctypes.byref(data_buffer), ctypes.sizeof(data_buffer), ctypes.byref(bytesRead)
    )
    error = GetLastError()
    assert success, 'Failed to read address %s, error code %d' % (
        hex(address), error
    )
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
    logger.debug(output)
    logger.debug("Resolved --> %s", hex(result))
    return result
