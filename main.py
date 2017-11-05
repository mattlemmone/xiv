from threading import Thread
import logging

from lib.memory import MemoryWatch
from core.player import Player
from lib import application
from lib import process
from core.script_manager import ScriptManager

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def initialize_application_data():
    application.hwnd = process.get_hwnd(window_name=application.window_name)
    application.pid = process.get_pid(process_name=application.process_name)
    application.py_handle = process.get_handle(pid=application.pid)
    application.base_address = process.get_base_address(pid=application.pid)


def create_registry_singletons():
    # Everything here will be registered to MemoryWatch
    Player()


def main():
    initialize_application_data()

    mem_watch = MemoryWatch(poll_rate=100)
    mem_watch.resolve_all_pointers()

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
