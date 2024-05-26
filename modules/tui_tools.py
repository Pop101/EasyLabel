import TermTk as ttk

def interp_color(color_1:ttk.TTkColor, color_2:ttk.TTkColor, interp:float) -> ttk.TTkColor:
    if color_1._fg == None:
        fg = color_2._fg
    elif color_2._fg == None:
        fg = color_1._fg
    else:
        fg = [
            int(color_1._fg[0] + (color_2._fg[0] - color_1._fg[0]) * interp),
            int(color_1._fg[1] + (color_2._fg[1] - color_1._fg[1]) * interp),
            int(color_1._fg[2] + (color_2._fg[2] - color_1._fg[2]) * interp)
        ]
    
    if color_1._bg == None:
        bg = color_2._bg
    elif color_2._bg == None:
        bg = color_1._bg
    else:
        bg = [
            int(color_1._bg[0] + (color_2._bg[0] - color_1._bg[0]) * interp),
            int(color_1._bg[1] + (color_2._bg[1] - color_1._bg[1]) * interp),
            int(color_1._bg[2] + (color_2._bg[2] - color_1._bg[2]) * interp)
        ]
        
    return ttk.TTkColor(
        fg=fg,
        bg=bg,
        colorMod=color_1._colorMod
    )

def inverse_color(color:ttk.TTkColor) -> ttk.TTkColor:
    if color._fg == None:
        fg = None
    else:
        fg = [255 - color._fg[0], 255 - color._fg[1], 255 - color._fg[2]]
    
    if color._bg == None:
        bg = None
    else:
        bg = [255 - color._bg[0], 255 - color._bg[1], 255 - color._bg[2]]
        
    return ttk.TTkColor(
        fg=fg,
        bg=bg,
        colorMod=color._colorMod
    )

def generate_button_style(row:float, col:float):
    # Conceptually, we want a red to green gradient across the rows and a blue to yellow gradient across the columns
    # We can achieve this by interpolating between the colors
    
    row_color_1 = ttk.TTkColor.fg("#ff0000")
    row_color_2 = ttk.TTkColor.fg("#00ff00")
    row_color = interp_color(row_color_1, row_color_2, row)
    
    col_color_1 = ttk.TTkColor.fg("#0000ff")
    col_color_2 = ttk.TTkColor.fg("#ffff00")
    col_color = interp_color(col_color_1, col_color_2, col)
    
    bg_color = interp_color(row_color, col_color, 0.5).invertFgBg()
    fg_color = ttk.TTkColor.fg("#dddddd")
    
    return {
                'default':     {'color': fg_color+bg_color,
                                'borderColor': ttk.TTkColor.RST,
                                'grid':1},
                'disabled':    {'color': ttk.TTkColor.fg('#888888'),
                                'borderColor':ttk.TTkColor.fg('#888888'),
                                'grid':0},
                'hover':       {'color': fg_color + interp_color(bg_color, ttk.TTkColor.bg("#dddddd"), 0.2) + ttk.TTkColor.BOLD,
                                'borderColor': ttk.TTkColor.fg("#FFFFCC")+ttk.TTkColor.BOLD,
                                'grid':1},
                'checked':     {'color': fg_color + interp_color(bg_color, ttk.TTkColor.bg("#FFFFFF"), 0.5),
                                'borderColor': ttk.TTkColor.fg("#FFFFFF") + interp_color(bg_color, ttk.TTkColor.bg("#FFFFFF"), 0.3),
                                'grid':0},
                'unchecked':   {'color': fg_color + bg_color,
                                'borderColor': ttk.TTkColor.RST,
                                'grid':3},
                'clicked':     {'color': bg_color.invertFgBg() + interp_color(bg_color, fg_color.invertFgBg(), 0.5) + ttk.TTkColor.BOLD,
                                'borderColor': ttk.TTkColor.fg("#DDDDDD")+ttk.TTkColor.BOLD,
                                'grid':0},
                'focus':       {'color': fg_color + bg_color + ttk.TTkColor.BOLD,
                                'borderColor': bg_color + ttk.TTkColor.BOLD,
                                'grid':1},
    }