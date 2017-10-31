import process
import ffxiv
from memory import MemoryWatch


def initialize_ffxiv_data():
    ffxiv.hwnd = process.get_hwnd(ffxiv.window_name)
    ffxiv.pid = process.get_pid(ffxiv.process_name)
    ffxiv.py_handle = process.get_handle(ffxiv.pid)
    ffxiv.base_address = process.get_base_address(ffxiv.pid)


def main():
    initialize_ffxiv_data()
    mem_watch = MemoryWatch(ffxiv)
    mem_watch.find_all_pointers()


if __name__ == "__main__":
    main()
