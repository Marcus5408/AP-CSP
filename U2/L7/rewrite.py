"""
A GUI application for managing a wishlist of Steam games, written in Python 3.12.0.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
import re
import webbrowser
import requests

class Wishlister(tk.Tk):
    """
    A GUI application for managing a wishlist of Steam games.
    """
    def __init__(self):
        super().__init__()
        self.title("Wishlister v1.0.0")
        self.geometry("800x600")
        self.minsize(600, 300)

        # The main window's UI.
        self.title_label = ttk.Label(text="Wishlister v1.0.0")
        self.title_label.config(font=("Arial", 24))
        self.add_button = ttk.Button(text="Add Game", command=self.add_item_ui)
        self.remove_button = ttk.Button(text="Remove Game", command=self.remove_item_ui)
        self.insert_button = ttk.Button(text="Insert Game", command=self.insert_item_ui)
        self.swap_button = ttk.Button(text="Swap Games", command=self.swap_items_ui)
        self.shuffle_button = ttk.Button(text="Shuffle Games", command=self.shuffle_items_ui)
        self.find_max_button = ttk.Button(text="Find Max. Price", command=self.find_max_ui)

        # initialize the Treeview that shows the wishlist
        self.wishlist_display = ttk.Treeview()
        self.wishlist_display["columns"] = ("Game", "Price", "URL")
        self.wishlist_display.heading("#0", text="Steam ID")
        self.wishlist_display.heading("Game", text="Name")
        self.wishlist_display.heading("Price", text="Price")
        self.wishlist_display.heading("URL", text="URL")
        self.wishlist_display.column("#0", width=40)
        self.wishlist_display.column("Game", width=200)
        self.wishlist_display.column("Price", width=75)

        # initialize the wishlist database. also the mandatory string and float lists.
        self.database = []
        self.mandatory_string_list = []
        self.mandatory_float_list = []

        # add the widgets to the main window
        self.title_label.grid(row=0, column=0, columnspan=6, padx=5, pady=5, sticky="nsew")
        self.add_button.grid(row=1, column=0, padx=5, pady=(0,5), sticky="nsew")
        self.remove_button.grid(row=1, column=1, padx=(0,5), pady=(0,5), sticky="nsew")
        self.insert_button.grid(row=1, column=2, padx=(0,5), pady=(0,5), sticky="nsew")
        self.swap_button.grid(row=1, column=3, padx=(0,5), pady=(0,5), sticky="nsew")
        self.shuffle_button.grid(row=1, column=4, padx=(0,5), pady=(0,5), sticky="nsew")
        self.find_max_button.grid(row=1, column=5, padx=(0,5), pady=(0,5), sticky="nsew")
        self.wishlist_display.grid(row=2, column=0, columnspan=6, padx=5, pady=(0,5), sticky="nsew")
        
        # configure the grid and allow double-clicking on links
        for i in range(6):
            self.columnconfigure(i, weight=1)
        self.rowconfigure(2, weight=1)
        self.wishlist_display.bind("<Double-1>", self.open_url)

    def add_item_ui(self):
        """
        Opens a dialog to add a new game to the wishlist database.
        """
        add_item_dialog = tk.Toplevel(self)
        add_item_dialog.title("Add Game")
        add_item_dialog.geometry("400x100")
        add_item_dialog.minsize(400, 100)
        add_item_dialog.resizable(False, False)

        # Create widgets for the dialog
        add_item_dialog.title_label = ttk.Label(add_item_dialog, text="Add Game")
        add_item_dialog.title_label.config(font=("Arial", 12))
        add_item_dialog.game_link_label = ttk.Label(add_item_dialog, text="Game Link:", width=11)
        add_item_dialog.game_link_entry = ttk.Entry(add_item_dialog, width=50)
        # this button does basically everything. it gets the game's ID, name, and price from the steam API
        # and adds it to the database.
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

        # Add the widgets to the dialog
        add_item_dialog.title_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        add_item_dialog.game_link_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        add_item_dialog.game_link_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=2, sticky="nsew")
        add_item_dialog.add_button.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
        add_item_dialog.cancel_button.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")

        # configure the grid
        for i in range(2):
            add_item_dialog.columnconfigure(i, weight=1)

    def remove_item_ui(self):
        """
        Opens a dialog to remove a game from the wishlist database.
        """
        remove_item_dialog = tk.Toplevel(self)
        remove_item_dialog.title("Remove Game")
        remove_item_dialog.geometry("200x300")
        remove_item_dialog.minsize(200, 300)
        remove_item_dialog.resizable(False, False)

        # Create widgets for the dialog
        remove_item_dialog.title_label = ttk.Label(remove_item_dialog, text="Remove Game")
        remove_item_dialog.title_label.config(font=("Arial", 12))
        # listbox for the user to select the item to remove
        listbox = tk.Listbox(remove_item_dialog)
        for item in self.wishlist_display.get_children():
            listbox.insert(tk.END, self.wishlist_display.item(item)["values"][0])
        ok_button = ttk.Button(
            remove_item_dialog,
            text="OK",
            command=lambda: (
                self.change_database(
                    action="remove",
                    # get_game_id is only used here. it's not used anywhere else.
                    # it gets the game_id based on the name of a game.
                    game_id=self.get_game_id(listbox.get(tk.ACTIVE)),
                    data={}
                ),
                remove_item_dialog.destroy()
            )
        )
        cancel_button = ttk.Button(remove_item_dialog, text="Cancel", command=remove_item_dialog.destroy)

        # Add the widgets to the dialog
        remove_item_dialog.title_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        listbox.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        ok_button.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        cancel_button.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        # configure the grid
        for i in range(2):
            remove_item_dialog.columnconfigure(i, weight=1)
        remove_item_dialog.rowconfigure(1, weight=1)

    def get_game_id(self, game_name):
        """
        Gets the game_id of a game based on its name.
        """
        for item in self.database:
            if item["name"] == game_name:
                return item["game_id"]
        return None

    def insert_item_ui(self):
        """
        Opens a dialog to insert a new game into the wishlist database.
        """
        insert_item_dialog = tk.Toplevel(self)
        insert_item_dialog.title("Insert Game")
        insert_item_dialog.geometry("400x150")
        insert_item_dialog.minsize(400, 150)
        insert_item_dialog.resizable(False, False)

        # Create widgets for the dialog
        insert_item_dialog.title_label = ttk.Label(insert_item_dialog, text="Insert Game")
        insert_item_dialog.title_label.config(font=("Arial", 12))
        insert_item_dialog.game_link_label = ttk.Label(insert_item_dialog, text="Game Link:", width=11)
        insert_item_dialog.game_link_entry = ttk.Entry(insert_item_dialog, width=50)
        insert_item_dialog.game_position_label = ttk.Label(insert_item_dialog, text="Position:", width=11)
        insert_item_dialog.game_position_spinbox = tk.Spinbox(insert_item_dialog, from_=1, to=len(self.database) + 1, width=48)
        # Create an "OK" button that inserts the new item when clicked
        ok_button = ttk.Button(
            insert_item_dialog,
            text="OK",
            command=lambda: (
                self.change_database(
                    action="insert",
                    game_id=self.get_steam_details("id", insert_item_dialog.game_link_entry.get()),  # Get the entered item
                    data={
                        "position": insert_item_dialog.game_position_spinbox.get(),
                        "game_id": self.get_steam_details("id", insert_item_dialog.game_link_entry.get()),
                        "name": self.get_steam_details("name", insert_item_dialog.game_link_entry.get()),
                        "price": self.get_steam_details("price", insert_item_dialog.game_link_entry.get()),
                        "url": insert_item_dialog.game_link_entry.get()
                    }
                ),
                insert_item_dialog.destroy()
            )
        )
        cancel_button = ttk.Button(insert_item_dialog, text="Cancel", command=insert_item_dialog.destroy)

        # Add the widgets to the dialog
        insert_item_dialog.title_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        insert_item_dialog.game_link_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        insert_item_dialog.game_link_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="nsew")
        insert_item_dialog.game_position_label.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        insert_item_dialog.game_position_spinbox.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="nsew")
        ok_button.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")
        cancel_button.grid(row=3, column=2, padx=5, pady=5, sticky="nsew")

    def swap_items_ui(self):
        """
        Opens a dialog to swap the positions of two games in the wishlist database.
        """
        swap_items_dialog = tk.Toplevel(self)
        swap_items_dialog.title("Swap Games")
        swap_items_dialog.geometry("310x150")
        swap_items_dialog.minsize(310, 150)
        swap_items_dialog.resizable(False, False)
        
        # Create widgets for the dialog
        swap_items_dialog.title_label = tk.Label(swap_items_dialog, text="Swap Items", font=("Arial", 12))
        swap_items_dialog.item1_label = tk.Label(swap_items_dialog, text="Item 1:")
        swap_items_dialog.item2_label = tk.Label(swap_items_dialog, text="Item 2:")
        swap_items_dialog.first_item = ttk.Combobox(swap_items_dialog, values=[self.wishlist_display.item(item)["values"][0] for item in self.wishlist_display.get_children()])
        swap_items_dialog.second_item = ttk.Combobox(swap_items_dialog, values=[self.wishlist_display.item(item)["values"][0] for item in self.wishlist_display.get_children()])
        # Create an "OK" button that swaps the selected items when clicked
        ok_button = ttk.Button(
            swap_items_dialog,
            text="OK",
            command=lambda: (
                self.change_database(
                    action="swap",
                    game_id=None,
                    data={
                        "name1":swap_items_dialog.first_item.get(),
                        "name2":swap_items_dialog.second_item.get()
                    }
                ),
                swap_items_dialog.destroy()
            )
        )
        cancel_button = ttk.Button(swap_items_dialog, text="Cancel", command=swap_items_dialog.destroy)

        # Add the widgets to the dialog
        swap_items_dialog.title_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        swap_items_dialog.item1_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        swap_items_dialog.item2_label.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        swap_items_dialog.first_item.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        swap_items_dialog.second_item.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
        ok_button.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
        cancel_button.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")


    def shuffle_items_ui(self):
        """
        Shuffles the database. No dialog needed.
        """
        self.change_database(action="shuffle", game_id=None, data={})

    def find_max_ui(self):
        """
        Finds the most expensive game in the database and displays a message box with the result.
        """
        max_price = 0
        max_game_name = ""
        for item in self.database:
            game_name = item["name"]
            game_link = item["url"]
            price = float(self.get_steam_details("price", game_link))
            if price > max_price:
                max_price = price
                max_game_name = game_name
        message = f"The most expensive game is {max_game_name} with a price of ${max_price:.2f}"
        messagebox.showinfo("Most Expensive Game", message, icon="info")

    def get_steam_details(self, detail:str, game_link:str):
        """
        Gets the details of a game from the Steam API.
        """
        # exit if the detail requested is invalid
        if detail not in ["id", "name", "price"]:
            raise ValueError("Invalid detail requested.")
        
        # get the game's ID from the link
        game_id_match = re.search(r"app/(\d+)", game_link)
        if game_id_match is not None:
            game_id = int(game_id_match.group(1))
        else:
            raise ValueError("Invalid game link, or cannot find steam ID")
        # get the game's details from the API
        url = f"https://store.steampowered.com/api/appdetails?appids={game_id}"
        api_response = requests.get(url, timeout=5)
        data = json.loads(api_response.text)

        # parse out specific details from the API response
        if detail == "id":
            return game_id
        elif detail == "name":
            return data[str(game_id)]["data"]["name"]
        elif detail == "price":
            # convert to str because API returns "true" rather than "True"
            if data[str(game_id)]["data"]["is_free"]:
                return "0.00"
            else:
                price = data[str(game_id)]["data"]["price_overview"]["final"]
                final_price = float(f"{price/100:.2f}")
                # final_price = f"${price/100:.2f}"
                return final_price
        else:
            raise ValueError("Invalid detail.")
    
    def add_item_to_database(self, game_id:int, data:dict):
        """
        Adds an item to the database.

        Args:
        - game_id (int): the ID of the game to add
        - data (dict): a dictionary containing the name, price, and URL of the game to add
        """
        data_to_add = {
            "game_id": game_id,
            "name": data["name"],
            "price": data["price"],
            "url": data["url"]
        }
        self.database.append(data_to_add)

    def remove_item_from_database(self, game_id:int):
        """
        Removes an item from the database.

        Args:
        - game_id (int): the ID of the game to remove
        """
        for i, item in enumerate(self.database):
            if item["game_id"] == game_id:
                self.database.pop(i)
                break
        else:
            raise ValueError("Item not found in database.")

    def insert_item_into_database(self, game_id:int, data:dict):
        """
        Inserts an item into the database at the specified position.

        Args:
        - game_id (int): the ID of the game to add
        - data (dict): a dictionary containing the name, price, URL, and position of the game to add
        """
        position = int(data.get("position"))
        if position is None:
            raise ValueError("Invalid data parameter. 'position' key is required.")
        data_to_insert = {
            "game_id": game_id,
            "name": data["name"],
            "price": data["price"],
            "url": data["url"]
        }
        self.database.insert(position - 1, data_to_insert)

    def swap_items_in_database(self, name1:str, name2:str):
        """
        Swaps the positions of two items in the database.

        Args:
        - name1 (str): the name of the first item to swap
        - name2 (str): the name of the second item to swap
        """
        # find the indices of the items to swap
        index1 = None
        index2 = None
        for i, item in enumerate(self.database):
            if item["name"] == name1:
                index1 = i
            elif item["name"] == name2:
                index2 = i
            if index1 is not None and index2 is not None:
                break
        if index1 is None or index2 is None:
            raise ValueError("Invalid game names. Game names must be in the database.")
        # swap the items
        self.database[index1], self.database[index2] = self.database[index2], self.database[index1]

    def shuffle_database(self):
        """
        Shuffles the items in the database randomly. that's it.
        """
        random.shuffle(self.database)

    def change_database(self, action:str, game_id:int, data):
        """
        Changes the database based on the specified action.

        Args:
        - action (str): the action to perform on the database (add, remove, insert, swap, shuffle)
        - game_id (int): the ID of the game to modify
        - data (dict): a dictionary containing the data needed to perform the specified action
        """
        # make sure requested action on the database is valid
        if action not in ["add", "remove", "insert", "swap", "shuffle"]:
            raise ValueError("Invalid action.")

        # perform the requested action
        if action == "add":
            self.add_item_to_database(game_id, data)
        elif action == "remove":
            self.remove_item_from_database(game_id)
        elif action == "insert":
            self.insert_item_into_database(game_id, data)
        elif action == "swap":
            name1 = data.get("name1")
            name2 = data.get("name2")
            if name1 is None or name2 is None:
                raise ValueError("Invalid data parameter. 'name1' and 'name2' keys are required.")
            self.swap_items_in_database(name1, name2)
        elif action == "shuffle":
            self.shuffle_database()

        # update what the user sees
        self.update_treeview()

    def update_treeview(self):
        """
        Updates the treeview display with the current database information.
        """
        # delete everything from the treeview
        self.wishlist_display.delete(*self.wishlist_display.get_children())

        # add everything from the database to the treeview
        for i, data in enumerate(self.database):
            price_data = float(data["price"])
            self.wishlist_display.insert(
                parent="",
                index=i,
                iid=i,
                text=data["game_id"],
                values=(
                    data["name"],
                    f"${price_data:.2f}",
                    data["url"]
                )
            )
        
        # update the mandatory string and float lists. i think its good enough?
        self.mandatory_string_list = [data["name"] for data in self.database]
        self.mandatory_float_list = [data["price"] for data in self.database]
        print(f"The strings!! : {self.mandatory_string_list}\n The floats!! : {self.mandatory_float_list}")
    
    def open_url(self):
        """
        Opens the URL of the selected item in the user's default web browser.
        """
        item = self.wishlist_display.selection()[0]
        url = self.wishlist_display.item(item, "values")[2]
        webbrowser.open(url)

if __name__ == "__main__":
    app = Wishlister()
    app.mainloop()
