import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import messagebox, Entry, Label, Button, Toplevel
from tkinter import ttk
from PIL import Image, ImageTk  # Import PIL for handling images
from datetime import datetime

# Paths
data_path = "dataset/"
unknown_path = "unknown_faces/"
password = "118181"

# Make directories if they don't exist
if not os.path.exists(data_path):
    os.makedirs(data_path)
if not os.path.exists(unknown_path):
    os.makedirs(unknown_path)

# Load classifiers
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()

def get_camera_source():
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            cap.release()
            return i
    return 0

def recognize_face():
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
            face_roi = frame[y:y+h, x:x+w]
            face_gray = gray[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(face_gray)
            
            if len(eyes) >= 2:  # Ensure real face with both eyes detected
                face_img = cv2.resize(face_gray, (200, 200))
                label, confidence = recognizer.predict(face_img)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                if confidence < 50:
                    name = label_dict[label]
                    cv2.putText(frame, f"{name} ({timestamp})", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                else:
                    unknown_face_path = os.path.join(unknown_path, f"unknown_{timestamp.replace(':', '-')}.jpg")
                    cv2.imwrite(unknown_face_path, face_roi)
                    cv2.putText(frame, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        
        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def check_password():
    def verify():
        if password_entry.get() == password:
            password_window.destroy()
            recognize_face()
        else:
            messagebox.showerror("Error", "Incorrect Password!")
    
    password_window = Toplevel(root)
    password_window.title("Enter Password")
    password_window.geometry("300x150")
    Label(password_window, text="Enter Password:").pack(pady=10)
    password_entry = Entry(password_window, show="*")
    password_entry.pack(pady=5)
    Button(password_window, text="Submit", command=verify).pack(pady=10)

# GUI Setup
root = tk.Tk()
root.title("Passenger Photo Uploading Section")
root.geometry("400x350")
root.configure(bg="#f0f0f0")

# Load the background image using PIL
bg_image_path = "D:/Railway_ticket.py/image_project/ima.jpg"  # Path to your image
bg_image = Image.open(bg_image_path)
bg_image = bg_image.resize((1100, 1100), Image.Resampling.LANCZOS)  # Resize to fit the window
bg_image = ImageTk.PhotoImage(bg_image)

# Set the background image in the window
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)  # Make the background fill the entire window

# Styling
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=5)
style.configure("TLabel", font=("Arial", 12), background="#f0f0f0")

# Add the "Start Recognition" button on top of the background image
ttk.Button(root, text="Start Recognition", command=check_password).pack(pady=5)

root.mainloop()
