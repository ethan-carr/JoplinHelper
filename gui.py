import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog

import stock_descriptions
import daily_journal

def toggle_check(index):
    checked_items[index] = not checked_items[index]
    update_checklist()

def update_checklist():
    for i, item in enumerate(items):
        checkbutton_vars[i].set(checked_items[i])

def select_all():
    if(checked_items.count(False) == len(checked_items)):
        for i in range(len(items)):
            checked_items[i] = True
    else:
        for i in range(len(items)):
            checked_items[i] = False

    
    for i, item in enumerate(items):
        checkbutton_vars[i].set(checked_items[i])

def create_daily():
    output_label.configure(text=daily_journal.create_daily_journal())
    return True

def add_to_watch():
    inputs = []
    questions = ["Full name"]
    for i in range(len(questions)):
        user_input = simpledialog.askstring("Input", questions[i])
        if user_input is None:
            return  # User clicked Cancel
        inputs.append(user_input)
    
    
    output_label.configure(text=daily_journal.add_to_watching(full_name=str(inputs[0])))

    return True

def add_to_buys():
    inputs = []
    questions = ["Full Finviz name? ex.) AAPL | Apple Inc.","Date of Purchase? ex.) 2023-08-30","Price of Purchased Stock? (no $)","Number of Shares Purchased?","Account Traded? (Paper or TD Ameritrade)"]
    for i in range(len(questions)):
        user_input = simpledialog.askstring("Input", questions[i])
        if user_input is None:
            return  # User clicked Cancel
        inputs.append(user_input)
    
    
    output_label.configure(text=daily_journal.add_to_buying(full_name=str(inputs[0]),date=inputs[1],price=inputs[2],shares=inputs[3],account=inputs[4]))


    return True

def add_to_sells():
    inputs = []
    questions = ["Full Finviz name? ex.) AAPL | Apple Inc.","Date of Sell? ex.) 2023-08-30","Price of Sold Stock? (no $)","Number of Shares Sold?","Account Traded? (Paper or TD Ameritrade)"]
    for i in range(len(questions)):
        user_input = simpledialog.askstring("Input", questions[i])
        if user_input is None:
            return  # User clicked Cancel
        inputs.append(user_input)
    
    
    output_label.configure(text=daily_journal.add_to_sell(full_name=str(inputs[0]),date=inputs[1],price=inputs[2],shares=inputs[3],account=inputs[4]))


    return True

def add_to_port():
    inputs = []
    questions = ["Full Finviz name? ex.) AAPL | Apple Inc.","Date of Purchase? ex.) 2023-08-30","Price of Purchased Stock? (no $)","Number of Shares Purchased?","Account Traded? (Paper or TD Ameritrade)"]
    for i in range(len(questions)):
        user_input = simpledialog.askstring("Input", questions[i])
        if user_input is None:
            return  # User clicked Cancel
        inputs.append(user_input)
    
    output_label.configure(text=daily_journal.add_to_portfolio(full_name=str(inputs[0]),date=inputs[1],price=inputs[2],shares=inputs[3],account="### " + str(inputs[4]) + "\n"))


    return True

def update_port():
    output_label.configure(text=daily_journal.update_portfolio())
    return True

def update_stocks():
    print(checked_items)
    print(items)
    return True

def refresh_list():
    output_label.configure(text="List Refreshed!")
    notebook_id = stock_descriptions.joplin.get_notebook("Individual Stocks")
    notes = stock_descriptions.joplin.api.get_notes(notebook_id=notebook_id)
    
    titles = []
    for note in notes.items:
        titles.append(note.title)
    
    items = titles
    return titles

root = tk.Tk()
root.title("Ethan's Joplin Stock Tool V0.3.1")

main_frame = ttk.Frame(root)
main_frame.pack(fill='both', expand=True)

# Left Column - Buttons
button_frame = ttk.Frame(main_frame)
button_frame.pack(side='left', padx=10, pady=10)

top_label = ttk.Label(button_frame, text="Ethan's Joplin Utility", font=("Arial", 16))
top_label.pack()

mini_label = ttk.Label(button_frame, text="Stock Tool V0.3.1", font=("Arial", 12))
mini_label.pack()

# Some padding
top_padding = ttk.Label(button_frame)
top_padding.pack()

# Create daily journal
createdaily_button = ttk.Button(button_frame, text="Create Daily Journal", command=create_daily, width=30)
createdaily_button.pack()

# Add to watchlist
addwatchlist_button = ttk.Button(button_frame, text="Add to Watchlist", command=add_to_watch, width=30)
addwatchlist_button.pack()

# Add to buying
addbuying_button = ttk.Button(button_frame, text="Add to Buys", command=add_to_buys, width=30)
addbuying_button.pack()

# Add to selling
addselling_button = ttk.Button(button_frame, text="Add to Sells", command=add_to_sells, width=30)
addselling_button.pack()

# Add to portfolio
addport_button = ttk.Button(button_frame, text="Add to Portfolio", command=add_to_port, width=30)
addport_button.pack()

# Update Portfolio
updateport_button = ttk.Button(button_frame, text="Update Portfolio", command=update_port, width=30)
updateport_button.pack()

# Create Stock Description
#createdaily_button = ttk.Button(button_frame, text="Create Daily Journal", command=select_all, width=30)
#createdaily_button.pack()

# Some padding
top_padding = ttk.Label(button_frame)
top_padding.pack()

mini2_label = ttk.Label(button_frame, text="Checklist Tools", font=("Arial", 12))
mini2_label.pack()

select_all_button = ttk.Button(button_frame, text="Select All", command=select_all, width=30)
select_all_button.pack()

updatestocks_button = ttk.Button(button_frame, text="Update Stocks", command=update_stocks, width=30)
updatestocks_button.pack()

refresh_button = ttk.Button(button_frame, text="Refresh List", command=refresh_list, width=30)
refresh_button.pack()

top_padding = ttk.Label(button_frame)
top_padding.pack()

output_label = ttk.Label(button_frame, text="", font=("Arial", 9))
output_label.pack()

top_padding = ttk.Label(button_frame)
top_padding.pack()


# Right Column - Scrollable Checklist
checklist_frame = ttk.Frame(main_frame, borderwidth=2, relief='groove')
checklist_frame.pack(side='right', padx=10, pady=10, fill='both', expand=True)

scrollable_frame = ttk.Frame(checklist_frame)
scrollable_frame.pack(fill='both', expand=True)

canvas = tk.Canvas(scrollable_frame)
canvas.pack(side='left', fill='both', expand=True)

scrollbar = ttk.Scrollbar(scrollable_frame, orient='vertical', command=canvas.yview)
scrollbar.pack(side='right', fill='y')
canvas.configure(yscrollcommand=scrollbar.set)

inner_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=inner_frame, anchor='nw')

items = refresh_list()
checked_items = [False] * len(items)
checkbutton_vars = []

for i, item in enumerate(items):
    var = tk.BooleanVar(value=checked_items[i])
    checkbutton_vars.append(var)
    checkbutton = ttk.Checkbutton(inner_frame, text=item, variable=var, command=lambda i=i: toggle_check(i))
    checkbutton.pack(anchor='w')

root.mainloop()
