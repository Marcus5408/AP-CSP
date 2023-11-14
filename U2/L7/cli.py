import click
import random

# Function to add an item to the collection
def add_item(names, values, name, value):
    names.append(name)
    values.append(value)
    click.echo("Item added successfully!")

# Function to remove an item from the collection
def remove_item(names, values, index):
    if 0 <= index < len(names):
        names.pop(index)
        values.pop(index)
        click.echo("Item removed successfully!")
    else:
        click.echo("Invalid item number.")

# Function to insert an item into the collection
def insert_item(names, values, index, name, value):
    if 0 <= index <= len(names):
        names.insert(index, name)
        values.insert(index, value)
        click.echo("Item inserted successfully!")
    else:
        click.echo("Invalid location.")

# Function to swap two items in the collection
def swap_items(names, values, index1, index2):
    if 0 <= index1 < len(names) and 0 <= index2 < len(names):
        names[index1], names[index2] = names[index2], names[index1]
        values[index1], values[index2] = values[index2], values[index1]
        click.echo("Items swapped successfully!")
    else:
        click.echo("Invalid item numbers.")

# Function to search for the item with the maximum value
def search_max(names, values):
    if not names:
        click.echo("Collection is empty.")
    else:
        max_index = values.index(max(values))
        click.echo(f"The item with the maximum value is: {names[max_index]} ({values[max_index]})")

# Function to print the full collection
def print_collection(names, values):
    if not names:
        click.echo("Collection is empty.")
    else:
        click.echo("Full Collection:")
        for i, (name, value) in enumerate(zip(names, values), start=1):
            click.echo(f"{i}. {name} ({value})")

# Function to shuffle the collection
def shuffle_collection(names, values):
    if not names:
        click.echo("Collection is empty.")
    else:
        combined = list(zip(names, values))
        random.shuffle(combined)
        names[:], values[:] = zip(*combined)
        click.echo("Collection shuffled successfully!")

# @click.command()
@click.group()
@click.option('--name', prompt='Enter the item name', help='Name of the item to add')
@click.option('--value', prompt='Enter the associated number', type=float, help='Associated number of the item')
@click.option('--index', type=int, help='Index of the item in the collection')
@click.option('--index1', type=int, help='Index of the first item to swap')
@click.option('--index2', type=int, help='Index of the second item to swap')
@click.option('--list', is_flag=True, help='Print the full collection')
@click.option('--shuffle', is_flag=True, help='Shuffle the collection')
def main(name, value, index, index1, index2, list, shuffle):
    if ctx.invoked_subcommand is None:
        show_menu()

    item_names = []
    item_values = []

    if list:
        print_collection(item_names, item_values)
    elif shuffle:
        shuffle_collection(item_names, item_values)
    else:
        add_item(item_names, item_values, name, value)

        if index is not None:
            remove_item(item_names, item_values, index)
        elif index1 is not None and index2 is not None:
            swap_items(item_names, item_values, index1, index2)

@main.command()
def show_menu():
    while True:
        try:
            click.echo('''
            1. Add an item
            2. Remove an item
            3. Swap items
            4. List items
            5. Shuffle items
            6. Exit
            ''')

            value = click.prompt('Please enter a choice', type=int)

            if value == 1:
                add_item()
            elif value == 2:
                remove_item()
            elif value == 3:
                swap_items()
            elif value == 4:
                list_items()
            elif value == 5:
                shuffle_items()
            elif value == 6:
                break
        except Exception as e:
            click.echo(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
