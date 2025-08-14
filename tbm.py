import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from pymongo import MongoClient
from datetime import datetime
import uuid

def get_db_collection(uri="mongodb://localhost:27017/",
                      db_name="travel_db", coll_name="bookings"):
    client = MongoClient(uri)
    db = client[db_name]
    return db[coll_name]

collection = get_db_collection()

def make_uid():
    return str(uuid.uuid4())[:8]   # short unique ID

def add_booking():
    passenger = ent_passenger.get().strip()
    destination = ent_destination.get().strip()
    date_str = ent_date.get_date().strftime("%Y-%m-%d")
    status = status_var.get()

    if not (passenger and destination):
        messagebox.showerror("Missing Data", "Please fill in all fields.")
        return

    uid = make_uid()
    doc = {
        "uid": uid,
        "passenger": passenger,
        "destination": destination,
        "travel_date": date_str,
        "status": status
    }
    collection.insert_one(doc)
    messagebox.showinfo("Added", f"Booking {uid} created.")
    clear_form()
    display_all()

def edit_booking():
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Select", "Choose a booking to edit.")
        return

    uid = sel[0]
    passenger = ent_passenger.get().strip()
    destination = ent_destination.get().strip()
    date_str = ent_date.get_date().strftime("%Y-%m-%d")
    status = status_var.get()

    if not (passenger and destination):
        messagebox.showerror("Missing Data", "Please fill in all fields.")
        return

    result = collection.update_one(
        {"uid": uid},
        {"$set": {
            "passenger": passenger,
            "destination": destination,
            "travel_date": date_str,
            "status": status
        }}
    )

    if result.matched_count:
        messagebox.showinfo("Updated", f"Booking {uid} updated.")
    else:
        messagebox.showerror("Not found", "Booking not found in DB.")

    clear_form()
    display_all()

def remove_booking():
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Select", "Choose a booking to cancel.")
        return
    uid = sel[0]
    confirm = messagebox.askyesno("Confirm", f"Cancel booking {uid}?")
    if not confirm:
        return
    result = collection.delete_one({"uid": uid})
    if result.deleted_count:
        messagebox.showinfo("Cancelled", f"Booking {uid} removed.")
    else:
        messagebox.showwarning("Missing", "Booking not found.")
    clear_form()
    display_all()

def clear_form():
    ent_passenger.delete(0, tk.END)
    ent_destination.delete(0, tk.END)
    ent_date.set_date(datetime.today())
    status_var.set("Booked")
    tree.selection_remove(tree.selection())

def display_all():
    for row in tree.get_children():
        tree.delete(row)
    for doc in collection.find().sort("travel_date", 1):
        tree.insert("", tk.END, iid=doc["uid"],
                    values=(doc["uid"], doc["passenger"], doc["destination"], doc["travel_date"], doc["status"]))

def on_tree_select(event):
    sel = tree.selection()
    if not sel:
        return
    uid = sel[0]
    doc = collection.find_one({"uid": uid})
    if not doc:
        return
    ent_passenger.delete(0, tk.END)
    ent_passenger.insert(0, doc.get("passenger", ""))
    ent_destination.delete(0, tk.END)
    ent_destination.insert(0, doc.get("destination", ""))
    ent_date.set_date(datetime.strptime(doc.get("travel_date", ""), "%Y-%m-%d"))
    status_var.set(doc.get("status", "Booked"))

root = tk.Tk()
root.title("✈ Travel Booking Manager")
root.geometry("950x600")
root.configure(bg="#eaf4fc")

# Title
banner = tk.Label(root, text="✈ Travel Booking Manager", font=("Arial", 20, "bold"), bg="#0077b6", fg="white", pady=10)
banner.pack(fill=tk.X)

# Form Frame
form_frame = tk.LabelFrame(root, text="Booking Details", font=("Arial", 12, "bold"), bg="#eaf4fc", padx=10, pady=10)
form_frame.pack(fill=tk.X, padx=15, pady=10)

# Passenger Name
tk.Label(form_frame, text="Passenger Name:", bg="#eaf4fc", font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=5)
ent_passenger = tk.Entry(form_frame, width=30)
ent_passenger.grid(row=0, column=1, pady=5, padx=5)

# Destination
tk.Label(form_frame, text="Destination:", bg="#eaf4fc", font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=5)
ent_destination = tk.Entry(form_frame, width=30)
ent_destination.grid(row=1, column=1, pady=5, padx=5)

# Travel Date
tk.Label(form_frame, text="Travel Date:", bg="#eaf4fc", font=("Arial", 11)).grid(row=2, column=0, sticky="w", pady=5)
ent_date = DateEntry(form_frame, width=18, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
ent_date.grid(row=2, column=1, pady=5, padx=5, sticky="w")

# Status
tk.Label(form_frame, text="Status:", bg="#eaf4fc", font=("Arial", 11)).grid(row=3, column=0, sticky="w", pady=5)
status_var = tk.StringVar(value="Booked")
status_menu = ttk.Combobox(form_frame, textvariable=status_var, values=["Booked", "Completed", "Cancelled"], state="readonly", width=16)
status_menu.grid(row=3, column=1, pady=5, padx=5, sticky="w")

# Buttons
btn_frame = tk.Frame(form_frame, bg="#eaf4fc")
btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

btn_colors = {"bg": "#0077b6", "fg": "white"}

tk.Button(btn_frame, text="Add Booking", width=15, command=add_booking, bg=btn_colors["bg"], fg=btn_colors["fg"], relief="flat").grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Edit Booking", width=15, command=edit_booking, bg=btn_colors["bg"], fg=btn_colors["fg"], relief="flat").grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Cancel Booking", width=15, command=remove_booking, bg=btn_colors["bg"], fg=btn_colors["fg"], relief="flat").grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Clear Form", width=15, command=clear_form, bg=btn_colors["bg"], fg=btn_colors["fg"], relief="flat").grid(row=0, column=3, padx=5)
tk.Button(btn_frame, text="Refresh List", width=15, command=display_all, bg=btn_colors["bg"], fg=btn_colors["fg"], relief="flat").grid(row=0, column=4, padx=5)

# Table Frame
table_frame = tk.Frame(root, bg="#eaf4fc")
table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

cols = ("UID", "Passenger", "Destination", "Travel Date", "Status")
tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=15)

for col in cols:
    tree.heading(col, text=col)

tree.column("UID", width=100, anchor="center")
tree.column("Passenger", width=180, anchor="w")
tree.column("Destination", width=150, anchor="w")
tree.column("Travel Date", width=110, anchor="center")
tree.column("Status", width=100, anchor="center")

# Scrollbar
vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=vsb.set)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
vsb.pack(side=tk.RIGHT, fill=tk.Y)

tree.bind("<<TreeviewSelect>>", on_tree_select)

# Init
ent_date.set_date(datetime.today())
display_all()

root.mainloop()
