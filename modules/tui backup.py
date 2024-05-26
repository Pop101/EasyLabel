import TermTk as ttk

import config

import os
import math

def quit_app():
    ttk.TTkHelper.quit()
    os.system("clear")
    print("Quitting app, press enter to return")


def top_bar_layout() -> ttk.TTkWidget:
    top_bar = ttk.TTkFrame(border=config.get("top_bar").get('Framed', False), layout=ttk.TTkHBoxLayout(), size=(100, 3))
    
    top_bar.layout().addWidget(ttk.TTkLabel(text=config.get("top_bar").get('Title', "")))
    top_bar.layout().addWidget(ttk.TTkSpacer())
    
    quit_btn = ttk.TTkButton(text="x", border=False, maxHeight=1, maxWidth=7)
    quit_btn.clicked.connect(quit_app)
    top_bar.layout().addWidget(quit_btn)
    
    return top_bar
    
def base_layout(layout_to_wrap: ttk.TTkWidget) -> ttk.TTk:
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

def main_layout(text, buttons:list, allow_multiselect=False, button_callback=lambda x: x, confirmation_callback=lambda: 1, require_confirmation=False) -> ttk.TTkWidget:
    # The main application frame, structured as a
    # line of text and multiple buttons with a single callback
    # for each button.
    # There may be a confirmation button on the bottom
    main_frame = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(), border=False)     
    
    for line in text.splitlines():
        text_label = ttk.TTkLabel(text=line)
        main_frame.layout().addWidget(text_label)

    main_frame.layout().addWidget(ttk.TTkSpacer())
    
    
    # Create buttons
    side_length = int(math.sqrt(len(buttons)))
    rows = side_length
    columns = side_length
    
    if rows * columns < len(buttons):
        columns += 1
        
    if len(buttons) <= 3:
        columns = len(buttons)
    
    clicked_buttons = []
    def internal_button_callback(btn):
        button_callback(btn)
        if btn.isChecked(): clicked_buttons.append(btn)
        else:               clicked_buttons.remove(btn)
        
        if not allow_multiselect and btn.isChecked():
            for other_btn in clicked_buttons:
                if other_btn != btn:
                    other_btn.setChecked(False)
                    clicked_buttons.remove(other_btn)
                    
        if not (allow_multiselect or require_confirmation):
            confirmation_callback(btn)
            
    buttons_frame = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(), border=False, parent=main_frame)
    current_row = ttk.TTkFrame(layout=ttk.TTkHBoxLayout(), border=False, parent=buttons_frame)
    for i, button in enumerate(buttons):
        btn = ttk.TTkButton(text=button, border=True)
        btn.clicked.connect(lambda _btn=btn: internal_button_callback(_btn))
        btn.setCheckable(allow_multiselect or require_confirmation)
        
        current_row.layout().addWidget(btn)
        if (i + 1) % columns == 0:
            current_row = ttk.TTkFrame(layout=ttk.TTkHBoxLayout(), border=False, parent=buttons_frame)
        
    main_frame.layout().addWidget(buttons_frame)
    main_frame.layout().addWidget(ttk.TTkSpacer())
    
    # If we require confirmation, add the confirm button
    if allow_multiselect or require_confirmation:
        confirm_btn = ttk.TTkButton(text="Confirm", border=True)
        confirm_btn.clicked.connect(lambda: confirmation_callback())
        main_frame.layout().addWidget(confirm_btn)
    
    return main_frame

def replace_layout(old_layout: ttk.TTkWidget, new_layout: ttk.TTkWidget):
    parent = old_layout._parent
    parent.removeWidget(old_layout)
    parent.addWidget(new_layout)

def replace_layout_with_root(root: ttk.TTk, new_layout: ttk.TTkWidget):
    old_layout = root.layout().itemAtPosition(1, 0).widget()
    replace_layout(old_layout, new_layout)
    
if __name__ == "__main__":
    main = main_layout("Hello, world!\n\n\t\tabba", [f"Button {i}" for i in range(26)], require_confirmation=True, button_callback=lambda x: print(x.text()))
    root = base_layout(main)
    print(main._parent)
    replace_layout_2(layout, main)
    exit(0)
    replace_layout(main, main:=main_layout("Hello, world!\n\n\t\taadsfabba", [f"Button {i}" for i in range(26)], require_confirmation=True, button_callback=lambda x: print(x.text())))
    replace_layout(main, main_layout("Hello, world!\n\n\tdsfadsf", [f"Button {i}" for i in range(26)], require_confirmation=True, button_callback=lambda x: print(x.text())))
    
    layout.mainloop()
    
    # poetry run python modules/tui.py
    