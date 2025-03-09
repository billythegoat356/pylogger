from pydantic import BaseModel, Field
from typing import Optional



"""
Colors models and default colors
----------------
You can create your own colors by creating a ColorModel instance
"""


class ColorModel(BaseModel):
    """RGB color model with values between 0-255."""
    r: int = Field(default=255, ge=0, le=255)
    g: int = Field(default=255, ge=0, le=255)
    b: int = Field(default=255, ge=0, le=255)

    def __call__(self, text: str) -> str:
        return self.colorize(text)

    def colorize(self, text: str) -> str:
        """Simply colorize text on the foreground with this color"""
        return f"\033[38;2;{self.r};{self.g};{self.b}m{text}\033[0m"



class ColorCombo(BaseModel):
    """RGB color combo with foreground and background colors, allowing for transparent colors."""

    "Set to None for transparent colors"
    fg: Optional[ColorModel] = None
    bg: Optional[ColorModel] = None


    def __call__(self, text: str) -> str:
        return self.colorize(text)

    def colorize(self, text: str) -> str:
        """Colorize text and handle transparency"""
        result = ""
        
        # Only add colors if they are given
        if self.bg is not None:
            # If BG is given, space around text
            text = f" {text} "
            result += f"\033[48;2;{self.bg.r};{self.bg.g};{self.bg.b}m"
        
        if self.fg is not None:
            result += f"\033[38;2;{self.fg.r};{self.fg.g};{self.fg.b}m"
        
        # Add text and reset
        result += f"{text}\033[0m"
        
        return result


class Colors:
    """Default colors for easy access"""
    # Basic colors
    black = ColorModel(r=0, g=0, b=0)
    white = ColorModel(r=255, g=255, b=255)
    
    # Primary colors
    red = ColorModel(r=255, g=0, b=0)
    green = ColorModel(r=0, g=255, b=0)
    blue = ColorModel(r=0, g=0, b=255)

    # Primary colors - Red with shades
    red = ColorModel(r=255, g=0, b=0)
    dark_red = ColorModel(r=139, g=0, b=0)
    light_red = ColorModel(r=255, g=102, b=102)
    
    # Primary colors - Green with shades
    green = ColorModel(r=0, g=255, b=0)
    dark_green = ColorModel(r=0, g=139, b=0)
    light_green = ColorModel(r=144, g=238, b=144)
    
    # Primary colors - Blue with shades
    blue = ColorModel(r=0, g=0, b=255)
    dark_blue = ColorModel(r=0, g=0, b=139)
    light_blue = ColorModel(r=173, g=216, b=230)
    
    # Secondary colors
    yellow = ColorModel(r=255, g=255, b=0)
    cyan = ColorModel(r=0, g=255, b=255)
    magenta = ColorModel(r=255, g=0, b=255)
    
    # Tertiary colors
    orange = ColorModel(r=255, g=165, b=0)
    chartreuse = ColorModel(r=127, g=255, b=0)
    spring_green = ColorModel(r=0, g=255, b=127)
    azure = ColorModel(r=0, g=127, b=255)
    violet = ColorModel(r=127, g=0, b=255)
    rose = ColorModel(r=255, g=0, b=127)
    
    # Shades of gray
    dark_gray = ColorModel(r=64, g=64, b=64)
    gray = ColorModel(r=128, g=128, b=128)
    light_gray = ColorModel(r=192, g=192, b=192)
    
    # Browns
    brown = ColorModel(r=165, g=42, b=42)
    chocolate = ColorModel(r=210, g=105, b=30)
    tan = ColorModel(r=210, g=180, b=140)
    
    # Blues
    navy = ColorModel(r=0, g=0, b=128)
    royal_blue = ColorModel(r=65, g=105, b=225)
    sky_blue = ColorModel(r=135, g=206, b=235)
    turquoise = ColorModel(r=64, g=224, b=208)
    
    # Reds
    crimson = ColorModel(r=220, g=20, b=60)
    salmon = ColorModel(r=250, g=128, b=114)
    coral = ColorModel(r=255, g=127, b=80)
    
    # Greens
    forest_green = ColorModel(r=34, g=139, b=34)
    lime = ColorModel(r=50, g=205, b=50)
    olive = ColorModel(r=128, g=128, b=0)
    
    # Purples
    indigo = ColorModel(r=75, g=0, b=130)
    purple = ColorModel(r=128, g=0, b=128)
    lavender = ColorModel(r=230, g=230, b=250)
    
    # Pinks
    pink = ColorModel(r=255, g=192, b=203)
    hot_pink = ColorModel(r=255, g=105, b=180)
    deep_pink = ColorModel(r=255, g=20, b=147)
    
    # Yellows
    gold = ColorModel(r=255, g=215, b=0)
    khaki = ColorModel(r=240, g=230, b=140)
    
    # Web colors
    aqua = ColorModel(r=0, g=255, b=255)
    aquamarine = ColorModel(r=127, g=255, b=212)
    beige = ColorModel(r=245, g=245, b=220)
    bisque = ColorModel(r=255, g=228, b=196)
    cornflower_blue = ColorModel(r=100, g=149, b=237)
    firebrick = ColorModel(r=178, g=34, b=34)
    fuchsia = ColorModel(r=255, g=0, b=255)
    gainsboro = ColorModel(r=220, g=220, b=220)
    ivory = ColorModel(r=255, g=255, b=240)
    linen = ColorModel(r=250, g=240, b=230)
    maroon = ColorModel(r=128, g=0, b=0)
    mint_cream = ColorModel(r=245, g=255, b=250)
    misty_rose = ColorModel(r=255, g=228, b=225)
    moccasin = ColorModel(r=255, g=228, b=181)
    navajo_white = ColorModel(r=255, g=222, b=173)
    peru = ColorModel(r=205, g=133, b=63)
    plum = ColorModel(r=221, g=160, b=221)
    sienna = ColorModel(r=160, g=82, b=45)
    silver = ColorModel(r=192, g=192, b=192)
    slate_blue = ColorModel(r=106, g=90, b=205)
    slate_gray = ColorModel(r=112, g=128, b=144)
    thistle = ColorModel(r=216, g=191, b=216)
    tomato = ColorModel(r=255, g=99, b=71)
    wheat = ColorModel(r=245, g=222, b=179)