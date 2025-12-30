import tkinter as tk
from datetime import datetime
import os

# Offline version - reads from local file instead of Firebase
print("Loading Attendance Data (Offline Mode)")

def load_offline_attendance():
    """Load attendance data from local file"""
    attendance_data = {}
    
    if os.path.exists('offline_attendance.txt'):
        try:
            with open('offline_attendance.txt', 'r') as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split(',')
                        if len(parts) >= 4:
                            student_id, name, date, status = parts[:4]
                            
                            if student_id not in attendance_data:
                                attendance_data[student_id] = {
                                    'name': name,
                                    'total_presents': 0,
                                    'total_absents': 0,
                                    'daily_attendance': {}
                                }
                            
                            if status == 'present':
                                attendance_data[student_id]['total_presents'] += 1
                            else:
                                attendance_data[student_id]['total_absents'] += 1
                                
                            attendance_data[student_id]['daily_attendance'][date] = status
                            
        except Exception as e:
            print(f"Error loading offline attendance: {e}")
    
    # If no offline data, create sample data
    if not attendance_data:
        sample_students = [
            "F21BINCE1M04001",
            "F21BINCE1M04002", 
            "F21BINCE1M04004",
            "F21BINCE1M04007",
            "F21BINCE1M04008"
        ]
        
        for student_id in sample_students:
            attendance_data[student_id] = {
                'name': f'Student {student_id}',
                'total_presents': 0,
                'total_absents': 0,
                'daily_attendance': {}
            }
    
    return attendance_data

# Create the main application window
app = tk.Tk()
app.title("View Attendance Data (Offline)")
app.geometry("1000x600")

# Fetch the attendance data
data = load_offline_attendance()

# Create a canvas to display the attendance data with thick borders
canvas = tk.Canvas(app)
canvas.pack(fill=tk.BOTH, expand=True)

# Add scrollbar
scrollbar = tk.Scrollbar(app, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar.set)

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
    canvas.create_rectangle(x1, y1, x2, y2, width=border_thickness, fill="lightblue")
    canvas.create_text(x1 + cell_width/2, y1 + header_height/2, text=header, font=('Arial', 12, 'bold'))

# Insert data into the canvas
for row_num, (student_id, student_info) in enumerate(data.items(), start=1):
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
        
        # Color coding for attendance percentage
        fill_color = "white"
        if col_num == 4:  # Attendance percentage column
            if attendance_percentage >= 75:
                fill_color = "lightgreen"
            elif attendance_percentage >= 50:
                fill_color = "yellow"
            else:
                fill_color = "lightcoral"
        
        canvas.create_rectangle(x1, y1, x2, y2, width=border_thickness, fill=fill_color)
        canvas.create_text(x1 + cell_width/2, y1 + cell_height/2, text=value, font=('Arial', 10))

# Update scroll region
canvas.update_idletasks()
canvas.configure(scrollregion=canvas.bbox("all"))

# Add info label
info_label = tk.Label(app, text="Offline Mode - Data loaded from local file", 
                     font=('Arial', 10), bg="lightyellow", pady=5)
info_label.pack(side="bottom", fill="x")

if not os.path.exists('offline_attendance.txt'):
    no_data_label = tk.Label(app, text="No offline attendance data found. Run face_attendance_offline.py to generate data.", 
                           font=('Arial', 12), fg="red", pady=10)
    no_data_label.pack(side="bottom")

print(f"Displaying attendance data for {len(data)} students")

# Start the Tkinter main loop
app.mainloop()
