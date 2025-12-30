import tkinter as tk
from firebase_admin import db
import firebase_admin
from firebase_admin import credentials
from datetime import datetime
import calendar

# Initialize Firebase Admin
cred = credentials.Certificate("faceattendancesystem-c0163-firebase-adminsdk-bci46-64e225a7d7.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://faceattendancesystem-c0163-default-rtdb.firebaseio.com/'
})

# Function to fetch attendance data from Firebase
def fetch_attendance_data():
    ref = db.reference("Students")
    return ref.get()

# Create the main application window
app = tk.Tk()
app.title("View Attendance Data")
app.geometry("1000x600")

# Fetch the attendance data
data = fetch_attendance_data()

# Create a canvas to display the attendance data with thick borders
canvas = tk.Canvas(app)
canvas.pack(fill=tk.BOTH, expand=True)

# Constants for cell dimensions and border thickness
cell_width = 180
cell_height = 30
border_thickness = 2
header_height = 40

# Headers for the table
headers = ['ID', 'Name', 'Total Presents', 'Total Absents', 'Attendance Percentage']

# Draw headers
for col_num, header in enumerate(headers):
    x1 = col_num * cell_width
    y1 = 0
    x2 = x1 + cell_width
    y2 = y1 + header_height
    canvas.create_rectangle(x1, y1, x2, y2, width=border_thickness)
    canvas.create_text(x1 + cell_width/2, y1 + header_height/2, text=header, font=('Arial', 12, 'bold'))

# Insert data into the canvas
for row_num, (student_id, student_info) in enumerate(data.items(), start=1): # type: ignore
    total_presents = student_info.get('total_presents', 0)
    total_absents = student_info.get('total_absents', 0)
    if total_presents + total_absents > 0:
        attendance_percentage = (total_presents / (total_presents + total_absents)) * 100
    else:
        attendance_percentage = 0
    values = [student_id, student_info['name'], total_presents, total_absents, f"{attendance_percentage:.2f}%"]

    for col_num, value in enumerate(values):
        x1 = col_num * cell_width
        y1 = row_num * cell_height + header_height
        x2 = x1 + cell_width
        y2 = y1 + cell_height
        canvas.create_rectangle(x1, y1, x2, y2, width=border_thickness)
        canvas.create_text(x1 + cell_width/2, y1 + cell_height/2, text=value, font=('Arial', 10))

# Start the Tkinter main loop
app.mainloop()
