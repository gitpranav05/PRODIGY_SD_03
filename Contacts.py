from tkinter import *
import tkinter.messagebox as tmsg
import os

# File to store contacts
CONTACTS_FILE = "contacts.txt"

# Load contacts from file
def load_contacts():
    contacts = []
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as file:
            for line in file:
                name, phone, email = line.strip().split("|")
                contacts.append({"name": name, "phone": phone, "email": email})
    return contacts

# Save contacts to file
def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as file:
        for contact in contacts:
            file.write(f"{contact['name']}|{contact['phone']}|{contact['email']}\n")

# Add a new contact
def add_contact():
    name = entry_name.get()
    phone = entry_phone.get()
    email = entry_email.get()

    if not name or not phone or not email:
        tmsg.showwarning("Input Error", "All fields are required!")
        return

    contacts.append({"name": name, "phone": phone, "email": email})
    save_contacts(contacts)
    refresh_contacts_list()
    entry_name.delete(0, END)
    entry_phone.delete(0, END)
    entry_email.delete(0, END)

# Refresh the contact list display
def refresh_contacts_list():
    listbox_contacts.delete(0, END)
    for contact in contacts:
        listbox_contacts.insert(END, contact["name"])

# View contact details
def view_contact():
    selected_index = listbox_contacts.curselection()
    if not selected_index:
        tmsg.showwarning("Selection Error", "Please select a contact to view.")
        return

    contact = contacts[selected_index[0]]
    tmsg.showinfo(
        "Contact Details",
        f"Name: {contact['name']}\nPhone: {contact['phone']}\nEmail: {contact['email']}"
    )

# Edit a contact
def edit_contact():
    selected_index = listbox_contacts.curselection()
    if not selected_index:
        tmsg.showwarning("Selection Error", "Please select a contact to edit.")
        return

    contact = contacts[selected_index[0]]

    def save_changes():
        contact["name"] = entry_name.get()
        contact["phone"] = entry_phone.get()
        contact["email"] = entry_email.get()
        save_contacts(contacts)
        refresh_contacts_list()
        top_edit.destroy()

    top_edit = Toplevel(root)
    top_edit.title("Edit Contact")

    Label(top_edit, text="Name:").grid(row=0, column=0, padx=10, pady=5)
    entry_name = Entry(top_edit)
    entry_name.grid(row=0, column=1, padx=10, pady=5)
    entry_name.insert(0, contact["name"])

    Label(top_edit, text="Phone:").grid(row=1, column=0, padx=10, pady=5)
    entry_phone = Entry(top_edit)
    entry_phone.grid(row=1, column=1, padx=10, pady=5)
    entry_phone.insert(0, contact["phone"])

    Label(top_edit, text="Email:").grid(row=2, column=0, padx=10, pady=5)
    entry_email = Entry(top_edit)
    entry_email.grid(row=2, column=1, padx=10, pady=5)
    entry_email.insert(0, contact["email"])

    Button(top_edit, text="Save", command=save_changes).grid(row=3, column=0, columnspan=2, pady=10)

# Delete a contact
def delete_contact():
    selected_index = listbox_contacts.curselection()
    if not selected_index:
        tmsg.showwarning("Selection Error", "Please select a contact to delete.")
        return

    contact = contacts[selected_index[0]]
    if tmsg.askyesno("Confirm Delete", f"Are you sure you want to delete {contact['name']}?"):
        contacts.pop(selected_index[0])
        save_contacts(contacts)
        refresh_contacts_list()

# Search for a contact
def search_contact():
    query = entry_search.get().lower()
    if not query:
        tmsg.showwarning("Search Error", "Please enter a name, phone, or email to search.")
        return

    listbox_contacts.delete(0, END)
    for contact in contacts:
        if query in contact["name"].lower() or query in contact["phone"].lower() or query in contact["email"].lower():
            listbox_contacts.insert(END, contact["name"])

# Main application window
root = Tk()
root.title("Contact Management System")

contacts = load_contacts()

# Input fields
frame_inputs = Frame(root)
frame_inputs.pack(pady=10)

Label(frame_inputs, text="Name:").grid(row=0, column=0, padx=5, pady=5)
entry_name = Entry(frame_inputs)
entry_name.grid(row=0, column=1, padx=5, pady=5)

Label(frame_inputs, text="Phone:").grid(row=1, column=0, padx=5, pady=5)
entry_phone = Entry(frame_inputs)
entry_phone.grid(row=1, column=1, padx=5, pady=5)

Label(frame_inputs, text="Email:").grid(row=2, column=0, padx=5, pady=5)
entry_email = Entry(frame_inputs)
entry_email.grid(row=2, column=1, padx=5, pady=5)

Button(frame_inputs, text="Add Contact", command=add_contact).grid(row=3, column=0, columnspan=2, pady=10)

# Search field
frame_search = Frame(root)
frame_search.pack(pady=10)

Label(frame_search, text="Search:").grid(row=0, column=0, padx=5, pady=5)
entry_search = Entry(frame_search)
entry_search.grid(row=0, column=1, padx=5, pady=5)
Button(frame_search, text="Search", command=search_contact).grid(row=0, column=2, padx=5, pady=5)

# Contact list
frame_contacts = Frame(root)
frame_contacts.pack(pady=10)

Label(frame_contacts, text="Contacts:").pack()
listbox_contacts = Listbox(frame_contacts, width=40, height=10)
listbox_contacts.pack()

# Buttons for contact actions
frame_actions = Frame(root)
frame_actions.pack(pady=10)

Button(frame_actions, text="View Contact", command=view_contact).grid(row=0, column=0, padx=10)
Button(frame_actions, text="Edit Contact", command=edit_contact).grid(row=0, column=1, padx=10)
Button(frame_actions, text="Delete Contact", command=delete_contact).grid(row=0, column=2, padx=10)

refresh_contacts_list()

root.mainloop()
