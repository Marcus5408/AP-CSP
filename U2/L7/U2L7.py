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
wishlist_display.setColumnCount(4)
wishlist_display.setHeaderLabels(["Name", "Price", "Link", "Banner"])

database = []

class GameNotFoundException(Exception):
    """Exception raised when the game is not found in the Steam API."""

    def __init__(self, game_id, message="Game not found"):
        self.game_id = game_id
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.game_id} -> {self.message}'

def get_steam_details(game_id:str):
    # Steam API endpoint
    url = f"http://store.steampowered.com/api/appdetails?appids={game_id}"
    response = requests.get(url)
    data = json.loads(response.text)

    # Check if the request was successful
    if data[str(game_id)]["success"]:
        # Get the game's name
        game_name = data[str(game_id)]["data"]["name"]
        game_price = data[str(game_id)]["data"]["price_overview"]["final_formatted"]
        game_found = True
    else:
        raise GameNotFoundException(link)

    # Get the game's banner image
    banner_url = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{game_id}/header.jpg"
    response = requests.get(banner_url, timeout=5)
    banner_image = Image.open(BytesIO(response.content))
    banner_image.save(f"{game_name}_banner.png")
    banner_pixmap = QPixmap(f"{game_name}_banner.png")

    database.append(data)

    return game_name, game_price, banner_pixmap, game_found


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
    print(database)
    banner_url = database[len(database) - 1]["data"]["header_image"]

    # Download the banner image
    response = requests.get(banner_url, timeout=5)
    banner_image = Image.open(BytesIO(response.content))

    # Save the banner image
    banner_image.save(f"{game_name}_banner.png")

    # Create a QPixmap object for the banner image
    banner_pixmap = QPixmap(f"{game_name}_banner.png")

    # Add the game to the treeview with the banner image
    item = QTreeWidgetItem(wishlist_display)
    item.setText(0, game_name)
    item.setText(1, game_price)
    item.setText(2, game_link)
    item.setIcon(3, QIcon(banner_pixmap))

database.append((game_name, game_price, link))

# Add the game to the treeview
item = QTreeWidgetItem(wishlist_display)
item.setText(0, str(len(database) - 1))
item.setText(1, game_price)
item.setText(2, game_link)

wishlist_display.show()

app.exec_()
