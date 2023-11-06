import time
import tkinter as tk
from tkinter import ttk
import watchdog_reloader
import requests
from PIL import Image, ImageTk
from io import BytesIO

database = []

root = tk.Tk()
root.title("Wishlister")
root.geometry("700x600")

# Create a label for the title
title_label = tk.Label(root, text="Wishlister", font=("Helvetica", 16))
title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(10,5))

wishlist_display = ttk.Treeview(root, columns=("Name", "Price", "Link", "Banner"))
wishlist_display.heading("#0", text="#")
wishlist_display.heading("#1", text="Name")
wishlist_display.heading("#2", text="Price")
wishlist_display.heading("#3", text="Link")
wishlist_display.heading("#4", text="Banner")
wishlist_display.column("#0", width=20)
wishlist_display.column("#1", width=195)
wishlist_display.column("#2", width=95)
wishlist_display.column("#3", width=370)
wishlist_display.column("#4", width=100)
wishlist_display.grid(row=1, column=0, columnspan=2, padx=10, pady=(5, 5))

def add_game():
    """
    Create a new window to add a game to the wishlist.

    Args: None
    Returns: None
    """
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

    name_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
    name_entry.grid(row=0, column=1, padx=10, pady=(10, 5))
    price_label.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="w")
    price_entry.grid(row=1, column=1, padx=10, pady=(0, 5))
    link_label.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="w")
    link_entry.grid(row=2, column=1, padx=10, pady=(0, 5))

    add_button = ttk.Button(
        add_window,
        text="Add Game",
        command=lambda: add_to_db(
            name_entry.get(), price_entry.get(), link_entry.get()
        ),
    )
    add_button.grid(row=3, column=1, padx=10, pady=(5, 10), sticky="e")

add_game_button = ttk.Button(root, text="+", command=add_game)
add_game_button.grid(row=2, column=1, padx=10, pady=(5, 10), sticky="e")

def add_to_db(name, price, link):
    """
    Add a game to the database and the treeview.

    Args:
        name (str): The name of the game.
        price (str): The price of the game.
        link (str): The link to the game.

    Returns: None
    """
    # Get the game's Steam ID from the link
    steam_id = link.split("/")[4]

    # Use the Steam Storefront API to get the game's information
    response = requests.get(f"http://store.steampowered.com/api/appdetails?appids={steam_id}", timeout=5)
    data = response.json()

    # Check if the request was successful
    if data[steam_id]["success"]:
        # Get the game's banner image URL
        banner_url = data[steam_id]["data"]["header_image"]

        # Download the banner image
        response = requests.get(banner_url, timeout=5)
        banner_image = Image.open(BytesIO(response.content))

        # Save the banner image
        banner_image.save(f"{name}_banner.png")

        # Create a PhotoImage object for the banner image
        banner_photo = ImageTk.PhotoImage(banner_image)

        # Add the game to the treeview with the banner image
        wishlist_display.insert(
            parent= "",
            index= "end",
            values=(name, price, link, banner_photo)
        )

        # Keep a reference to the image to prevent garbage collection
        treeview.image = banner_photo

    database.append((name, price, link))

    # Add the game to the treeview
    wishlist_display.insert(
        parent="",
        index="end",
        iid=len(database) - 1,
        text=str(len(database) - 1),
        values=(price, link),
    )

# watchdog_reloader.start(root)
root.mainloop() # this will be uncommented once we stop using watchdog
