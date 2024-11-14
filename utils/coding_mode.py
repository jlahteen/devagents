import itertools
import sys
import time
import threading

# An event for stopping the coding mode
stop_coding_mode_event = threading.Event()


# Hides the cursor in the console.
def hide_cursor():
    sys.__stdout__.write("\033[?25l")
    sys.__stdout__.flush()


# Shows the cursor in the console.
def show_cursor():
    sys.__stdout__.write("\033[?25h")
    sys.__stdout__.flush()


# The main function to show the coding mode.
def coding_mode_main():
    hide_cursor()
    sys.__stdout__.write("Coding... ")
    cursor = itertools.cycle(["|", "/", "-", "\\"])
    while not stop_coding_mode_event.is_set():
        sys.__stdout__.write(next(cursor) + " ")
        sys.__stdout__.flush()
        time.sleep(0.2)
        sys.__stdout__.write("\b\b")
    sys.__stdout__.write("Done\n")
    show_cursor()


# A thread keeping up the coding mode in the console
coding_mode_thread = threading.Thread(target=coding_mode_main)


# Start the coding mode in the console.
def start_coding_mode():
    coding_mode_thread.start()


# Stops the coding mode in the console.
def stop_coding_mode():
    stop_coding_mode_event.set()
    coding_mode_thread.join()
