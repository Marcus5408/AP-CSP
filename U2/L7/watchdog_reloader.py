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
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()

    # Start the tkinter mainloop
    tkinter_root.mainloop()

    # Stop the observer when the mainloop is quit
    observer.stop()
    observer.join()

    # Restart the tkinter mainloop after a file change is detected
    tkinter_root.quit()
    tkinter_root.after(1000, start, tkinter_root)