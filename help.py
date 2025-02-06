import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # Import PIL for handling images

# Help Function for Registration
def registration_help():
    help_text = """
    Registration Help:
    
    1. Open the "Register" page.
    2. Fill in your full name, mobile number, proof document type (like Aadhar, PAN, or Passport), 
       your ID number from the document, and a password for your account.
    3. Once done, click "Register".
    4. After registration, you can log in using your mobile number and password.
    """
    messagebox.showinfo("Registration Help", help_text)

# Help Function for Login
def login_help():
    help_text = """
    Login Help:
    
    1. After registering, go to the "Login" page.
    2. Enter your mobile number and the password you created.
    3. Click "Login" to access the system.
    4. If you forgot your password, click "Forgot Password?" and follow the instructions to reset it.
    """
    messagebox.showinfo("Login Help", help_text)

# Help Function for Ticket Booking
def ticket_booking_help():
    help_text = """
    Ticket Booking Help:
    
    1. Once logged in, go to the "Ticket Booking" page.
    2. Choose your station (Pune) and the destination station (PCMC).
    3. Enter the date you want to travel (in the format YYYY-MM-DD).
    4. Choose the type of ID proof you want to use (Aadhar, PAN, or Passport) and enter the ID number.
    5. Click "Book Ticket" to complete the booking.
    """
    messagebox.showinfo("Ticket Booking Help", help_text)

# Help Function for Face Recognition
def face_recognition_help():
    help_text = """
    Face Recognition Help:
    
    1. To start, go to the "Create Dataset" section and take some pictures of your face (about 50 pictures).
    2. These pictures will be saved for face recognition.
    3. Next, click "Train Model" to teach the system how to recognize your face.
    4. After training, click "Start Face Recognition" to begin using the system.
    5. The system will try to recognize your face and show your name if it matches.
    6. If the system sees an unknown face, it will save the image with a timestamp.
    """
    messagebox.showinfo("Face Recognition Help", help_text)

# GUI Setup for Help Section
def open_help_window():
    help_window = tk.Tk()
    help_window.title("Help - Ticket Booking & Face Recognition App")
    help_window.geometry("400x400")
    help_window.config(bg="#f0f0f0")

    # Load the background image using PIL
    try:
        bg_image = Image.open("D:/Railway_ticket.py/image_project/imagesss.jpg")  # Path to your image
        bg_image = bg_image.resize((1200, 1200), Image.Resampling.LANCZOS)  # Resize to fit the window (LANCZOS is the equivalent to ANTIALIAS)
        bg_image = ImageTk.PhotoImage(bg_image)

        # Set the background image in the window
        bg_label = tk.Label(help_window, image=bg_image)
        bg_label.place(relwidth=1, relheight=1)  # Make the background fill the entire window
    except Exception as e:
        print(f"Error loading background image: {e}")

    # Define the global style
    style = ttk.Style()

    # Custom Styles
    style.configure("TButton",
                    font=("Arial", 12),
                    background="#4CAF50",  # Green background
                    foreground="red",
                    padding=10)

    style.configure("TLabel",
                    font=("Arial", 14),
                    background="#f0f0f0")

    style.configure("TFrame",
                    background="#f0f0f0")
    
    # Add some padding around the buttons
    frame = ttk.Frame(help_window)
    frame.pack(pady=20)

    # Create Buttons for each help section
    ttk.Button(frame, text="Registration Help", command=registration_help).pack(pady=10, fill="x")
    ttk.Button(frame, text="Login Help", command=login_help).pack(pady=10, fill="x")
    ttk.Button(frame, text="Ticket Booking Help", command=ticket_booking_help).pack(pady=10, fill="x")
    ttk.Button(frame, text="Face Recognition Help", command=face_recognition_help).pack(pady=10, fill="x")

    help_window.mainloop()

# Running the Help Window
open_help_window()
