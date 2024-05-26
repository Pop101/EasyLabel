from modules import tui
from modules import config

import pandas as pd
import os

# Attempt to load the data
data_path = config.get("data").get("path", None)
if not data_path:
    print("No data path specified in config.yml")
    exit(1)

if not os.path.exists(data_path):
    print(f"Data path {data_path} does not exist")
    exit(1)

if not config.get("output").get("path", None):
    print("No output path specified in config.yml")
    exit(1)
    
data = pd.read_csv(data_path, encoding=config.get("data").get("encoding", "utf-8"), sep=config.get("data").get("separator", ","))
label_columns = config.get("data").get("label_columns", data.columns.difference([config.get("data").get("text_column")]))
 
def write_row(row:pd.Series):
    if not os.path.exists(config.get("output").get("path")) and os.path.dirname(config.get("output").get("path")):
        os.makedirs(os.path.dirname(config.get("output").get("path")), exist_ok=True)
    
    row.to_frame().T.to_csv(config.get("output").get("path"), mode='a', header=not os.path.exists(config.get("output").get("path")), index=False, encoding=config.get("output").get("encoding", "utf-8"), sep=config.get("output").get("separator", ","))

row_iterator = iter(data.iterrows())
curr_row = None
def next_row():
    global curr_row
    try:
        _, curr_row = next(row_iterator)
        curr_row = curr_row.copy()
    except StopIteration:
        tui.quit_app("No more rows left")
        
# Advance the row iterator according to the lines of the output file
row_iterator = iter(data.iterrows())
output_len = 0
if os.path.isfile(config.get("output").get("path")):
    pd.read_csv(config.get("output").get("path"), encoding=config.get("output").get("encoding", "utf-8"), sep=config.get("output").get("separator", ","))
    output_len = len(data)
    for _ in range(output_len):
        next_row()
    
def advance_row(all_buttons):
    if all_buttons and curr_row is not None:
        buttons_pressed = {str(btn.text()).strip() for btn in all_buttons if btn.isChecked()}
        for column in label_columns:
            curr_row[column] = column in buttons_pressed
            
        write_row(curr_row)
    
    next_row()
    tui.set_layout(tui.labelling_layout(
        text=curr_row[config.get("data").get("text_column")],
        buttons=label_columns,
        allow_multiselect=config.get("data").get("multi_label", False),
        require_confirmation=config.get("data").get("require_confirmation", False),
        confirmation_callback=advance_row
    ))

advance_row(None)
tui.root.mainloop()
# poetry run python easy_label.py