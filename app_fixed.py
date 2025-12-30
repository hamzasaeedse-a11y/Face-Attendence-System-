import tkinter as tk
from tkinter import messagebox
import subprocess
import os

# Define functions to run each script
def run_face_attendance():
    try:
        # Try offline version first
        subprocess.run(["python", "face_attendance_offline.py"], check=True)
        messagebox.showinfo("Success", "Face Attendance (Offline) completed successfully.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to run Face Attendance: {e}")

def run_face_attendance_online():
    try:
        subprocess.run(["python", "face_attendance.py"], check=True)
        messagebox.showinfo("Success", "Face Attendance (Online) completed successfully.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to run Face Attendance Online: {e}")

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
        subprocess.run(["python", "view_attendance_offline.py"], check=True)
        messagebox.showinfo("Success", "Attendance data viewed successfully.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to view attendance data: {e}")

def view_attendance_data_online():
    try:
        subprocess.run(["python", "view_attendance_data.py"], check=True)
        messagebox.showinfo("Success", "Attendance data (online) viewed successfully.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to view attendance data online: {e}")

def open_downloaded_excel():
    try:
        excel_path = "Student_Attendance.xlsx"
        if os.path.exists(excel_path):
            os.startfile(excel_path) if os.name == 'nt' else os.system(f'xdg-open "{excel_path}"')
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

def create_sample_data():
    try:
        subprocess.run(["python", "create_sample_students.py"], check=True)
        messagebox.showinfo("Success", "Sample student data created successfully.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to create sample data: {e}")

def quit_application():
    app.quit()

# Create the main application window
app = tk.Tk()
app.title("Face Attendance Management System (Fixed)")
app.geometry("1400x800")

# Create a frame to hold the buttons and descriptions
frame = tk.Frame(app)
frame.pack(pady=20, padx=20, anchor="w")

def create_button_with_description(frame, text, description, command, row, button_color):
    button = tk.Button(frame, text=text, command=command, width=35, height=2, bg=button_color, fg="white")
    button.grid(row=row, column=0, padx=10, pady=5, sticky="w")
    label = tk.Label(frame, text=description, wraplength=500, justify="left")
    label.grid(row=row, column=1, padx=10, pady=5, sticky="w")

# Add title
title_label = tk.Label(app, text="Face Attendance System - Fixed Version", 
                      font=('Arial', 16, 'bold'), fg="blue")
title_label.pack(pady=10)

# Section: OFFLINE COMPONENTS (Work without Firebase)
offline_label = tk.Label(frame, text="📱 OFFLINE FEATURES (Work without Firebase)", 
                        font=('Arial', 12, 'bold'), fg="green")
offline_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

create_button_with_description(
    frame, "Run Face Attendance (Offline)",
    "🎯 Run face attendance with local data storage. No Firebase required.",
    run_face_attendance, 1, "#2E8B57")

create_button_with_description(
    frame, "View Attendance Data (Offline)",
    "📊 View attendance data from local files. No Firebase required.",
    view_attendance_data, 2, "#2E8B57")

create_button_with_description(
    frame, "Generate Face Encodings",
    "🔧 Generate face recognition encodings from student images. Works offline.",
    generate_encodes, 3, "#2E8B57")

create_button_with_description(
    frame, "Create Sample Student Data",
    "👥 Create sample student images for testing the system.",
    create_sample_data, 4, "#2E8B57")

# Separator
separator1 = tk.Frame(frame, height=2, bd=1, relief="sunken")
separator1.grid(row=5, columnspan=2, sticky="we", pady=15)

# Section: ONLINE FEATURES (Require Firebase)
online_label = tk.Label(frame, text="🌐 ONLINE FEATURES (Require Firebase Setup)", 
                       font=('Arial', 12, 'bold'), fg="orange")
online_label.grid(row=6, column=0, columnspan=2, pady=10, sticky="w")

create_button_with_description(
    frame, "Run Face Attendance (Online)",
    "🚀 Full online face attendance with Firebase database sync.",
    run_face_attendance_online, 7, "#FF8C00")

create_button_with_description(
    frame, "View Attendance Data (Online)",
    "📈 View attendance data from Firebase database.",
    view_attendance_data_online, 8, "#FF8C00")

create_button_with_description(
    frame, "Download Full Data",
    "⬇️ Download complete attendance data from Firebase as Excel.",
    download_data, 9, "#FF8C00")

create_button_with_description(
    frame, "Open Downloaded Excel",
    "📄 Open the downloaded Excel file. Download data first.",
    open_downloaded_excel, 10, "#FF8C00")

# Separator
separator2 = tk.Frame(frame, height=2, bd=1, relief="sunken")
separator2.grid(row=11, columnspan=2, sticky="we", pady=15)

# Section: ADMIN FEATURES
admin_label = tk.Label(frame, text="⚙️ ADMIN FEATURES (Require Firebase)", 
                      font=('Arial', 12, 'bold'), fg="red")
admin_label.grid(row=12, column=0, columnspan=2, pady=10, sticky="w")

create_button_with_description(
    frame, "Upload Student Data",
    "⚠️ Upload student data to Firebase. This will replace existing data!",
    upload_data, 13, "#DC143C")

create_button_with_description(
    frame, "Upload Student Images",
    "📸 Upload student images to Firebase storage for recognition.",
    upload_images, 14, "#DC143C")

# Info section
info_frame = tk.Frame(app)
info_frame.pack(side="bottom", fill="x", pady=10)

info_text = tk.Text(info_frame, height=4, bg="lightyellow", wrap=tk.WORD)
info_text.pack(fill="x", padx=20)
info_text.insert("1.0", """ℹ️ QUICK START:
1. Use OFFLINE features to test the system without Firebase setup
2. For ONLINE features, setup Firebase credentials (see SETUP_GUIDE.md)  
3. Generate face encodings before running attendance system
4. Press 'q' in the camera window to quit face attendance""")
info_text.config(state="disabled")

# Create Quit button
btn_quit = tk.Button(app, text="Quit Application", command=quit_application, 
                    width=35, height=2, bg="#8B0000", fg="white")
btn_quit.pack(pady=10)

print("🎉 Face Attendance System (Fixed) started!")
print("✅ Use OFFLINE features for immediate testing")
print("🌐 Setup Firebase for ONLINE features")

# Start the Tkinter main loop
app.mainloop()
