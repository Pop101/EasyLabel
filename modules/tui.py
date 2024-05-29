import TermTk as ttk

from modules import config
from modules import tui_tools as tools

import os
import math

def initialize_root(layout_to_wrap: ttk.TTkWidget) -> ttk.TTk:
    root = ttk.TTk(layout=ttk.TTkVBoxLayout())
    
    # Add the top bar
    root.layout().addWidget(top_bar_layout())
    
    # Add the main section, which is in a 
    wrapped_layout = ttk.TTkFrame(border=True, layout=ttk.TTkVBoxLayout(), stretch=(True, True))
    wrapped_layout.addWidget(layout_to_wrap)
    
    frame = ttk.TTkFrame(layout=ttk.TTkHBoxLayout())
    frame.layout().addWidget(wrapped_layout)
    root.layout().addWidget(wrapped_layout)
    
    return root

def quit_app(additional_text:str = ""):
    """A callback to quit the app"""
    ttk.TTkHelper.quit()
    os.system("clear")
    if additional_text:
        print(additional_text)
    print("Quitting app, press enter to return")


def top_bar_layout() -> ttk.TTkWidget:
    """Create the top bar layout with the title and a quit button"""
    
    top_bar = ttk.TTkFrame(border=config.get("top_bar").get('framed', False), layout=ttk.TTkHBoxLayout(), size=(100, 3))
    
    top_bar.layout().addWidget(ttk.TTkLabel(text=config.get("top_bar").get('title', "")))
    top_bar.layout().addWidget(ttk.TTkSpacer())
    
    quit_btn = ttk.TTkButton(text="x", border=False, maxHeight=1, maxWidth=7)
    quit_btn.clicked.connect(quit_app)
    top_bar.layout().addWidget(quit_btn)
    
    return top_bar
    


def labelling_layout(text, buttons:list[str], allow_multiselect=False, button_callback=lambda x: x, confirmation_callback=lambda x: x, require_confirmation=False) -> ttk.TTkWidget:
    """
    Creates a labelling layout, with a header text and a grid of buttons.
    
    The button callback is called whenever a button is pressed, with argument of type `ttk.TTkButton`.
    The confirmation callback is called when the confirm button is pressed, with a list of all buttons.
    
    If `allow_multiselect` is set to True, multiple buttons can be selected at once. This will also create a confirm button.
    If `require_confirmation` is set to True, a confirm button will be created.
    
    If neither `allow_multiselect` nor `require_confirmation` are set to True, the confirmation callback will be called whenever a button is pressed.
    Otherwise, it is called when the confirm button is pressed.
    """
    main_frame = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(), border=True)     
    
    for line in text.splitlines():
        text_label = ttk.TTkLabel(text=line)
        main_frame.layout().addWidget(text_label)

    main_frame.layout().addWidget(ttk.TTkSpacer())
    
    # Create buttons
    all_buttons = []
    clicked_buttons = []
    
    # Calculate the number of rows and columns for the buttons
    side_length = int(math.sqrt(len(buttons)))
    rows = side_length
    columns = side_length
    
    if rows * columns < len(buttons):
        columns += 1
        
    if len(buttons) <= 3:
        columns = len(buttons)
    
    # Define the button callback
    def internal_button_callback(btn):
        button_callback(btn)
        if btn not in clicked_buttons:
            btn.setChecked(True)
            clicked_buttons.append(btn)
            
        elif btn in clicked_buttons:   
            clicked_buttons.remove(btn)
            btn.setChecked(False)
        
        if not allow_multiselect and btn.isChecked():
            for other_btn in clicked_buttons:
                if other_btn != btn:
                    other_btn.setChecked(False)
                    clicked_buttons.remove(other_btn)
                    
        if not (allow_multiselect or require_confirmation):
            confirmation_callback(all_buttons)
    
    # Add the buttons line-by-line for better scaling
    buttons_frame = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(), border=False, parent=main_frame)
    current_row = ttk.TTkFrame(layout=ttk.TTkHBoxLayout(), border=False, parent=buttons_frame)
    for i, button in enumerate(buttons):
        btn = ttk.TTkButton(text=button, border=True)
        btn.clicked.connect(lambda _btn=btn: internal_button_callback(_btn))
        btn.setCheckable(allow_multiselect or require_confirmation)
        btn.setStyle(tools.generate_button_style((i % columns) / rows, (i // columns) / columns))
        
        current_row.layout().addWidget(btn)
        if (i + 1) % columns == 0:
            current_row = ttk.TTkFrame(layout=ttk.TTkHBoxLayout(), border=False, parent=buttons_frame)
            
        all_buttons.append(btn)
        
    main_frame.layout().addWidget(buttons_frame)
    main_frame.layout().addWidget(ttk.TTkSpacer())
    
    # If we require confirmation, add the confirm button
    if allow_multiselect or require_confirmation:
        confirm_btn = ttk.TTkButton(text="Confirm", border=True)
        confirm_btn.clicked.connect(lambda: confirmation_callback(all_buttons))
        main_frame.layout().addWidget(confirm_btn)
    
    return main_frame

def __replace_layout(old_layout: ttk.TTkWidget, new_layout: ttk.TTkWidget):
    parent = old_layout._parent
    parent.removeWidget(old_layout)
    parent.addWidget(new_layout)

def __replace_layout_with_root(root: ttk.TTk, new_layout: ttk.TTkWidget):
    old_layout = root.layout().itemAtPosition(1, 0).widget()
    __replace_layout(old_layout, new_layout)
    
current_layout = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(), border=False)
root = initialize_root(current_layout)

def set_layout(new_layout: ttk.TTkWidget):
    global current_layout
    __replace_layout_with_root(root, new_layout)
    current_layout = new_layout

if __name__ == "__main__":
    set_layout(labelling_layout("This should not show", ["Button 1", "Button 2", "Button 3"] * 20, allow_multiselect=True))
    set_layout(labelling_layout("This should def show", ["Button 1", "Button 2", "Button 3"] * 20, allow_multiselect=True))
    
    root.mainloop()
    