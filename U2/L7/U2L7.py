from os import link
from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import requests
from PIL import Image
from io import BytesIO
import re
import json

app = QApplication([])

# Create a QTreeWidget object
wishlist_display = QTreeWidget()
wishlist_display.setColumnCount(5)
wishlist_display.setHeaderLabels(["#", "Banner", "Name", "Price", "URL"])

database = []

class GameNotFoundException(Exception):
    """Exception raised when the game is not found in the Steam API."""

    def __init__(self, steam_id, message="Game not found"):
        self.steam_id = steam_id
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.steam_id} -> {self.message}'

def get_steam_details(steam_id:str):
    # Steam API endpoint
    url = f"http://store.steampowered.com/api/appdetails?appids={steam_id}"
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
    steam_banner_url = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{steam_id}/header.jpg"
    api_response = requests.get(steam_banner_url, timeout=5)
    steam_banner_image = Image.open(BytesIO(api_response.content))
    steam_banner_image.save(f"{steam_name}_banner.png")
    steam_banner_pixmap = QPixmap(f"{steam_name}_banner.png")

    database.append(data)

    return steam_name, steam_price, steam_banner_pixmap, valid_game


#    # Add the game to the treeview with the banner image
#    item = QTreeWidgetItem(wishlist_display)
#    item.setText(0, game_name)
#    item.setText(1, game_price)
#    item.setText(2, link)
#    item.setIcon(3, QIcon(banner_pixmap))
#

# example game link: https://store.steampowered.com/app/2449040/Cursorblade/
# extract the game's ID from the link, which is after app/
game_link = "https://store.steampowered.com/app/2449040/Cursorblade/"
game_id_match = re.search(r'app/(\d+)', game_link)
if game_id_match is not None:
    game_id = int(game_id_match.group(1))  # Extract the matched string and convert it to an integer
else:
    raise ValueError("Invalid game link")

game_name, game_price, banner_pixmap, game_found = get_steam_details(str(game_id))

# Check if the request was successful
if game_found:
    # Get the game's banner image URL
    banner_url = database[len(database) - 1][str(game_id)]["data"]["header_image"]

    # Download the banner image
    response = requests.get(banner_url, timeout=5)
    banner_image = Image.open(BytesIO(response.content))

    # Save the banner image
    banner_image.save(f"{game_name}_banner.png")

    # Create a QPixmap object for the banner image
    banner_pixmap = QPixmap(f"{game_name}_banner.png")
    banner_pixmap = banner_pixmap.scaled(128, 128, Qt.KeepAspectRatio)

    # Add the game to the treeview with the banner image
    item = QTreeWidgetItem(wishlist_display)
    item.setText(0, str(len(database) - 1))
    item.setIcon(1, QIcon(banner_pixmap))
    item.setText(2, game_name)
    item.setText(3, game_price)
    item.setText(4, game_link)

wishlist_display.show()

app.exec_()
