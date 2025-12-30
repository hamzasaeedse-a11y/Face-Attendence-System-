import tkinter as tk
from tkinter import messagebox
import subprocess
import os

# Define functions to run each script
def run_face_attendance():
    try:
        subprocess.run(["python", "face_attendance.py"], check=True)
        messagebox.showinfo("Success", "Face Attendance script completed successfully.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to run Face Attendance: {e}")

def download_data():
    try:
        subprocess.run(["python", "downloadTheData.py"], check=True)
        messagebox.showinfo("Success", "Data downloaded successfully.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to download data: {e}")

def upload_data():
    try:
        subprocess.run(["python", "sendDataToDatabase.py"], check=True)
        messagebox.showinfo("Success", "Data uploaded successfully.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to upload data: {e}")

def upload_images():
    try:
        subprocess.run(["python", "sendImagesToDatabase.py"], check=True)
        messagebox.showinfo("Success", "Images uploaded successfully.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to upload images: {e}")

def view_attendance_data():
    try:
        subprocess.run(["python", "view_attendance_data.py"], check=True)
        messagebox.showinfo("Success", "Attendance data viewed successfully.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to view attendance data: {e}")

def open_downloaded_excel():
    try:
        excel_path = "Student_Attendance.xlsx"
        if os.path.exists(excel_path):
            os.startfile(excel_path)
        else:
            messagebox.showerror("Error", "Excel file not found.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open Excel file: {e}")

def generate_encodes():
    try:
        subprocess.run(["python", "encodeGenerator.py"], check=True)
        messagebox.showinfo("Success", "Encodes generated successfully.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to generate encodes: {e}")

def quit_application():
    app.quit()

# Create the main application window
app = tk.Tk()
app.title("Attendance Management System")
app.geometry("1280x720")

# Create a frame to hold the buttons and descriptions
frame = tk.Frame(app)
frame.pack(pady=20, padx=20, anchor="w")

def create_button_with_description(frame, text, description, command, row, button_color):
    button = tk.Button(frame, text=text, command=command, width=30, height=2, bg=button_color, fg="white")
    button.grid(row=row, column=0, padx=10, pady=5, sticky="w")
    label = tk.Label(frame, text=description, wraplength=400, justify="left")
    label.grid(row=row, column=1, padx=10, pady=5, sticky="w")

# creating the buttons by calling above function
create_button_with_description(
    frame, "Run Face Attendance",
    "Run the face attendance script to record student attendance using facial recognition.",
    run_face_attendance, 0, "#4077ad")

create_button_with_description(
    frame, "Quick OverView Attendance Data",
    "Quick View the attendance data in a readable format.",
    view_attendance_data, 1, "#4077ad")

create_button_with_description(
    frame, "Download Full Data",
    "Download the full attendance data from the database and save as EXCEL file.",
    download_data, 2, "#4077ad")

create_button_with_description(
    frame, "Open Downloaded Excel",
    "Open the downloaded Excel file to view attendance data. \nNOTE: Download the data first",
    open_downloaded_excel, 3, "#4077ad")

line = tk.Frame(frame, height=2, bd=1, relief="sunken")
line.grid(row=4, columnspan=2, sticky="we", pady=10)

create_button_with_description(
    frame, "Upload Data",
    "Upload the updated attendance data to the database. \nALERT! This will erase all previous RECORDS",
    upload_data, 5, "#ab7e1d")

create_button_with_description(
    frame, "Upload Images",
    "Upload student images to the database for facial recognition.",
    upload_images, 6, "#ab7e1d")

create_button_with_description(
    frame, "Generate Encodes",
    "Generate face encodings for the uploaded student images.",
    generate_encodes, 7, "#ab7e1d")

# Create Quit button
btn_quit = tk.Button(app, text="Quit Application", command=quit_application, width=30, height=2, bg="#a13333", fg="white")
btn_quit.pack(pady=10, padx=20, anchor="w")

# Start the Tkinter main loop
app.mainloop()
