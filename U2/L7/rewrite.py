import os
import tkinter as tk
from tkinter import ttk
import json
import requests
import re
import webbrowser

class Wishlister(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wishlister v1.0.0")
        self.geometry("800x600")
        self.minsize(600, 300)

        self.title_label = ttk.Label(text="Wishlister v1.0.0")
        self.title_label.config(font=("Arial", 24))

        self.add_button = ttk.Button(text="Add Game", command=self.add_item_ui)
        self.remove_button = ttk.Button(text="Remove Game", command=self.remove_item_ui)
        self.insert_button = ttk.Button(text="Insert Game", command=self.insert_item_ui)
        self.swap_button = ttk.Button(text="Swap Games", command=self.swap_items_ui)
        self.shuffle_button = ttk.Button(text="Shuffle Games", command=self.shuffle_items_ui)
        self.find_max_button = ttk.Button(text="Find Max. Price", command=self.find_max_ui)
        self.init_wishlist()
        self.database = []
        self.mandatory_string_list = []
        self.mandatory_float_list = []

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
        else:
            try:
                with open(f"{os.path.dirname(__file__)}/storage/database.json", "r", encoding="utf-8") as file:
                    self.database = json.load(file)
            except FileNotFoundError:
                pass
        
        for i in range(6):
            self.columnconfigure(i, weight=1)
        self.rowconfigure(2, weight=1)

        self.wishlist_display.bind("<Double-1>", self.open_url)

    def init_wishlist(self):
        self.wishlist_display = ttk.Treeview()
        self.wishlist_display["columns"] = ("Game", "Price", "URL")
        self.wishlist_display.heading("#0", text="Steam ID")
        self.wishlist_display.heading("Game", text="Name")
        self.wishlist_display.heading("Price", text="Price")
        self.wishlist_display.heading("URL", text="URL")

        self.wishlist_display.column("#0", width=40)
        self.wishlist_display.column("Game", width=200)
        self.wishlist_display.column("Price", width=75)

    def add_item_ui(self):
        add_item_dialog = tk.Toplevel(self)
        add_item_dialog.title("Add Game")
        add_item_dialog.geometry("400x100")
        add_item_dialog.minsize(400, 100)
        add_item_dialog.resizable(False, False)

        add_item_dialog.title_label = ttk.Label(add_item_dialog, text="Add Game")
        add_item_dialog.title_label.config(font=("Arial", 12))

        add_item_dialog.game_link_label = ttk.Label(add_item_dialog, text="Game Link:", width=11)
        add_item_dialog.game_link_entry = ttk.Entry(add_item_dialog, width=50)

        add_item_dialog.add_button = ttk.Button(
            add_item_dialog,
            text="Add",
            command=lambda: (
                self.change_database(
                    action="add",
                    game_id=self.get_steam_details("id", add_item_dialog.game_link_entry.get()),
                    data={
                        "game_id": self.get_steam_details("id", add_item_dialog.game_link_entry.get()),
                        "name": self.get_steam_details("name", add_item_dialog.game_link_entry.get()),
                        "price": self.get_steam_details("price", add_item_dialog.game_link_entry.get()),
                        "url": add_item_dialog.game_link_entry.get()
                    }
                ),
                add_item_dialog.destroy()
            )
        )
        add_item_dialog.cancel_button = ttk.Button(add_item_dialog, text="Cancel", command=add_item_dialog.destroy)

        add_item_dialog.title_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        add_item_dialog.game_link_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        add_item_dialog.game_link_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=2, sticky="nsew")
        add_item_dialog.add_button.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
        add_item_dialog.cancel_button.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")

    def remove_item_ui(self):
        pass

    def insert_item_ui(self):
        pass

    def swap_items_ui(self):
        pass

    def shuffle_items_ui(self):
        pass
    
    def find_max_ui(self):
        pass

    def get_steam_details(self, detail:str, game_link:str):
        # extract the game's ID from the link, which is after app/
        if detail not in ["id", "name", "price"]:
            raise ValueError("Invalid detail requested.")

        game_id_match = re.search(r"app/(\d+)", game_link)
        if game_id_match is not None:
            game_id = int(game_id_match.group(1))
        else:
            raise ValueError("Invalid game link, or cannot find steam ID")
        url = f"https://store.steampowered.com/api/appdetails?appids={game_id}"
        api_response = requests.get(url, timeout=5)
        data = json.loads(api_response.text)

        if detail == "id":
            return game_id
        elif detail == "name":
            return data[str(game_id)]["data"]["name"]
        elif detail == "price":
            price = data[str(game_id)]["data"]["price_overview"]["final_formatted"]
            final_price = float(re.sub(r'[^\d.]+', '', price))
            return final_price
        else:
            raise ValueError("Invalid detail.")
    
    def change_database(self, action:str, game_id:int, data):
        if action not in ["add", "remove", "insert", "swap", "shuffle"]:
            raise ValueError("Invalid action.")

        if action == "add":
            data_to_add = {
                "game_id": game_id,
                "name": data["name"],
                "price": data["price"],
                "url": data["url"]
            }
            self.database.append(data_to_add)
        elif action == "remove":
            for i, item in enumerate(self.database):
                if item["game_id"] == game_id:
                    self.database.pop(i)
                    break
        elif action == "insert":
            data_to_insert = {
                "game_id": game_id,
                "name": data["name"],
                "price": data["price"],
                "url": data["url"]
            }
            self.database.insert(game_id, data_to_insert)
        
        self.update_treeview()
    
    def update_treeview(self):
        # delete everything in the treeview
        self.wishlist_display.delete(*self.wishlist_display.get_children())

        # add everything from the database to the treeview
        for i, data in enumerate(self.database):
            self.wishlist_display.insert(
                parent="",
                index=i,
                iid=i,
                text=data["game_id"],
                values=(
                    data["name"],
                    data["price"],
                    data["url"]
                )
            )
    
    def open_url(self, event):
        item = self.wishlist_display.selection()[0]
        url = self.wishlist_display.item(item, "values")[2]
        webbrowser.open(url)

if __name__ == "__main__":
    app = Wishlister()
    app.mainloop()
