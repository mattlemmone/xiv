import process
import ffxiv
from memory import MemoryWatch
from player import Player


def initialize_ffxiv_data():
    ffxiv.hwnd = process.get_hwnd(window_name=ffxiv.window_name)
    ffxiv.pid = process.get_pid(process_name=ffxiv.process_name)
    ffxiv.py_handle = process.get_handle(pid=ffxiv.pid)
    ffxiv.base_address = process.get_base_address(pid=ffxiv.pid)


def create_registry_singletons():
    # Everything here will be registered to MemoryWatch
    Player()


def main():
    initialize_ffxiv_data()

    mem_watch = MemoryWatch(application=ffxiv)
    mem_watch.find_all_pointers()

    # Must create singletons after pointers are found
    create_registry_singletons()
    mem_watch.start(poll_rate=1)


if __name__ == "__main__":
    main()
