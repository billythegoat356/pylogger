from typing import Optional

from datetime import datetime
import inspect
from pathlib import Path

from .config import Config
from .styles import FormatColors as FS, Separators as Seps
from .levels import LevelModel



"""
Class taking care of formatting the log messages
Uses the styles defined in the styles module
----------------
The formatting is NOT customizable, only the styles are
"""



# Dynamically get the module directory name
THIS_MODULE_PATH = Path(__file__).parent
THIS_MODULE_NAME = THIS_MODULE_PATH.name



class Formatting:

    @classmethod
    def format(cls, message: str, level: LevelModel, prefix: Optional[str] = None) -> str:
        """
        Formats the message with the given level

        Parameters:
            message (str): the message to format
            level (Level): the level of the message

        Returns:
            str - the formatted message
        """
        # Get values
        time, date = cls.format_time_and_date()
        path, lineno = cls.format_file_info()

        # Build formatted message
        formatted_message = ""

        if prefix is not None:
            formatted_message += prefix + FS.separator.colorize(Seps.prefix_time)
        
        formatted_time = FS.time.colorize(text=time)
        formatted_date = FS.date.colorize(text=date)
        formatted_path = FS.path.colorize(text=path)
        formatted_lineno = FS.lineno.colorize(text=lineno)

        formatted_level = level.format()

        formatted_message += (
            formatted_time \
            + FS.separator.colorize(Seps.time_date) \
            + formatted_date \
            + FS.separator.colorize(Seps.date_path) \
            + formatted_path \
            + FS.separator.colorize(Seps.path_lineno) \
            + formatted_lineno \
            + FS.separator.colorize(Seps.lineno_level) \
            + formatted_level \
            + FS.separator.colorize(Seps.level_message) \
            + message
        )

        return formatted_message
    
    @classmethod
    def raw_format(cls, message: str, level: LevelModel, prefix: Optional[str] = None) -> str:
        """
        Formats the message with the given level, without any color

        Parameters:
            message (str): the message to format
            level (Level): the level of the message

        Returns:
            str - the formatted message
        """
        # Get values
        time, date = cls.format_time_and_date()
        path, lineno = cls.format_file_info()

        # Build formatted message
        formatted_message = ""

        if prefix is not None:
            formatted_message += prefix + Seps.prefix_time
        
        formatted_message = (
            time \
            + Seps.time_date \
            + date \
            + Seps.date_path \
            + path \
            + Seps.path_lineno \
            + lineno \
            + Seps.lineno_level \
            + level.name \
            + Seps.level_message \
            + message
        )

        return formatted_message
    

    @classmethod
    def format_time_and_date(cls) -> tuple[str, str]:
        """
        Returns a tuple of formatted time and date, in this format:
            13:33:37
            13 Jan 2007

        Returns:
            tuple[str, str] - time and date
        """
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        date = now.strftime("%d %b %Y")
        return time, date
    
    @classmethod
    def format_file_info(cls) -> tuple[str, str]:
        """
        Returns a tuple of the file info:
            file path, (starting from the root of the project)
            lineno in brackets

        Returns:
            tuple[str, str] - file info
        """
        try:
            # Get the current frame's caller
            frame = inspect.currentframe()

            # If frame is unknown
            if frame is None:
                return '<unknown>', '[?]'

            # Go back until we're out of this module
            while Path(frame.f_code.co_filename).parent.name == THIS_MODULE_NAME:
                frame = frame.f_back
            
            # Get the formatted relative file path
            file_path = frame.f_code.co_filename

            # Handle special cases like '<stdin>' from interactive shell
            if file_path == '<stdin>' or not Path(file_path).exists():
                return str(file_path), f'[{frame.f_lineno}]'
        
            # Get the formatted relative file path
            try:
                rel_file_path = Path(file_path).relative_to(Config.ROOT_PATH)
                f_file_path = '/'.join(rel_file_path.parts)
            except ValueError:
                # If we can't make it relative to ROOT_PATH, just use the full path
                f_file_path = str(Path(file_path))

            # Get and format the line number
            lineno = f'[{frame.f_lineno}]'

            return f_file_path, lineno
        finally:
            # Reference cycle prevention
            del frame




