import threading
import sys
from typing import Optional

from pathlib import Path

from .config import Config
from .format import Formatting
from .levels import LevelModel, Levels



"""
Logging classes
----------------
Logger: allows direct logging
PrefixLogger: allows logging with a preset prefix, and a custom file (instance-based)
----------------
You are free to write your own wrapper logging classes, inheriting from the following
"""



"Direct logging class"
class Logger:
    # Prevents multiple threads concurrencing
    _stdout_lock = threading.Lock()
    _file_lock = threading.Lock()

    @classmethod
    def log(cls, message: str, level: LevelModel, prefix: Optional[str] = None) -> str | None:
        """
        Logs the message with the given level and prefix (if the minimum level threshold is met)
        
        Parameters:
            message (str): the message to log
            level (LevelModel): the level of the message
            prefix (Optional[str]): the prefix to include in the message

        Returns:
            str | None - the raw formatted message, if the level threshold is met
        """
        # If the level threshold is not met, simply return
        if level < Config.MIN_LEVEL:
            return
        
        formatted_message = Formatting.format(message=message, level=level, prefix=prefix)
        raw_message = Formatting.raw_format(message=message, level=level, prefix=prefix)

        with cls._stdout_lock:
            sys.stdout.write(formatted_message + "\n")
            sys.stdout.flush()
        
        if Config.LOG_FILE is not None:
            with cls._file_lock:
                with Config.LOG_FILE.open(mode='a') as f:
                    f.write(raw_message + "\n")
        
        return raw_message

    "Logger methods for each level"

    @classmethod
    def debug(cls, message: str, prefix: Optional[str] = None) -> None:
        cls.log(message=message, level=Levels.DEBUG, prefix=prefix)
    
    @classmethod
    def info(cls, message: str, prefix: Optional[str] = None) -> None:
        cls.log(message=message, level=Levels.INFO, prefix=prefix)
    
    @classmethod
    def warning(cls, message: str, prefix: Optional[str] = None) -> None:
        cls.log(message=message, level=Levels.WARNING, prefix=prefix)
    
    @classmethod
    def error(cls, message: str, prefix: Optional[str] = None) -> None:
        cls.log(message=message, level=Levels.ERROR, prefix=prefix)
    
    @classmethod
    def fatal(cls, message: str, prefix: Optional[str] = None) -> None:
        cls.log(message=message, level=Levels.FATAL, prefix=prefix)


"Instance logging, with prefix"
class PrefixLogger(Logger):

    """
    Allows the creation of a logger with a preset prefix
    Basically wraps the log methods to include the instance prefix on each call

    WARNING: The prefix should be already formatted when given
    """

    def __init__(self, prefix: str, log_file: Optional[str | Path] = None) -> None:
        """
        Parameters:
            prefix (str): the formatted prefix to include in the log messages
            log_file (Optional[str | Path]): the path to the log file
        """

        self.prefix: str = prefix

        if isinstance(log_file, str):
            log_file = Path(log_file)
        
        if isinstance(log_file, Path):
            log_file = Config.ROOT_PATH / log_file
        
        self.log_file: Optional[Path] = log_file
        self._file_lock: Optional[threading.Lock] = None

        if log_file is not None:
            self._file_lock = threading.Lock()
    

    def log(self, message: str, level: LevelModel) -> str | None:
        """
        Passes the call to the parent log method with the instance prefix, then logs to the file, if set
        
        Parameters:
            message (str): the message to log
            level (LevelModel): the level of the message
        
        Returns:
            str | None - the raw formatted message, if the level threshold is met
        """
        # If the level threshold is not met, simply return
        if level < Config.MIN_LEVEL:
            return
        
        # Log to terminal and get raw message
        raw_message = super().log(message=message, level=level, prefix=self.prefix)

        # If provided, log to the file
        if self.log_file is not None:
            with self._file_lock:
                with self.log_file.open(mode='a') as f:
                    f.write(raw_message + "\n")
    
    "Logger methods for each level"

    def debug(self, message: str) -> None:
        self.log(message=message, level=Levels.DEBUG)
    
    def info(self, message: str) -> None:
        self.log(message=message, level=Levels.INFO)
    
    def warning(self, message: str) -> None:
        self.log(message=message, level=Levels.WARNING)
    
    def error(self, message: str) -> None:
        self.log(message=message, level=Levels.ERROR)

    def fatal(self, message: str) -> None:
        self.log(message=message, level=Levels.FATAL)
    
