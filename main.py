import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # Import PIL for handling images
import subprocess

# Function placeholders
def open_register():
    subprocess.Popen(["python", "register.py"])  # Replace with your actual script path

def open_login():
    subprocess.Popen(["python", "login.py"])  # Replace with your actual script path

def open_face_recognition():
    subprocess.Popen(["python", "face_recognition.py"])  # Replace with your actual script path

def open_unknown_faces():
    subprocess.Popen(["python", "unknown_faces.py"])  # Replace with your actual script path

def open_help():
    subprocess.Popen(["python", "help.py"])

# Create main Tkinter window
root = tk.Tk()
root.title("Main Menu")
root.geometry("400x400")
root.configure(bg="#f0f0f0")

# Load the background image using PIL
try:
    bg_image = Image.open("D:/Railway_ticket.py/image_project/imagess.jpg")  # Path to your image
    bg_image = bg_image.resize((1200, 1200), Image.Resampling.LANCZOS)  # Resize to fit the window (LANCZOS is the equivalent to ANTIALIAS)
    bg_image = ImageTk.PhotoImage(bg_image)

    # Set the background image in the window
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)  # Make the background fill the entire window
except Exception as e:
    print(f"Error loading background image: {e}")

# Greeting Label
greeting_label = tk.Label(root, text="Namaste User", font=("Arial", 16, "bold"), bg="#f0f0f0")
greeting_label.pack(pady=20)

# Instruction Label
instruction_label = tk.Label(root, text="Note: If you are a user, don't tap on 'Enable Railway Camera' or 'Unknown Passengers'", font=("Arial", 10, "italic"), bg="#f0f0f0", fg="red")
instruction_label.pack(pady=10)

# Apply styles
style = ttk.Style()
style.configure("Red.TButton", foreground="green", background="red", font=("Arial", 12, "bold"), padding=10)
style.configure("Green.TButton", foreground="red", background="green", font=("Arial", 12, "bold"), padding=10)
style.configure("Blue.TButton", foreground="blue", background="blue", font=("Arial", 12, "bold"), padding=10)
style.configure("Orange.TButton", foreground="orange", background="orange", font=("Arial", 12, "bold"), padding=10)
style.configure("Orange.TButton", foreground="brown", background="black", font=("Arial", 12, "bold"), padding=10)

# Buttons
ttk.Button(root, text="Login", style="Red.TButton", command=open_register).pack(pady=10, fill="x", padx=20)
ttk.Button(root, text="Register", style="Green.TButton", command=open_login).pack(pady=10, fill="x", padx=20)
ttk.Button(root, text="Enable Railway Camera", style="Blue.TButton", command=open_face_recognition).pack(pady=10, fill="x", padx=20)
ttk.Button(root, text="Unknown Passenger", style="Orange.TButton", command=open_unknown_faces).pack(pady=10, fill="x", padx=20)
ttk.Button(root, text="Help", style="Red.TButton", command=open_help).pack(pady=10, fill="x", padx=20)

root.mainloop()
