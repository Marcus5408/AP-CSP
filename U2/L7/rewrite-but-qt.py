"""
A GUI application for managing a wishlist of Steam games, written in Python 3.12.0.

Theres also the replit version (https://replit.com/@Marcus5408/wishlisterer) but
tkinter kind of sucks on replit and it cuts off the buttons so i guess just copy
and paste from github (https://github.com/Marcus5408/AP-CSP/blob/main/U2/L7/rewrite.py)
and run it locally.
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem, QComboBox, QLineEdit, QSpinBox, QDialog, QMessageBox
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QMessageBox, QWidget
from PyQt5.QtCore import Qt
import json
import random
import re
import webbrowser
import requests

class Wishlister(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Wishlister v1.0.0")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(600, 300)

        # The main window's UI.
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.title_label = QLabel("Wishlister v1.0.0")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px;")

        self.add_button = QPushButton("Add Game", self)
        self.remove_button = QPushButton("Remove Game", self)
        self.insert_button = QPushButton("Insert Game", self)
        self.swap_button = QPushButton("Swap Games", self)
        self.shuffle_button = QPushButton("Shuffle Games", self)
        self.find_max_button = QPushButton("Find Max. Price", self)

        # initialize the Treeview that shows the wishlist
        self.wishlist_display = QTreeWidget(self)
        self.wishlist_display.setColumnCount(3)
        self.wishlist_display.setHeaderLabels(["Name", "Price", "URL"])

        # initialize the wishlist database. also the mandatory string and float lists.
        self.database = []
        self.mandatory_string_list = []
        self.mandatory_float_list = []

        # add the widgets to the main window
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addWidget(self.title_label)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)
        button_layout.addWidget(self.insert_button)
        button_layout.addWidget(self.swap_button)
        button_layout.addWidget(self.shuffle_button)
        button_layout.addWidget(self.find_max_button)

        self.central_layout.addLayout(button_layout)
        self.central_layout.addWidget(self.wishlist_display)

        # allow double-clicking on items
        self.wishlist_display.itemDoubleClicked.connect(self.open_url)

        self.add_button.clicked.connect(self.add_item_ui)
        self.remove_button.clicked.connect(self.remove_item_ui)
        self.insert_button.clicked.connect(self.insert_item_ui)
        self.swap_button.clicked.connect(self.swap_items_ui)
        self.shuffle_button.clicked.connect(self.shuffle_items_ui)
        self.find_max_button.clicked.connect(self.find_max_ui)

    def add_item_ui(self):
        """
        Opens a dialog to add a new game to the wishlist database.
        """
        add_item_dialog = QDialog(self)
        add_item_dialog.setWindowTitle("Add Game")
        add_item_dialog.setGeometry(200, 200, 400, 100)
        add_item_dialog.setFixedSize(400, 200)

        add_item_layout = QVBoxLayout(add_item_dialog)

        add_item_label = QLabel("Add Game")
        add_item_label.setStyleSheet("font-size: 12px;")

        game_link_label = QLabel("Game Link:")
        game_link_entry = QLineEdit()

        add_button = QPushButton("Add", add_item_dialog)
        cancel_button = QPushButton("Cancel", add_item_dialog)

        add_button.clicked.connect(lambda: self.change_database(
            action="add",
            game_id=self.get_steam_details("id", game_link_entry.text()),
            data={
                "game_id": self.get_steam_details("id", game_link_entry.text()),
                "name": self.get_steam_details("name", game_link_entry.text()),
                "price": self.get_steam_details("price", game_link_entry.text()),
                "url": game_link_entry.text()
            }
        ))
        add_button.clicked.connect(add_item_dialog.accept)

        cancel_button.clicked.connect(add_item_dialog.reject)

        add_item_layout.addWidget(add_item_label)
        add_item_layout.addWidget(game_link_label)
        add_item_layout.addWidget(game_link_entry)
        add_item_layout.addWidget(add_button)
        add_item_layout.addWidget(cancel_button)

        add_item_dialog.exec()

    def remove_item_ui(self):
        """
        Opens a dialog to remove a game from the wishlist database.
        """
        remove_item_dialog = QDialog(self)
        remove_item_dialog.setWindowTitle("Remove Game")
        remove_item_dialog.setGeometry(200, 200, 200, 150)
        remove_item_dialog.setFixedSize(200, 150)

        remove_item_layout = QVBoxLayout(remove_item_dialog)

        remove_item_label = QLabel("Remove Game")
        remove_item_label.setStyleSheet("font-size: 12px;")

        listbox = QComboBox()
        for item in self.wishlist_display.findItems("", Qt.MatchContains):
            listbox.addItem(item.text(0))

        ok_button = QPushButton("OK", remove_item_dialog)
        cancel_button = QPushButton("Cancel", remove_item_dialog)

        ok_button.clicked.connect(lambda: self.change_database(
            action="remove",
            game_id=self.get_game_id(listbox.currentText()),
            data={}
        ))
        ok_button.clicked.connect(remove_item_dialog.accept)

        cancel_button.clicked.connect(remove_item_dialog.reject)

        remove_item_layout.addWidget(remove_item_label)
        remove_item_layout.addWidget(listbox)
        remove_item_layout.addWidget(ok_button)
        remove_item_layout.addWidget(cancel_button)

        remove_item_dialog.exec()

    def insert_item_ui(self):
        """
        Opens a dialog to insert a new game into the wishlist database.
        """
        insert_item_dialog = QDialog(self)
        insert_item_dialog.setWindowTitle("Insert Game")
        insert_item_dialog.setGeometry(200, 200, 400, 150)
        insert_item_dialog.setFixedSize(400, 200)

        insert_item_layout = QVBoxLayout(insert_item_dialog)

        insert_item_label = QLabel("Insert Game")
        insert_item_label.setStyleSheet("font-size: 12px;")

        game_link_label = QLabel("Game Link:")
        game_link_entry = QLineEdit()

        position_label = QLabel("Position:")
        position_spinbox = QSpinBox()
        position_spinbox.setMinimum(1)
        position_spinbox.setMaximum(len(self.database) + 1)

        ok_button = QPushButton("OK", insert_item_dialog)
        cancel_button = QPushButton("Cancel", insert_item_dialog)

        ok_button.clicked.connect(lambda: self.change_database(
            action="insert",
            game_id=self.get_steam_details("id", game_link_entry.text()),
            data={
                "position": position_spinbox.value(),
                "game_id": self.get_steam_details("id", game_link_entry.text()),
                "name": self.get_steam_details("name", game_link_entry.text()),
                "price": self.get_steam_details("price", game_link_entry.text()),
                "url": game_link_entry.text()
            }
        ))
        ok_button.clicked.connect(insert_item_dialog.accept)

        cancel_button.clicked.connect(insert_item_dialog.reject)

        insert_item_layout.addWidget(insert_item_label)
        insert_item_layout.addWidget(game_link_label)
        insert_item_layout.addWidget(game_link_entry)
        insert_item_layout.addWidget(position_label)
        insert_item_layout.addWidget(position_spinbox)
        insert_item_layout.addWidget(ok_button)
        insert_item_layout.addWidget(cancel_button)

        insert_item_dialog.exec()

    def swap_items_ui(self):
        """
        Opens a dialog to swap the positions of two games in the wishlist database.
        """
        swap_items_dialog = QDialog(self)
        swap_items_dialog.setWindowTitle("Swap Games")
        swap_items_dialog.setGeometry(200, 200, 310, 200)
        swap_items_dialog.setFixedSize(310, 200)

        swap_items_layout = QVBoxLayout(swap_items_dialog)

        swap_items_label = QLabel("Swap Items")
        swap_items_label.setStyleSheet("font-size: 12px;")

        item1_label = QLabel("Item 1:")
        item2_label = QLabel("Item 2:")

        first_item = QComboBox()
        second_item = QComboBox()

        for item in self.wishlist_display.findItems("", Qt.MatchContains):
            first_item.addItem(item.text(0))
            second_item.addItem(item.text(0))

        ok_button = QPushButton("OK", swap_items_dialog)
        cancel_button = QPushButton("Cancel", swap_items_dialog)

        ok_button.clicked.connect(lambda: self.change_database(
            action="swap",
            game_id=None,
            data={
                "name1": first_item.currentText(),
                "name2": second_item.currentText()
            }
        ))
        ok_button.clicked.connect(swap_items_dialog.accept)

        cancel_button.clicked.connect(swap_items_dialog.reject)

        swap_items_layout.addWidget(swap_items_label)
        swap_items_layout.addWidget(item1_label)
        swap_items_layout.addWidget(first_item)
        swap_items_layout.addWidget(item2_label)
        swap_items_layout.addWidget(second_item)
        swap_items_layout.addWidget(ok_button)
        swap_items_layout.addWidget(cancel_button)

        swap_items_dialog.exec()

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
        QMessageBox.information(self, "Most Expensive Game", message)

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
        # Clear everything from the QTreeWidget
        self.wishlist_display.clear()

        # Add everything from the database to the QTreeWidget
        for i, data in enumerate(self.database):
            price_data = float(data["price"])
            item = QTreeWidgetItem(self.wishlist_display)
            item.setText(0, str(data["game_id"]))
            item.setText(1, data["name"])
            item.setText(2, f"${price_data:.2f}")
            item.setText(3, data["url"])

        # Update the mandatory string and float lists
        self.mandatory_string_list = [data["name"] for data in self.database]
        self.mandatory_float_list = [data["price"] for data in self.database]
        print(f"The strings!! : {self.mandatory_string_list}\n The floats!! : {self.mandatory_float_list}")

    def open_url(self):
        """
        Opens the URL of the selected item in the user's default web browser.
        """
        selected_items = self.wishlist_display.selectedItems()
        if selected_items:
            item = selected_items[0]
            url = item.text(3)  # Assuming URL is in the fourth column (index 3)
            webbrowser.open(url)
        else:
            QMessageBox.warning(self, "No Item Selected", "Please select an item to open its URL.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Wishlister()
    window.show()
    sys.exit(app.exec())