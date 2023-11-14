import os
import tkinter as tk
from tkinter import ttk

class Wishlister(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title_label = ttk.Label(text="Wishlister v1.0.0")
        self.title_label.config(font=("Arial", 24))

        self.add_button = ttk.Button(text="Add Game")
        self.remove_button = ttk.Button(text="Remove Game")
        self.insert_button = ttk.Button(text="Insert Game")
        self.swap_button = ttk.Button(text="Swap Games")
        self.shuffle_button = ttk.Button(text="Shuffle Games")
        self.find_max_button = ttk.Button(text="Find Max. Price")
        self.init_wishlist()
        self.database = []

        self.title_label.grid(row=0, column=0, columnspan=6, padx=5, pady=5, sticky="nsew")

        self.add_button.grid(row=1, column=0, padx=5, pady=(0,5), sticky="nsew")
        self.remove_button.grid(row=1, column=1, padx=(0,5), pady=(0,5), sticky="nsew")
        self.insert_button.grid(row=1, column=2, padx=(0,5), pady=(0,5), sticky="nsew")
        self.swap_button.grid(row=1, column=3, padx=(0,5), pady=(0,5), sticky="nsew")
        self.shuffle_button.grid(row=1, column=4, padx=(0,5), pady=(0,5), sticky="nsew")
        self.find_max_button.grid(row=1, column=5, padx=(0,5), pady=(0,5), sticky="nsew")
        
        self.wishlist_display.grid(row=2, column=0, columnspan=6, padx=5, pady=(0,5), sticky="nsew")

        if not os.path.exists(f"{os.path.dirname(__file__)}/storage/"):
            os.mkdir(f"{os.path.dirname(__file__)}/storage/")

    def init_wishlist(self):
        self.wishlist_display = ttk.Treeview()
        self.wishlist_display["columns"] = ("Game", "Price", "URL")
        self.wishlist_display.heading("#0", text="#")
        self.wishlist_display.heading("Game", text="Name")
        self.wishlist_display.heading("Price", text="Price")
        self.wishlist_display.heading("URL", text="URL")

        self.wishlist_display.column("#0", width=30)

    def add_item(self):
        pass

    def remove_item(self):
        pass

    def insert_item(self):
        pass

    def swap_items(self):
        pass

    def shuffle_items(self):
        pass
    
    def find_max(self):
        pass

if __name__ == "__main__":
    app = Wishlister()
    app.mainloop()
