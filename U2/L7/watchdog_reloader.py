from ast import main
import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import tkinter as tk
from tkinter import ttk

class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return None

        elif event.event_type == 'modified':
            print("Reloading...")
            os.execl(sys.executable, sys.executable, *sys.argv)

def start(tkinter_root):
    """
    Start the watchdog observer and the tkinter mainloop.

    Args:
        tkinter_root: The root window of the tkinter application.

    Returns:
        None
    """
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()

    mainloop_running = False
    try:
        tkinter_root.mainloop()
    except SyntaxError as e:
        print(f"Error: {e}")
        print("Mainloop not started")
    except tk.TclError as e:
        print(f"Error: {e}")
        print("Mainloop not started")
    else:
        print("Mainloop started successfully")
        mainloop_running = True

    # Stop the observer when the mainloop is quit
    observer.stop()
    observer.join()

    if mainloop_running:
        # Only call quit() if mainloop() was run successfully
        tkinter_root.quit()
        # Restart the tkinter mainloop after a file change is detected
        # tkinter_root.after(1000, start, tkinter_root)