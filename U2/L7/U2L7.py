from os import link, path, mkdir, listdir
from io import BytesIO
import re
import json
from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem
from PySide6.QtGui import QIcon, QPixmap, QImage
from PySide6.QtCore import Qt
import requests
from PIL import Image
from fuzzywuzzy import fuzz

app = QApplication([])

# Create a QTableWidget object
wishlist_display = QTableWidget()
wishlist_display.setColumnCount(5)
wishlist_display.setHorizontalHeaderLabels(["#", "Banner", "Name", "Price", "URL"])
database = []

if not path.exists(f"{path.dirname(__file__)}/storage"):
    mkdir(f"{path.dirname(__file__)}/storage")


class GameNotFoundException(Exception):
    """Exception raised when the game is not found in the Steam API."""

    def __init__(self, steam_id, message="Game not found"):
        self.steam_id = steam_id
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.steam_id} -> {self.message}"


def fuzzmatch_files(directory, target_text, threshold=70):
    matched_files = []
    for filename in listdir(directory):
        if filename.endswith('.txt'):
            with open(path.join(directory, filename), 'r') as file:
                file_content = file.read()
                if fuzz.ratio(file_content, target_text) >= threshold:
                    matched_files.append(filename)
    return matched_files


def get_steam_details(steam_id: str):
    # Steam API endpoint
    url = f"https://store.steampowered.com/api/appdetails?appids={steam_id}"
    api_response = requests.get(url, timeout=5)
    data = json.loads(api_response.text)

    # Check if the request was successful
    if data[str(steam_id)]["success"]:
        # Get the game's name
        steam_name = data[str(steam_id)]["data"]["name"]
        steam_price = data[str(steam_id)]["data"]["price_overview"]["final_formatted"]
        valid_game = True
    else:
        raise GameNotFoundException(link)

    # Get the game's banner image
    steam_banner_url = (
        f"https://cdn.cloudflare.steamstatic.com/steam/apps/{steam_id}/header.jpg"
    )
    api_response = requests.get(steam_banner_url, timeout=5)
    steam_banner_image = Image.open(BytesIO(api_response.content))
    steam_banner_image.save(f"{steam_name}_banner.png")
    steam_banner_pixmap = QPixmap(f"{steam_name}_banner.png")

    database.append(data)

    return steam_name, steam_price, steam_banner_pixmap, valid_game


#    # Add the game to the table with the banner image
#    item = QTableWidgetItem(wishlist_display)
#    item.setText(0, game_name)
#    item.setText(1, game_price)
#    item.setText(2, link)
#    item.setIcon(3, QIcon(banner_pixmap))
#

# example game link: https://store.steampowered.com/app/2449040/Cursorblade/
# extract the game's ID from the link, which is after app/
game_link = "https://store.steampowered.com/app/2449040/Cursorblade/"


def add_game_online():
    game_id_match = re.search(r"app/(\d+)", game_link)
    if game_id_match is not None:
        game_id = int(
            game_id_match.group(1)
        )  # Extract the matched string and convert it to an integer
    else:
        raise ValueError("Invalid game link")
    game_name, game_price, banner_pixmap, game_found = get_steam_details(str(game_id))
    # Check if the request was successful
    if game_found:
        # Get the game's banner image URL
        banner_url = database[len(database) - 1][str(game_id)]["data"]["header_image"]

        # Download, save, and prep the banner image to be put in the UI
        response = requests.get(banner_url, timeout=5)
        banner_image = Image.open(BytesIO(response.content))
        banner_image.save(f"{path.dirname(__file__)}/storage/{game_name}_banner.png")
        banner_image = QImage().load(f"{path.dirname(__file__)}/storage/{game_name}_banner.png")

        # Add the game to the table with the banner image
        num_rows = wishlist_display.rowCount()
        row = wishlist_display.rowCount()
        wishlist_display.insertRow(row)

        item = QTableWidgetItem()
        wishlist_display.setItem(row, 0, item)
        item.setText(str(len(database) - 1))

        item = QTableWidgetItem()
        item.setData(Qt.DecorationRole, QPixmap.fromImage(QImage()))
        wishlist_display.setItem(row, 1, item)

        item = QTableWidgetItem()
        wishlist_display.setItem(row, 2, item)
        item.setText(game_name)

        item = QTableWidgetItem()
        wishlist_display.setItem(row, 3, item)
        item.setText(game_price)

        item = QTableWidgetItem()
        wishlist_display.setItem(row, 4, item)
        item.setText(game_link)


add_game_online()

wishlist_display.show()

app.exec()
