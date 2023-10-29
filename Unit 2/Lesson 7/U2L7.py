import tkinter as tk
import os
import sys
import time
from tkinter import ttk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return None

        elif event.event_type == 'modified':
            print("Reloading...")
            os.execl(sys.executable, sys.executable, *sys.argv)

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

database = []

root = tk.Tk()
root.title("Wishlister")
root.geometry("600x500")

# Create a label for the title
title_label = tk.Label(root, text="Wishlister", font=("Helvetica", 16))
title_label.grid(row=0, column=0, columnspan=2, pady=10)

wishlist_display = ttk.Treeview(root, columns=("Name", "Price", "Link"))
wishlist_display.heading("#0", text="Name")
wishlist_display.heading("#1", text="Price")
wishlist_display.heading("#2", text="Link")
wishlist_display.column("#0", width=300)
wishlist_display.column("#1", width=100)
wishlist_display.column("#2", width=200)
wishlist_display.grid(row=1, column=0, columnspan=2, pady=10)

def addGame():
    # Create a new window
    add_window = tk.Toplevel(root)
    add_window.title("Add Game")
    add_window.geometry("300x200")

    # Create labels and entry fields for the game information
    name_label = ttk.Label(add_window, text="Name:")
    name_entry = ttk.Entry(add_window)
    price_label = ttk.Label(add_window, text="Price:")
    price_entry = ttk.Entry(add_window)
    link_label = ttk.Label(add_window, text="Link:")
    link_entry = ttk.Entry(add_window)

    name_label.grid(row=0, column=0, padx=10, pady=10)
    name_entry.grid(row=0, column=1, padx=10, pady=10)
    price_label.grid(row=1, column=0, padx=10, pady=10)
    price_entry.grid(row=1, column=1, padx=10, pady=10)
    link_label.grid(row=2, column=0, padx=10, pady=10)
    link_entry.grid(row=2, column=1, padx=10, pady=10)

    # Create a button to add the game to the database
    add_button = ttk.Button(add_window, text="Add Game", command=lambda: addToDatabase(name_entry.get(), price_entry.get(), link_entry.get()))
    add_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

add_game_button = ttk.Button(root, text="Add Game", command=addGame)
add_game_button.grid(row=2, column=0, padx=10, pady=10)

def addToDatabase(name, price, link):
    # Add the game to the database
    database.append((name, price, link))

    # Add the game to the treeview
    wishlist_display.insert(parent='', index='end', iid=len(database)-1, text=name, values=(price, link))

root.mainloop()