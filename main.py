from threading import Thread
import logging

from lib.memory import MemoryWatch
from core.player import Player
from lib import client
from lib import process
from core.script_manager import ScriptManager

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


def main():
    initialize_client_data()

    mem_watch = MemoryWatch(poll_rate=200)
    mem_watch.find_multi_level_pointers()

    # Must create singletons after pointers are found
    create_registry_singletons()

    # Start memory watch thread
    mem_watch.start()

    # Execute scripts
    script_manager = ScriptManager()
    script_manager.run_all()


if __name__ == "__main__":
    main_thread = Thread(target=main)
    main_thread.daemon = True
    main_thread.start()

    while True:
        pass
