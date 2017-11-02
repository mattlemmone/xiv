import logging
from threading import Thread

from memory import MemoryWatch
from player import Player
import client
import process

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def initialize_client_data():
    client.hwnd = process.get_hwnd(window_name=client.window_name)
    client.pid = process.get_pid(process_name=client.process_name)
    client.py_handle = process.get_handle(pid=client.pid)
    client.base_address = process.get_base_address(pid=client.pid)


def create_registry_singletons():
    # Everything here will be registered to MemoryWatch
    Player()


def execute_scripts():
    while True:
        logger.debug('execute_scripts')


def main():
    initialize_client_data()

    mem_watch = MemoryWatch(poll_rate=1)
    mem_watch.find_base_pointers()

    # Must create singletons after pointers are found
    create_registry_singletons()
    mem_watch.start()
    # execute_scripts()


if __name__ == "__main__":
    main_thread = Thread(target=main)
    main_thread.daemon = True
    main_thread.start()

    while True:
        pass
