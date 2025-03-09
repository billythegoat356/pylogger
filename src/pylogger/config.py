from typing import Optional

import sys, os
from pathlib import Path
import inspect

from .levels import Levels, LevelModel



"""
Logging configuration
----------------
Config class to set the:
    - minimum logging level threshold: this condition will be checked before each logging call
    - log file: the file to log to, if set
    - root path (auto-detected): the root path of the project, used to auto-detect the caller's path. will be set automatically but you can override
"""



class classproperty:
    """Decorator to create a class property."""
    def __init__(self, method):
        self.method = method
        
    def __get__(self, instance, cls):
        return self.method(cls)
    

class Config:
    MIN_LEVEL: LevelModel = Levels.DEBUG
    LOG_FILE: Path | None = None
    _root_path: Path | None = None

    @classmethod
    def set_level(cls, level: LevelModel) -> None:
        """
        Sets the current minimum level

        Parameters:
            level (LevelModel): the level to set as the minimum
        """
        cls.MIN_LEVEL = level

    @classmethod
    def set_log_file(cls, path: str | Path) -> None:
        """
        Sets the log file at the given path

        Parameters:
            path (str | Path): the path to set as the log file
        """
        if isinstance(path, str):
            path = cls.ROOT_PATH / Path(path)
        cls.LOG_FILE = path

    @classproperty
    def ROOT_PATH(cls) -> Path:
        """
        Usage of classproperty to allow the exception to be raised if it is not set
        """
        if cls._root_path is None:
            raise ValueError("Root path not set. Call 'config.set_root_path()' first")
        return cls._root_path

    @classmethod
    def set_root_path(cls, path: Optional[str | Path] = None) -> None:
        """
        Sets the root path at the given path
        If not give, sets it at the current caller frame level

        Parameters:
            path (Optional[str | Path]): the path to set as the root path
        """

        if path is not None:
            if isinstance(path, str):
                path = Path(path)
            cls._root_path = path
            return
        
        try:
            # Get the current frame's caller
            frame = inspect.currentframe()

            # If frame is unknown
            if frame is None:
                raise ValueError("Could not get the current frame")

            # Go one frame back
            frame = frame.f_back

            # Set the root path
            root_path = Path(frame.f_code.co_filename).parent
            cls._root_path = root_path

        finally:
            # Reference cycle prevention
            del frame

    @classmethod
    def _auto_detect_root_path(cls) -> None:
        """
        Helper method to automatically detect the root path
        Uses the main script's directory as the root path if
        possible, otherwise the current working directory
        """
        try:
            # Get the main script path (the entry point of the program)
            main_module = sys.modules['__main__']
            if hasattr(main_module, '__file__'):
                cls._root_path = Path(main_module.__file__).parent
            else:
                # In interactive mode, use current working directory
                cls._root_path = Path(os.getcwd())
        except (AttributeError, KeyError) as e:
            raise ValueError(f"Could not auto-detect root path: {e}")


Config._auto_detect_root_path()