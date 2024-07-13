import random
import threading
import time
import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
from googletrans import Translator
import braille
from PIL import Image, ImageTk, ImageSequence, ImageDraw, ImageFont
import pygame
# Initialize pygame for background music
pygame.mixer.init()
pygame.mixer.music.load("deer.mp3")

def play_gif():
    # Create a new top-level window
    gif_window = tk.Toplevel(root)
    gif_window.title("⠎⠓⠊⠅⠁⠝⠕⠅⠕⠀⠝⠕⠅⠕⠝⠕⠅⠕⠀⠅⠕⠎⠓⠊⠞⠁⠝⠞⠁⠝")
    gif_window.overrideredirect(True)  # Remove window decorations

    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate window dimensions and position
    window_width = 400  # You can adjust this size
    window_height = 300  # You can adjust this size
    x_position = screen_width - window_width
    y_position = (screen_height // 2) - (window_height // 2)

    # Set window size and position
    gif_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Load the GIF file
    gif_path = "deer.gif"  # Replace with the path to your GIF file
    gif = Image.open(gif_path)
    frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(gif)]

    # Create a label to display the GIF frames
    gif_label = tk.Label(gif_window)
    gif_label.pack()

    def update_frame(frame_index):
        frame = frames[frame_index]
        gif_label.config(image=frame)
        frame_index = (frame_index + 1) % len(frames)
        gif_window.after(80, update_frame, frame_index)

    update_frame(0)

    # Ensure the GIF window closes when the main window is closed
    def on_closing():
        gif_window.destroy()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)


def deer(translated_text, MyText):
    # Check for specific words and play music if found
    if "deer" in translated_text or "dear" in translated_text or "กวาง" in MyText or "เดียร์" in MyText:
        text_output.insert(tk.END, "🎵 ⠏⠇⠁⠽⠊⠝⠛⠀⠃⠁⠉⠅⠛⠗⠕⠥⠝⠙⠀⠍⠥⠎⠊⠉ 🎵\n")
        pygame.mixer.music.play(-1)  # Play music indefinitely
        play_gif()


# Initialize the recognizer and translator
r = sr.Recognizer()
translator = Translator()

def countdown(n):
    for i in range(n, 0, -1):
        text_output.insert(tk.END, f"{i}..")
        root.update_idletasks()  # Force GUI to update immediately
        time.sleep(1)
    text_output.insert(tk.END, "⠛⠕⠀⠎⠓⠕⠕⠞!\n")
    root.update_idletasks()  # Force GUI to update immediately

# Function to handle speech recognition in a separate thread
def recognize_speech():
    try:
        with sr.Microphone() as source:
            text_output.delete('1.0', tk.END)
            text_output.insert(tk.END, "🎧 ⠊⠀⠁⠍⠀⠇⠊⠎⠞⠑⠝⠊⠝⠛\n")
            root.update_idletasks()  # Force GUI to update immediately
            r.adjust_for_ambient_noise(source, duration=0.2)
            audio = r.listen(source, timeout=8)  # Adjust timeout as needed  
            MyText = r.recognize_google(audio, language='th-TH')
            MyText = MyText.lower()
            text_output.insert(tk.END, f"\U0001f600 ⠊⠀⠓⠑⠁⠗⠙ => {MyText}\n")
            text_output.insert(tk.END, "🤖 ⠞⠗⠁⠝⠎⠇⠁⠞⠊⠝⠛")
            root.update_idletasks()  # Force GUI to update immediately
            time.sleep(1)  
            countdown(3)
            # Translate the text to English
            try:
                translated = translator.translate(MyText, src='th', dest='en')
                translated_text = translated.text
                text_output.insert(tk.END, f"🤔 ⠙⠊⠙⠀⠊⠀⠛⠑⠞⠀⠊⠞⠀⠗⠊⠛⠓⠞ => \n {translated_text}\n")
                deer(translated_text, MyText)
            except Exception as e:
                text_output.insert(tk.END, f"☢️⠑⠗⠗⠕⠗⠀⠞⠗⠁⠝⠎⠇⠁⠞⠑ => {e}\n")
            root.update_idletasks()  # Force GUI to update immediately
            br = braille.textToBraille(translated_text)
            text_output.insert(tk.END, f"{br}\n")
    except sr.RequestError as e:
        text_output.insert(tk.END, f"☢️ ⠗⠑⠟⠥⠑⠎⠞⠀⠑⠗⠗⠕⠗ => {e}\n")
    except sr.UnknownValueError:
        text_output.insert(tk.END, "☢️ ⠺⠓⠁⠞⠀⠙⠊⠙⠀⠽⠕⠥⠀⠎⠁⠽\n") #what did you say
    except Exception as e:
        text_output.insert(tk.END, f"☢️ ⠥⠝⠑⠭⠏⠑⠉⠞⠑⠙⠀⠑⠗⠗⠕⠗ => {e}\n")
        
# Function to start speech recognition in a separate thread
def start_recognition():
    # Start the recognize_speech function in a new thread
    threading.Thread(target=recognize_speech).start()

def show_image_with_text():
    # Load the image
    img_path = "not.png"  # Replace with the path to your image
    original_image = Image.open(img_path)
    
    # Create a drawing context
    draw = ImageDraw.Draw(original_image)
    
    # Define the text and font
    text = "YOU ARE NOT"
    font_size = 40  # Adjust font size as needed (2 times larger)
    font = ImageFont.truetype("arial.ttf", font_size)  # Use a TrueType font for custom size
    
    # Calculate text size
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]  # Using textbbox() to get size
    image_width, image_height = original_image.size
    
    # Calculate text position (center of the image)
    text_x = (image_width - text_width) // 2
    text_y = (image_height - text_height) // 2 + 150
    
    # Create a background rectangle for the text
    padding = 10  # Padding around the text
    rectangle_x0 = text_x - padding
    rectangle_y0 = text_y - padding
    rectangle_x1 = text_x + text_width + padding
    rectangle_y1 = text_y + text_height + padding
    
    # Draw the background rectangle
    draw.rectangle([rectangle_x0, rectangle_y0, rectangle_x1, rectangle_y1], fill="black")
    
    # Draw the text on top of the background rectangle
    draw.text((text_x, text_y), text, font=font, fill="white")
    
    # Convert image for tkinter
    img = ImageTk.PhotoImage(original_image)
    def create_image_window():
        x_position = random.randint(0, screen_width - img.width())
        y_position = random.randint(0, screen_height - img.height())
        image_window = tk.Toplevel(root)
        image_window.geometry(f"{img.width()}x{img.height()}+{x_position}+{y_position}")
        image_window.overrideredirect(True)
        image_label = tk.Label(image_window, image=img)
        image_label.pack()
        root.after(10, create_image_window)

    root.after(10, create_image_window)

# Function to handle exit
def on_closing():
    if messagebox.showinfo("Check Check","Click here if you are blind"):
        show_image_with_text()


# Create the main window
root = tk.Tk()
root.title("แอพเพื่อคนหูบอดและตาหนวก")

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate window dimensions and position (80% width and 70% height)
window_width = int(screen_width * 0.75)
window_height = int(screen_height * 0.85)
x_position = 0
y_position = (screen_height // 2) - (window_height // 2)

# Set window size and position
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Calculate font size (5% of screen width)
font_size = int(screen_width * 0.02)

# Create a frame for the widgets
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create a large label for the title
title_label = tk.Label(frame, text="แอพเพื่อคนหูบอดและตาหนวก\n⠁⠏⠏⠀⠋⠕⠗⠀⠞⠓⠑⠀⠑⠁⠗⠎⠀⠃⠇⠊⠝⠙⠀⠁⠝⠙⠀⠍⠥⠎⠞⠁⠉⠓⠑", font=("Segoe UI Emoji", font_size))
title_label.pack(pady=10)

# Create start button
start_button = tk.Button(frame, text="⠇⠊⠎⠞⠑⠝", command=start_recognition, font=("Helvetica", font_size))
start_button.pack(pady=5)

# Create a text widget for output
text_output = tk.Text(frame, height=10, width=50, font=("Segoe UI Emoji", font_size))
text_output.pack(pady=5, fill=tk.BOTH, expand=True)

# Handle the window close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the GUI event loop
root.mainloop()
