import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

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
    cursor.execute('''CREATE TABLE IF NOT EXISTS tickets (
                      ticket_id INTEGER PRIMARY KEY,
                      from_station TEXT,
                      departure_station TEXT,
                      train_name TEXT,
                      journey_date TEXT,
                      passenger_proof TEXT,
                      proof_id TEXT)''')
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
    
    conn = sqlite3.connect("ticket_booking.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO clients (name, mobile, document_type, proof_id, password) VALUES (?, ?, ?, ?, ?)",
                       (name, mobile, document_type, proof_id, password))
        conn.commit()
        messagebox.showinfo("Success", "Registration Successful!")
        root_register.destroy()
        login_page()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Mobile number already registered!")
    finally:
        conn.close()

# Forgot Password Function
def forgot_password():
    mobile = entry_login_mobile.get()
    if not mobile:
        messagebox.showerror("Error", "Please enter your mobile number to reset password!")
        return
    messagebox.showinfo("Forgot Password", f"Password reset instructions sent to {mobile}.")

# Login Function
def login_client():
    mobile = entry_login_mobile.get()
    password = entry_login_password.get()
    
    conn = sqlite3.connect("ticket_booking.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients WHERE mobile=? AND password=?", (mobile, password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        messagebox.showinfo("Success", "Login Successful!")
        root_login.destroy()
        ticket_booking_page()
    else:
        messagebox.showerror("Error", "Invalid credentials!")

# Ticket Booking Page
def ticket_booking_page():
    global root_ticket, from_station_var, departure_station_var, train_name_var, journey_date_var, proof_var, proof_id_var
    root_ticket = tk.Tk()
    root_ticket.title("Ticket Booking - Ticket Booking App")
    root_ticket.geometry("400x600")
    root_ticket.config(bg="#f0f0f0")

    tk.Label(root_ticket, text="Book a Ticket", font=("Arial", 18), bg="#f0f0f0").pack(pady=10)
    
    # From Station
    tk.Label(root_ticket, text="From Station", bg="#f0f0f0").pack()
    from_station_var = tk.StringVar()
    from_station_var.set("Pune")
    ttk.Combobox(root_ticket, textvariable=from_station_var, values=["Pune"]).pack(pady=5)

    # Departure Station
    tk.Label(root_ticket, text="Departure Station", bg="#f0f0f0").pack()
    departure_station_var = tk.StringVar()
    departure_station_var.set("PCMC")
    ttk.Combobox(root_ticket, textvariable=departure_station_var, values=["PCMC"]).pack(pady=5)

    # Train Name
    tk.Label(root_ticket, text="Train Name", bg="#f0f0f0").pack()
    train_name_var = tk.StringVar()
    train_name_var.set("PCMC Smart Rail")
    ttk.Combobox(root_ticket, textvariable=train_name_var, values=["PCMC Smart Rail"]).pack(pady=5)

    # Journey Date
    tk.Label(root_ticket, text="Date of Journey (YYYY-MM-DD)", bg="#f0f0f0").pack()
    journey_date_var = tk.StringVar()
    tk.Entry(root_ticket, textvariable=journey_date_var).pack(pady=5)

    # Arrival Time (Fixed)
    tk.Label(root_ticket, text="Rail Arrival Time at Pune: 12:00 PM", bg="#f0f0f0").pack(pady=5)
    tk.Label(root_ticket, text="Rail Arrival Time at PCMC: 01:00 PM", bg="#f0f0f0").pack(pady=5)
    tk.Label(root_ticket, text="Class:Sleeper S1", bg="#f0f0f0").pack(pady=5)

    # Proof Type
    tk.Label(root_ticket, text="Proof Type", bg="#f0f0f0").pack(pady=5)
    proof_var = tk.StringVar()
    proof_var.set("Aadhar")
    ttk.Combobox(root_ticket, textvariable=proof_var, values=["Aadhar", "PAN", "Passport"]).pack(pady=5)

    # Proof ID
    tk.Label(root_ticket, text="Proof ID No.", bg="#f0f0f0").pack(pady=5)
    proof_id_var = tk.StringVar()
    tk.Entry(root_ticket, textvariable=proof_id_var).pack(pady=5)

    # Book Ticket Button
    tk.Button(root_ticket, text="Book Ticket", command=book_ticket, bg="#4CAF50", fg="white").pack(pady=10)
    
    # Book Another Ticket Button
    tk.Button(root_ticket, text="Book Another Ticket", command=book_another_ticket, bg="#008CBA", fg="white").pack(pady=5)
    
    root_ticket.mainloop()

# Book Ticket Function
def book_ticket():
    from_station = from_station_var.get()
    departure_station = departure_station_var.get()
    train_name = train_name_var.get()
    journey_date = journey_date_var.get()
    proof_type = proof_var.get()
    proof_id = proof_id_var.get()

    if not (journey_date and proof_id):
        messagebox.showerror("Error", "All fields are required!")
        return
    
    conn = sqlite3.connect("ticket_booking.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tickets (from_station, departure_station, train_name, journey_date, passenger_proof, proof_id) VALUES (?, ?, ?, ?, ?, ?)",
                   (from_station, departure_station, train_name, journey_date, proof_type, proof_id))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Ticket Booked Successfully!")
    root_ticket.destroy()
    payment_page()

# Book Another Ticket Function
def book_another_ticket():
    root_ticket.destroy()
    ticket_booking_page()

# Payment Page
def payment_page():
    global root_payment, payment_amount_var
    root_payment = tk.Tk()
    root_payment.title("Payment - Ticket Booking App")
    root_payment.geometry("400x300")
    root_payment.config(bg="#f0f0f0")
    
    tk.Label(root_payment, text="Payment", font=("Arial", 18), bg="#f0f0f0").pack(pady=10)
    
    tk.Label(root_payment, text="Ticket Cost: ₹500", bg="#f0f0f0").pack(pady=10)
    
    tk.Label(root_payment, text="Enter Payment Amount", bg="#f0f0f0").pack(pady=5)
    payment_amount_var = tk.StringVar()
    tk.Entry(root_payment, textvariable=payment_amount_var).pack(pady=5)
    
    def process_payment():
        try:
            entered_amount = float(payment_amount_var.get())
            if entered_amount == 500:
                messagebox.showinfo("Success", "Payment Successful!")
                root_payment.destroy()
            else:
                messagebox.showerror("Error", "Incorrect Payment Amount!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount!")
    
    tk.Button(root_payment, text="Pay ₹500", command=process_payment, bg="#4CAF50", fg="white").pack(pady=20)
    
    root_payment.mainloop()

# Register Page
def register_page():
    global root_register, entry_name, entry_mobile, document_var, entry_proof_id, entry_password
    root_register = tk.Tk()
    root_register.title("Register - Ticket Booking App")
    root_register.geometry("400x500")
    root_register.config(bg="#f0f0f0")
    
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
    
    tk.Button(root_register, text="Register", command=register_client, bg="#4CAF50", fg="white").pack(pady=10)
    tk.Button(root_register, text="Already Registered? Login", command=login_page, fg="blue", bg="#f0f0f0").pack() 
    
    root_register.mainloop()

# Login Page
def login_page():
    global root_login, entry_login_mobile, entry_login_password
    root_login = tk.Tk()
    root_login.title("Login - Ticket Booking App")
    root_login.geometry("400x400")
    root_login.config(bg="#f0f0f0")
    
    tk.Label(root_login, text="Login", font=("Arial", 18), bg="#f0f0f0").pack(pady=10)
    
    tk.Label(root_login, text="Mobile Number", bg="#f0f0f0").pack(pady=5)
    entry_login_mobile = tk.Entry(root_login)
    entry_login_mobile.pack(pady=5)
    
    tk.Label(root_login, text="Password", bg="#f0f0f0").pack(pady=5)
    entry_login_password = tk.Entry(root_login, show="*")
    entry_login_password.pack(pady=5)

    tk.Button(root_login, text="Login", command=login_client, bg="#4CAF50", fg="white").pack(pady=10)
    tk.Button(root_login, text="Forgot Password?", command=forgot_password, fg="red", bg="#f0f0f0").pack(pady=5)
    tk.Button(root_login, text="Not registered? Register Now!", command=register_page, fg="blue", bg="#f0f0f0").pack(pady=5)

    root_login.mainloop()
# Run the login page initially
login_page()
import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import messagebox, Entry, Label, Button, Toplevel, simpledialog
from tkinter import ttk
from PIL import Image
from datetime import datetime

# Directories for saving face data
data_path = "dataset/"
unknown_path = "unknown_faces/"
password = "118181"

# Ensure directories exist
if not os.path.exists(data_path):
    os.makedirs(data_path)
if not os.path.exists(unknown_path):
    os.makedirs(unknown_path)

# Load face detection cascade and recognizer
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()

def get_camera_source():
    """ Find the first available camera source """
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            cap.release()
            return i
    return 0

def create_dataset():
    """ Collect 50 images to create a dataset for face recognition """
    name = simpledialog.askstring("Input", "Enter Passenger Name:")
    if not name:
        return
    cap = cv2.VideoCapture(get_camera_source())
    count = 0
    user_folder = os.path.join(data_path, name)
    os.makedirs(user_folder, exist_ok=True)
    
    while count < 50:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            face_img = gray[y:y+h, x:x+w]
            face_img = cv2.resize(face_img, (200, 200))
            cv2.imwrite(f"{user_folder}/{count}.jpg", face_img)
            count += 1
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, f"Photo Count: {count}/50", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Creating Dataset", frame)
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    messagebox.showinfo("Success", f"Dataset Created for {name}!")

def train_model():
    """ Train the face recognition model with the dataset """
    faces = []
    labels = []
    label_dict = {}
    
    people = os.listdir(data_path)
    for idx, person in enumerate(people):
        person_folder = os.path.join(data_path, person)
        for img_name in os.listdir(person_folder):
            img_path = os.path.join(person_folder, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            faces.append(img)
            labels.append(idx)
        label_dict[idx] = person
    
    recognizer.train(faces, np.array(labels))
    recognizer.save("trainer.yml")
    np.save("labels.npy", label_dict)
    messagebox.showinfo("Success", "Training Completed!")

def recognize_face():
    """ Recognize faces from the camera feed """
    recognizer.read("trainer.yml")
    label_dict = np.load("labels.npy", allow_pickle=True).item()
    cap = cv2.VideoCapture(get_camera_source())
    unknown_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            face_img = gray[y:y+h, x:x+w]
            face_img = cv2.resize(face_img, (200, 200))
            label, confidence = recognizer.predict(face_img)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if confidence < 50:
                name = label_dict[label]
                cv2.putText(frame, f"{name} ({timestamp})", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                unknown_face_path = os.path.join(unknown_path, f"unknown_{unknown_count}.jpg")
                cv2.imwrite(unknown_face_path, face_img)
                unknown_count += 1
        
        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def start_training():
    """ Start model training """
    train_model()

def start_recognition():
    """ Start face recognition """
    recognize_face()

# GUI Setup
root = tk.Tk()
root.title("Passenger Photo Uploading Section")
root.geometry("400x350")
root.configure(bg="#f0f0f0")

style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=5)
style.configure("TLabel", font=("Arial", 12), background="#f0f0f0")

ttk.Button(root, text="Create Dataset", command=create_dataset).pack(pady=5)
ttk.Button(root, text="Train Model", command=start_training).pack(pady=5)

root.mainloop()
