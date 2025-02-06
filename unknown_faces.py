import os
import cv2
import tkinter as tk
from tkinter import ttk, Canvas, Frame, Entry, Toplevel, messagebox
from PIL import Image, ImageTk

data_path = "dataset/"
unknown_path = "unknown_faces/"
password = "738530"

if not os.path.exists(data_path):
    os.makedirs(data_path)
if not os.path.exists(unknown_path):
    os.makedirs(unknown_path)

def apply_styles():
    """Apply CSS-like styling to the UI using ttk.Style()."""
    style = ttk.Style()
    
    # Main window button (blue background, red text)
    style.configure("BlueRed.TButton", font=("Arial", 12), padding=5, background="#007BFF", foreground="red")
    style.map("BlueRed.TButton", background=[("active", "#0056b3")])  # Darker blue on hover

    # Submit button in password window (green background, black text)
    style.configure("Green.TButton", font=("Arial", 12), padding=5, background="#28a745", foreground="black")
    style.map("Green.TButton", background=[("active", "#218838")])  # Darker green on hover

    # General styling
    style.configure("TLabel", font=("Arial", 12), padding=5)
    style.configure("TEntry", font=("Arial", 12), padding=5)
    style.configure("TFrame", background="#f0f0f0")

def verify_password(password_entry, password_window):
    """Verify password and open unknown faces window if correct."""
    if password_entry.get() == password:
        password_window.destroy()
        load_unknown_faces()
    else:
        messagebox.showerror("Error", "Incorrect Password!")

def load_unknown_faces():
    """Open the Unknown Faces Viewer."""
    unknown_faces_window = Toplevel(root)
    unknown_faces_window.title("Unknown Faces Viewer")
    unknown_faces_window.geometry("500x600")
    unknown_faces_window.configure(bg="#f0f0f0")

    canvas = Canvas(unknown_faces_window, bg="#f0f0f0")
    scrollbar = ttk.Scrollbar(unknown_faces_window, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="#f0f0f0")
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    images = [img for img in os.listdir(unknown_path) if img.endswith(('.png', '.jpg', '.jpeg'))]

    if not images:
        label = ttk.Label(scrollable_frame, text="No Unknown Faces Found", font=("Arial", 14), background="#f0f0f0")
        label.pack(pady=20)
        return

    for image_name in images:
        img_path = os.path.join(unknown_path, image_name)
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (200, 200))
        img_pil = Image.fromarray(img)
        img_tk = ImageTk.PhotoImage(img_pil)

        frame = Frame(scrollable_frame, bg="white", relief="solid", borderwidth=1)
        frame.pack(pady=10, padx=10, fill="both")

        label_img = tk.Label(frame, image=img_tk, bg="white")
        label_img.image = img_tk
        label_img.pack(pady=5)

        label_text = ttk.Label(frame, text=image_name, font=("Arial", 10), background="white")
        label_text.pack()

def open_password_window():
    """Open the password entry window."""
    password_window = Toplevel(root)
    password_window.title("Enter Password")
    password_window.geometry("300x150")
    password_window.configure(bg="#f0f0f0")

    ttk.Label(password_window, text="Enter Password:", background="#f0f0f0").pack(pady=10)
    password_entry = ttk.Entry(password_window, show="*")
    password_entry.pack(pady=5)

    ttk.Button(password_window, text="Submit", style="Green.TButton", command=lambda: verify_password(password_entry, password_window)).pack(pady=10)

# Create main Tkinter window
root = tk.Tk()
root.title("Access Unknown Faces")
root.geometry("400x200")
root.configure(bg="#f0f0f0")

# Load the background image using PIL
bg_image_path = "D:/Railway_ticket.py/image_project/im.jpg"  # Path to your image
bg_image = Image.open(bg_image_path)
bg_image = bg_image.resize((1100, 1100), Image.Resampling.LANCZOS)  # Resize to fit the window size
bg_image = ImageTk.PhotoImage(bg_image)

# Set the background image in the window
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)  # Make the background fill the entire window

apply_styles()

# Add the "View Unknown Faces" button on top of the background image
ttk.Button(root, text="View Unknown Faces", style="BlueRed.TButton", command=open_password_window).pack(pady=50)

root.mainloop()
