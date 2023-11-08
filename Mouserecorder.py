##pyinstaller --onefile your_script.py
import cv2
import tkinter as tk
from pynput.mouse import Listener, Controller
import threading
import json
from datetime import datetime
import pyautogui
import time
import keyboard








def windowResize() ->bool:
    """
    Function to resize window of ninja legends

    return Resize the window size to width = 830 PX and height = 495 PX True if window named Ninja Legends is found else return False
    """
    #This prints list of all the window.
    windows = pyautogui.getAllWindows()
    ninja_legend_found = False
    for window in windows:
        if ("Ninja Legends" == window.title):
            ninja_legend_found = True
            #  set width and height of game window to 830 by 490
            window.width = 830
            window.height = 495
            break
    return ninja_legend_found

# Function to close the application
def close_app():
    root.destroy()

# Function to start recording clicks
def start_recording():
    global recording
    recording = True
    clicked_positions.clear()
    clicked_positions_label.config(text="Recording...")

# Function to stop recording clicks
def stop_recording():
    global recording
    recording = False
    dump_clicked_positions()
    update_clicked_positions_label()
    clicked_positions_label.config(text="Recording stopped")

# Function to update the mouse position label
def update_mouse_position_label():
    x, y = mouse_controller.position
    mouse_position_label.config(text=f"Mouse Position: X={x}, Y={y}")
    root.after(100, update_mouse_position_label)

# Function to handle mouse clicks
def on_click(x, y, button, pressed):
    if recording:
        app_x, app_y = root.winfo_x(), root.winfo_y()
        if pressed and (
            x < app_x or x > app_x + app_region[2] or y < app_y or y > app_y + app_region[3]
        ):
            clicked_positions.append((x, y, datetime.now()))

# Function to update the clicked positions label
def update_clicked_positions_label():
    clicked_positions_label.config(
        text="Clicked Positions and Durations:\n" + format_clicked_positions()
    )

# Function to format clicked positions and durations
def format_clicked_positions():
    formatted = []
    for i in range(len(clicked_positions)):
        x, y, timestamp = clicked_positions[i]
        if i > 0:
            duration = (timestamp - clicked_positions[i - 1][2]).total_seconds()
        else:
            duration = 0.0
        formatted.append({"X": x, "Y": y, "Duration": duration})
    return json.dumps(formatted, indent=4)

# Function to dump clicked positions into a JSON file
def dump_clicked_positions():
    with open("clicked_positions.json", "w") as file:
        data = format_clicked_positions()
        file.write(data)

# Function to load data from a JSON file and display it
def auto_play_action():
    global auto_playing
    auto_playing = True
    auto_play_button.config(state="disabled")
    stop_auto_play_button.config(state="active")

    try:
        with open("clicked_positions.json", "r") as file:
            data = json.load(file)
            clicked_positions.clear()
            for item in data:
                x, y, duration = item["X"], item["Y"], item["Duration"]
                clicked_positions.append((x, y, duration))
                clicked_positions_label.config(text=f"Recording stopped X={x} Y={y} Duration={duration}")

            list_of_clicks = clicked_positions
    except FileNotFoundError:
        clicked_positions_label.config(text="No recorded data found!")

    def auto_play_task():
        count = 1
        while auto_playing:
            dot = "." * count
            clicked_positions_label.config(text=f"Auto Play is running {dot}")
            for x_pos, y_pos, duration in list_of_clicks:
                move_mouse_to_position(x_pos, y_pos)
                time.sleep(duration + 1)
                pyautogui.click(x_pos, y_pos)
            time.sleep(0.5)  # Simulate some action
            count += 1
            if count > 4:
                count = 1
            if keyboard.is_pressed("q"):
                stop_auto_play_action()
                break

    # Start a new thread for the auto play task
    auto_play_thread = threading.Thread(target=auto_play_task)
    auto_play_thread.start()

# Function to run when the "Stop Auto Play" button is clicked
def stop_auto_play_action():
    global auto_playing
    auto_playing = False
    auto_play_button.config(state="active")
    stop_auto_play_button.config(state="disabled")
    clicked_positions_label.config(text=f"Auto Play is stopping.")
    if auto_play_thread is not None:
        auto_play_thread.join()  # Wait for the auto-play thread to finish
        clicked_positions_label.config(text=f"Auto Play is stops after full circle. Please wait to continue")

def move_mouse_to_position(x, y):
    if x < 0:
        x = 0
    elif x > screen_width:
        x = screen_width
    if y < 0:
        y = 0
    elif y > screen_height:
        y = screen_height
    pyautogui.moveTo(x, y)
# Function to close the application
def close_app():
    global stop_threads  # Signal the threads to stop
    global auto_playing
    auto_playing = False
    auto_play_button.config(state="active")
    stop_auto_play_button.config(state="disabled")
    clicked_positions_label.config(text=f"Auto Play is stopping.")
    if auto_play_thread is not None:
        auto_play_thread.join()  # Wait for the auto-play thread to finish
        clicked_positions_label.config(text=f"Auto Play is stopped.")

# Function to disable the Auto Play button
def disable_auto_play_button():
    auto_play_button.config(state="disabled")

# Calculate the time difference between the target time and the current time
target_time = datetime(2023, 11, 8, 12, 0)  # Set your target date and time
current_time = datetime.now()
time_difference = target_time - current_time

# Convert the time difference to milliseconds
delay_milliseconds = int(time_difference.total_seconds() * 1000)

window_resized_bool = windowResize()
screen_width, screen_height = pyautogui.size()
# Define a global flag variable to signal threads to stop
stop_threads = False
# Define the auto_play_thread globally
auto_play_thread = None

list_of_clicks = []



# Create the main application window
root = tk.Tk()
root.title("ClickerForNS")
# Set the application window size to 320x320
root.geometry("320x320")

# Define the application region (320x320)
app_region = (0, 0, 320, 320)

# Create a frame for Section 1
frame1 = tk.Frame(root, bg="Blue",width=320, height=40)
frame1.pack(pady=10, padx=10)
frame1.pack_propagate(0)



# Start Recording button
start_recording_button = tk.Button(frame1, text="Start Recording", command=start_recording)
start_recording_button.pack( side="left", padx=20)

# Stop Recording button
stop_recording_button = tk.Button(frame1, text="Stop Recording", command=stop_recording )
stop_recording_button.pack(side="right" ,padx=20)


frame2 = tk.Frame(root, bg="Green", width=320, height=40)
frame2.pack(pady=10, padx=10)
frame2.pack_propagate(0)

# Auto Play button
auto_play_button = tk.Button(frame2, text="Autoplay", command=auto_play_action)
auto_play_button.pack(side="left" , padx=20)

# Create "Stop Auto Play" button (initially disabled)
stop_auto_play_button = tk.Button(frame2, text="Stop Autoplay", command=stop_auto_play_action, state="disabled")
stop_auto_play_button.pack(side="right" , padx=20)


frame3 = tk.Frame(root, bg="red", width=320, height=40)
frame3.pack(pady=10, padx=10)
frame3.pack_propagate(0)


# Label to display mouse position
mouse_position_label = tk.Label(frame3, text="Mouse Position: X=0, Y=0", bg="red")
mouse_position_label.pack(side="top")

# Close button
# close_button = tk.Button(root, text="Close", command=close_app)
# close_button.pack(side="top", pady=10)

# Label to display clicked position (below the Close button)
# clicked_positions_label = tk.Label(root, text="Clicked Positions and Durations:")
# clicked_positions_label.pack(side="top")

# Label to display clicked position (below the Close button)

frame4 = tk.Frame(root, bg="lightyellow", width=320, height=40)
frame4.pack(pady=10, padx=10)
frame4.pack_propagate(0)
clicked_positions_label = tk.Label(frame4, text="...")
clicked_positions_label.pack(side="top")

frame5 = tk.Frame(root, bg="lightyellow", width=320, height=40)
frame5.pack(pady=10, padx=10)
frame5.pack_propagate(0)

clicked_positions_label1 = tk.Label(frame5, text="Developed For Ravi SIR", bg="lightyellow")
clicked_positions_label1.pack(side="top")
clicked_positions_label = tk.Label(frame5, text="Developed By Shree Ram Sigdel. All right reserved" ,bg="lightyellow")
clicked_positions_label.pack(side="bottom")

# Create a thread to listen for mouse clicks
mouse_listener = Listener(on_click=on_click)
mouse_thread = threading.Thread(target=mouse_listener.start)
mouse_thread.start()

# Initialize the mouse controller to get the current mouse position
mouse_controller = Controller()

# Initialize the list to store clicked positions
clicked_positions = []

# Initialize recording flag
recording = False

# Update the mouse position label
update_mouse_position_label()

# Variable to track if auto play action is running
auto_playing = False

# Schedule the function to disable the Auto Play button at the target time
root.after(delay_milliseconds, disable_auto_play_button)

root.mainloop()
