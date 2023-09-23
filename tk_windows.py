import tkinter
from tkinter import ttk

# Create the main window
top = tkinter.Tk()
top.title("Hello World!")
top.geometry("300x200")

# Create a label in the window
label = ttk.Label(top, text="Hello World!")
label.pack()

entry = ttk.Entry(top)
entry.insert(0, "Hello World!")
entry.pack()

# Create a button that creates a new window when clicked with another button that launches the same window
def create_window(window_name="Hello World!"):
    window = tkinter.Toplevel(top)
    window.title("Hello World!")
    window.geometry("300x200")

    label = ttk.Label(window, text="Hello World!")
    label.pack()

    entry = ttk.Entry(window)
    entry.insert(0, window_name)
    entry.pack()

    # add button that makes a new window using the create_window function but passing in the input from the entry box
    button = ttk.Button(window, text="New Window", command=lambda: create_window(entry.get()))
    button.pack()

button = ttk.Button(top, text="New Window", command=lambda: create_window(entry.get()))
button.pack()

# Start the GUI
top.mainloop()
