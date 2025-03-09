
from .colors import ColorCombo, Colors


"""
Styles definitions for the formatting
These get applied in the formatting of the log messages
----------------
You can override these values and customize the styling of the formatting
"""


"Separators for the formatting of the log messages"
class Separators:
    prefix_time = " || "

    time_date = " ~ "
    date_path = " || "
    path_lineno = " "
    lineno_level = " || "
    
    level_message = " >>> "


"Formatting colors"
class FormatColors:
    time = ColorCombo(fg=Colors.slate_blue)
    date = ColorCombo(fg=Colors.slate_blue)
    path = ColorCombo(fg=Colors.royal_blue)
    lineno = ColorCombo(fg=Colors.khaki)

    separator = ColorCombo(fg=Colors.gray)


"Levels colors"
"NOTE: These are not customizable from here. Use `Levels` instead."
class LevelsColors:
    debug = ColorCombo(fg=Colors.forest_green)
    info = ColorCombo(fg=Colors.cyan)
    warning = ColorCombo(fg=Colors.orange)
    error = ColorCombo(fg=Colors.red)
    fatal = ColorCombo(fg=Colors.white, bg=Colors.red)
