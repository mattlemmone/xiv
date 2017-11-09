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

from core.pointers import multi_level_pointers
from core.pointers import single_level_pointers
from core.registry_entries import RegistryEntry
from lib import application
from lib.singleton import Singleton

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

k32 = ctypes.WinDLL('kernel32', use_last_error=True)

# RPM
ReadProcessMemory = k32.ReadProcessMemory
ReadProcessMemory.argtypes = [
    HANDLE, LPCVOID, LPVOID, ctypes.c_size_t, POINTER(ctypes.c_size_t)
]
ReadProcessMemory.restype = BOOL
# End RPM

# WPM
WriteProcessMemory = k32.WriteProcessMemory
WriteProcessMemory.argtypes = [
    HANDLE, LPVOID, LPCVOID, ctypes.c_size_t, POINTER(ctypes.c_size_t)
]
WriteProcessMemory.restype = BOOL
# End WPM

GetLastError = k32.GetLastError
GetLastError.argtypes = None
GetLastError.restype = DWORD

# Milliseconds
DEFAULT_POLL_RATE = 100


class MemoryWatch(Thread):
    __metaclass__ = Singleton
    _registry = defaultdict(list)

    def __init__(self, poll_rate):
        self.poll_rate = poll_rate
        Thread.__init__(self)
        self.daemon = True

    def resolve_all_pointers(self):
        _resolve_multi_level_pointers()
        _resolve_single_level_pointers()

    @classmethod
    def register(cls, registry_entry):
        reference = registry_entry.reference
        class_name = reference.__class__.__name__

        assert isinstance(registry_entry, RegistryEntry)
        # logger.debug(
        #     "%s: registering %s%r",
        #     cls.__name__, class_name, registry_entry.attribute_path
        # )
        cls._registry[reference.address].append(registry_entry)

    @classmethod
    def unregister_by_address(cls, address):
        cls._registry.pop(address, None)

    def run(self, poll_rate=DEFAULT_POLL_RATE):
        """
        Reads items from registry, updates them via reference, sleeps, repeats
        """
        logger.debug('memwatch started')
        while True:
            for address, registry_entry_list in MemoryWatch._registry.items():
                for entry in registry_entry_list:
                    new_value = read_address(entry.address, entry.data_type)
                    _reference_update(
                        entry.reference, entry.attribute_path, new_value
                    )
            #         logger.debug('Updated {:22s} {:29s} --> {:15s}'.format(
            #             entry.description, entry.attribute_path, str(new_value)
            #         ))
            # logger.debug('-' * 40)
            time.sleep(poll_rate / 1000)


def _resolve_multi_level_pointers():
    """
    Updates/resolves all pointer addresses so they can be referenced for
    immediate memory reads
    """
    logger.debug("Finding multi-level pointers...")
    for name, pointer in multi_level_pointers.items():
        logger.debug("Resolving %s pointer @ %s...", name, pointer.offsets)
        pointer.address = read_address_pointers(
            application.base_address,
            pointer.offsets,
        )

        assert pointer.address, 'Error resolving multi lvl pointer %s!' % name


def _resolve_single_level_pointers():
    """
    Updates/resolves all pointer addresses so they can be referenced for
    immediate memory reads
    """
    logger.debug("Finding single-level pointers...")
    for name, pointer in single_level_pointers.items():
        logger.debug("Resolving %s pointer @ %s...", name, pointer.offsets)
        assert len(pointer.offsets) == 1, 'Static pointers must have one offset'

        pointer.address = application.base_address + pointer.offsets[0]
        assert pointer.address, 'Error resolving single lvl pointer %s!' % name


def _reference_update(reference, attribute_path, new_value):
    # Update reference attributes
    attr = attribute_path[0]
    if len(attribute_path) > 1:
        cloned_path = list(attribute_path[1:])

        if not isinstance(reference, list):
            next_ref = getattr(reference, attr)
        else:
            next_ref = reference[int(attr)]

        _reference_update(
            next_ref, cloned_path, new_value
        )
    else:
        if getattr(reference, attr) != new_value:
            setattr(reference, attr, new_value)


def read_address(address, data_buffer):
    handle_id = application.py_handle.handle
    bytes_read = ctypes.c_ulonglong()
    success = ReadProcessMemory(
        handle_id, address,
        ctypes.byref(data_buffer), ctypes.sizeof(data_buffer), ctypes.byref(bytes_read)
    )
    error = GetLastError()
    assert success, 'Failed to read address %s, error code %d' % (
        hex(address), error
    )
    return data_buffer.value


def write_address(address, data_buffer):
    handle_id = application.py_handle.handle
    bytes_written = ctypes.c_ulonglong()
    success = WriteProcessMemory(
        handle_id, address,
        ctypes.byref(data_buffer), ctypes.sizeof(data_buffer), bytes_written
    )
    error = GetLastError()
    assert success, 'Failed to write address %s, error code %d' % (
        hex(address), error
    )
    return success


def read_address_pointers(base_address, offsets):
    """
    Return final address pointer from list of pointer offsets
    """
    temp_buffer = ctypes.c_ulonglong()
    address = base_address + offsets[0]
    result = read_address(address, temp_buffer)
    output = '1) %s' % hex(result)

    for idx, offset in enumerate(offsets):
        if not idx:
            continue
        result = read_address(result + offset, temp_buffer)
        output = '%s -> %d) %s' % (output, idx + 1, hex(result))
    logger.debug(output)
    logger.debug("Resolved --> %s", hex(result))
    return result
