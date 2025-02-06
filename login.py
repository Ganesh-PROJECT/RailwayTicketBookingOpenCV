import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # Import PIL for handling images
import sqlite3

# Database Setup
def setup_database():
    conn = sqlite3.connect("ticket_booking.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS clients (
                      id INTEGER PRIMARY KEY,
                      name TEXT,
                      mobile TEXT UNIQUE,
                      document_type TEXT,
                      proof_id TEXT,
                      password TEXT)''')
    conn.commit()
    conn.close()

setup_database()

# Register Function
def register_client():
    name = entry_name.get()
    mobile = entry_mobile.get()
    document_type = document_var.get()
    proof_id = entry_proof_id.get()
    password = entry_password.get()
    
    if not (name and mobile and document_type and proof_id and password):
        messagebox.showerror("Error", "All fields are required!")
        return
    
    try:
        conn = sqlite3.connect("ticket_booking.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clients (name, mobile, document_type, proof_id, password) VALUES (?, ?, ?, ?, ?)",
                       (name, mobile, document_type, proof_id, password))
        conn.commit()
        messagebox.showinfo("Success", "Registration Successful!")
        root_register.destroy()
        login_page()  # Redirect to login after registration
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Mobile number already registered!")
    except Exception as e:
        messagebox.showerror("Error", f"Database Error: {str(e)}")
    finally:
        conn.close()

# Register Page UI
def register_page():
    global root_register, entry_name, entry_mobile, document_var, entry_proof_id, entry_password
    root_register = tk.Tk()
    root_register.title("Register - Ticket Booking App")
    root_register.geometry("400x500")
    root_register.config(bg="#f0f0f0")
    
    # Load the background image using PIL
    try:
        bg_image = Image.open("D:/Railway_ticket.py/image_project/imag.jpg")  # Path to your image
        bg_image = bg_image.resize((1200, 1200), Image.Resampling.LANCZOS)  # Resize to fit the window
        bg_image = ImageTk.PhotoImage(bg_image)

        # Set the background image in the window
        bg_label = tk.Label(root_register, image=bg_image)
        bg_label.place(relwidth=1, relheight=1)  # Make the background fill the entire window
    except Exception as e:
        print(f"Error loading background image: {e}")
    
    tk.Label(root_register, text="Register", font=("Arial", 18), bg="#f0f0f0").pack(pady=10)
    
    tk.Label(root_register, text="Name", bg="#f0f0f0").pack()
    entry_name = tk.Entry(root_register)
    entry_name.pack(pady=5)
    
    tk.Label(root_register, text="Mobile (+Country Code)", bg="#f0f0f0").pack()
    entry_mobile = tk.Entry(root_register)
    entry_mobile.pack(pady=5)
    
    tk.Label(root_register, text="Document Proof", bg="#f0f0f0").pack(pady=5)
    document_var = tk.StringVar()
    document_var.set("Select")
    ttk.Combobox(root_register, textvariable=document_var, values=["Aadhar", "PAN", "Passport"]).pack(pady=5)
    
    tk.Label(root_register, text="Proof ID No.", bg="#f0f0f0").pack(pady=5)
    entry_proof_id = tk.Entry(root_register)
    entry_proof_id.pack(pady=5)
    
    tk.Label(root_register, text="Password", bg="#f0f0f0").pack(pady=5)
    entry_password = tk.Entry(root_register, show="*")
    entry_password.pack(pady=5)
    
    tk.Button(root_register, text="Register", command=register_client).pack(pady=10)
    tk.Button(root_register, text="Already Registered? Login", command=login_page).pack() 
    
    root_register.mainloop()

# Login Page (Basic Placeholder)
def login_page():
    messagebox.showinfo("Login", "Please log in with your credentials.")

# Run the register page initially
register_page()
