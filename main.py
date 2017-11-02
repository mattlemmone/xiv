from memory import MemoryWatch
from player import Player
import client
import process


def initialize_client_data():
    client.hwnd = process.get_hwnd(window_name=client.window_name)
    client.pid = process.get_pid(process_name=client.process_name)
    client.py_handle = process.get_handle(pid=client.pid)
    client.base_address = process.get_base_address(pid=client.pid)


def create_registry_singletons():
    # Everything here will be registered to MemoryWatch
    Player()


def main():
    initialize_client_data()

    mem_watch = MemoryWatch()
    mem_watch.find_base_pointers()

    # Must create singletons after pointers are found
    create_registry_singletons()
    mem_watch.start(poll_rate=1)


if __name__ == "__main__":
    main()
