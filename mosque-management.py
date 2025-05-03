import tkinter as tk
from tkinter import messagebox
from dbConnection import MosqueDatabase
import webbrowser

db = MosqueDatabase()

class Mosque:
    def __init__(self, name, type, address, coordinates, imam_name):
        self.name = name
        self.type = type
        self.address = address
        self.coordinates = coordinates
        self.imam_name = imam_name

    def insert(self):
        db.insert(self.name, self.type, self.address, self.coordinates, self.imam_name)

#  GUI Setup
green = "#464E2E"
brown = "#362706"
grey = "#E9E5D6"

root = tk.Tk()
root.title("Mosque Manager")
root.resizable(0, 0)
root.configure(bg=grey)

# Title
main = tk.Label(root, text="Mosque Management System", bg=grey, fg=brown, font=("Helvetica", 16, "bold"))
main.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Input Fields
fields = ['Name', 'Address', 'Coordinates', 'Imam Name']
entries = {}

for i, field in enumerate(fields, start=1):
    tk.Label(root, text=field, bg=grey, fg=brown, font=("Helvetica", 12, "bold")).grid(
        row=i, column=0, padx=10, pady=5, sticky='w' 
    )
    ent = tk.Entry(root, width=30, bg="#FDF7F4", fg=brown, font=("Helvetica", 11, "bold"))
    ent.grid(
        row=i, column=1, padx=(0,10), pady=5, sticky='w'
    )
    entries[field.lower().replace(" ", "_")] = ent

# Type Dropdown 
tk.Label(root, text="Type", bg=grey, fg=brown, font=("Helvetica", 12, "bold")).grid(
    row=len(fields)+1, column=0, padx=10, pady=5, sticky='w'
)
mosque_types = ['Arabic', 'Persian', 'Turkish', 'Other']
selected_type = tk.StringVar(value=mosque_types[0])
option_menu = tk.OptionMenu(root, selected_type, *mosque_types)
option_menu.configure(bg=brown, fg=grey, font=("Helvetica", 11, "bold"), highlightthickness=0, bd=0)
option_menu.grid(
    row=len(fields)+1, column=1, sticky='w', padx=(0,10), pady=5
)

# Listbox Display
listbox = tk.Listbox(root, width=80, height=10)
listbox.configure(bg="#FDF7F4", fg=brown, font=("Helvetica", 11, "bold"), selectbackground="#FDF7F4", selectforeground=green)
listbox.grid(row=len(fields)+2, column=0, columnspan=2, padx=10, pady=10)

selected_id = None

def refresh_listbox(data):
    listbox.delete(0, tk.END)
    for mosque in data:
        listbox.insert(tk.END, f"{mosque[0]} | {mosque[1]} | {mosque[2]} | {mosque[3]} | {mosque[4]} | {mosque[5]}")

def on_listbox_select(event):
    global selected_id
    selection = listbox.curselection()
    if selection:
        index = selection[0]
        data = listbox.get(index).split(" | ")
        selected_id = int(data[0])
        entries['name'].delete(0, tk.END)
        entries['name'].insert(0, data[1])
        selected_type.set(data[2])
        entries['address'].delete(0, tk.END)
        entries['address'].insert(0, data[3])
        entries['coordinates'].delete(0, tk.END)
        entries['coordinates'].insert(0, data[4])
        entries['imam_name'].delete(0, tk.END)
        entries['imam_name'].insert(0, data[5])

listbox.bind('<<ListboxSelect>>', on_listbox_select)

# Button Actions 
def add_entry():
    global selected_id
    name = entries['name'].get()
    type_ = selected_type.get()
    address = entries['address'].get()
    coordinates = entries['coordinates'].get()
    imam_name = entries['imam_name'].get()
    if name and address:
        mosque = Mosque(name, type_, address, coordinates, imam_name)
        mosque.insert()
        selected_id = None
        messagebox.showinfo("Success", "Mosque added.")
        display_all()
    else:
        messagebox.showerror("Error", "Name and address are required.")

def update_entry():
    global selected_id
    if selected_id is None:
        messagebox.showerror("Error", "Select an entry to update.")
        return
    db.update(
        selected_id,
        entries['name'].get(),
        selected_type.get(),
        entries['address'].get(),
        entries['coordinates'].get(),
        entries['imam_name'].get()
    )
    selected_id = None
    messagebox.showinfo("Updated", "Mosque updated.")
    display_all()

def delete_entry():
    global selected_id
    if selected_id is None:
        messagebox.showerror("Error", "Select an entry to delete.")
        return
    db.delete(selected_id)
    selected_id = None
    messagebox.showinfo("Deleted", "Mosque deleted.")
    display_all()

def search_entry():
    name = entries['name'].get()
    if not name:
        messagebox.showerror("Error", "Enter a name to search.")
        return
    results = db.search(name)
    refresh_listbox(results)

def display_all():
    mosques = db.display_mosques()
    refresh_listbox(mosques)

def display_on_map():
    if selected_id is None:
        messagebox.showerror("Error", "Select an entry with coordinates.")
        return
    coords = entries['coordinates'].get()
    if coords:
        url = f"https://www.google.com/maps?q={coords}"
        webbrowser.open(url)
    else:
        messagebox.showerror("Error", "No coordinates found.")

# Buttons
buttons = [
    ("Add Entry", add_entry),
    ("Update Entry", update_entry),
    ("Delete Entry", delete_entry),
    ("Search by Name", search_entry),
    ("Display All", display_all),
    ("Display on Map", display_on_map)
]

for i, (text, cmd) in enumerate(buttons):
    tk.Button(root, text=text, bg=brown, fg=grey, font=("Helvetica", 11, "bold"), width=20, command=cmd).grid(row=7 + i // 2, column=i % 2, padx=10, pady=5)

display_all()
root.mainloop()