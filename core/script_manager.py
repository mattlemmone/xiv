import abc
import logging
import os
import importlib

from core.error import ScriptManagerException
from core.error import ScriptDesignException

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCRIPT_PATH = 'scripts'
SCRIPT_CLASS = 'Script'
APPROVED_SCRIPT_EXTN = frozenset(['.py'])
BLACKLISTED_FILES = frozenset(['__init__.py'])


class BaseScript(object):
    """
    All scripts should inherit this type!
    """
    __metaclass__ = abc.ABCMeta
    script_active = True

    @abc.abstractmethod
    def run(self):
        pass


class ScriptManager(object):

    def __init__(self):
        self.files = frozenset(_get_all_script_files())
        self.current_script = None

    def run_one(self, file_name, loop=False):
        if file_name not in self.files:
            raise ScriptManagerException(
                '%s could not be found' % file_name
            )

        while True:
            self.current_script = self._load_script(file_name)

            if self.current_script.script_active:
                self.current_script.run()
            else:
                logger.debug('Script %s is not active, skipping...', file_name)

            if not loop:
                break

    def run_all(self, loop=False):
        for file in self.files:
            self.run_one(file, loop)

    def _load_script(self, file_name):
        module_path = '%s.%s' % (SCRIPT_PATH, file_name)
        module = importlib.import_module(module_path)
        script = module.Script

        _verify_script(script)

        return script


def _verify_script(script):
    script_name = script.__module__

    if not issubclass(script, BaseScript):
        raise ScriptDesignException(
            'Script in %s must inherit from BaseScript' % script_name
        )

    if not callable(script.run):
        raise ScriptDesignException(
            'Script in %s requires "run" to be a method' % script_name
        )

    if hasattr(script.run, '__isabstractmethod__'):
        raise ScriptDesignException(
            'Script in %s requires a "run" method' % script_name
        )


def _get_all_script_files():
    """
    Return array of all scripts in scripts dir
    """
    scripts = []
    for file_name in os.listdir(SCRIPT_PATH):
        file_path = os.path.join(SCRIPT_PATH, file_name)
        file_extn = os.path.splitext(file_path)[-1]

        if os.path.isfile(file_path) and file_extn in APPROVED_SCRIPT_EXTN:
            if file_name in BLACKLISTED_FILES:
                continue

            trimmed_file_name = file_name[:-len(file_extn)]
            scripts.append(trimmed_file_name)

    return scripts
