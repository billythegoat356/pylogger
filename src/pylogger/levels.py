from pydantic import BaseModel

from .colors import ColorCombo, Colors
from .styles import LevelsColors



"""
Levels models and default levels
----------------
You can create your own levels by creating a LevelModel instance
"""


class LevelModel(BaseModel):
    name: str
    color: ColorCombo
    value: int


    def __call__(self):
        return self.format()
    
    def format(self) -> str:
        "Colorizes the level and returns it as a string"
        return self.color.colorize(text=self.name)
    

    def __lt__(self, other: 'LevelModel') -> bool:
        if isinstance(other, LevelModel):
            return self.value < other.value
        return NotImplemented
    
    def __le__(self, other: 'LevelModel') -> bool:
        if isinstance(other, LevelModel):
            return self.value <= other.value
        return NotImplemented
    
    def __gt__(self, other: 'LevelModel') -> bool:
        if isinstance(other, LevelModel):
            return self.value > other.value
        return NotImplemented
    
    def __ge__(self, other: 'LevelModel') -> bool:
        if isinstance(other, LevelModel):
            return self.value >= other.value
        return NotImplemented
    
    def __eq__(self, other: 'LevelModel') -> bool:
        if isinstance(other, LevelModel):
            return self.value == other.value
        return NotImplemented
    
    def __ne__(self, other: 'LevelModel') -> bool:
        if isinstance(other, LevelModel):
            return self.value != other.value
        return NotImplemented



class Levels:
    DEBUG = LevelModel(name="DEBUG", color=LevelsColors.debug, value=0)
    INFO = LevelModel(name="INFO", color=LevelsColors.info, value=1)
    WARNING = LevelModel(name="WARNING", color=LevelsColors.warning, value=2)
    ERROR = LevelModel(name="ERROR", color=LevelsColors.error, value=3)
    FATAL = LevelModel(name="FATAL", color=LevelsColors.fatal, value=4)

