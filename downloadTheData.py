import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate("faceattendancesystem-c0163-firebase-adminsdk-bci46-64e225a7d7.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://faceattendancesystem-c0163-default-rtdb.firebaseio.com/'
})

# Reference to the Students data
ref = db.reference("Students")
students_data = ref.get()

# Prepare data for the Excel file
attendance_data = {}
all_dates = set()

# Collect all dates with attendance data
for student_info in students_data.values(): # type: ignore
    daily_attendance = student_info.get('daily_attendance', {})
    for date_str in daily_attendance.keys():
        all_dates.add(date_str)

# Process data for each student
for student_id, student_info in students_data.items(): # type: ignore
    daily_attendance = student_info.get('daily_attendance', {})
    for date_str in all_dates:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        year_month = date_obj.strftime("%Y-%m")
        
        if year_month not in attendance_data:
            attendance_data[year_month] = []

        status = daily_attendance.get(date_str, "absent")
        attendance_data[year_month].append({
            'Student ID': student_id,
            'Name': student_info['name'],
            'Date': date_str,
            'Day': date_obj.day,
            'Status': status,
            'Total Presents': student_info.get('total_presents', 0),
            'Total Absents': student_info.get('total_absents', 0)
        })

# Create a well-formatted Excel file
excel_file_path = 'Student_Attendance.xlsx'
with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
    if not attendance_data:
        # Create a default sheet if no attendance data is present
        df = pd.DataFrame([{'Message': 'No attendance data available'}])
        df.to_excel(writer, sheet_name='No Data', index=False)
    else:
        for year_month, records in attendance_data.items():
            # Get the number of days in the month
            date_obj = datetime.strptime(year_month, "%Y-%m")
            days_in_month = pd.Period(year_month).days_in_month

            # Create a DataFrame
            df = pd.DataFrame(records)

            # Pivot the DataFrame to have days as columns
            pivot_df = df.pivot_table(
                index=['Student ID', 'Name', 'Total Presents', 'Total Absents'],
                columns='Day',
                values='Status',
                aggfunc='first'
            ).reset_index()

            # Add missing days as columns if not present
            for day in range(1, days_in_month + 1):
                if day not in pivot_df.columns:
                    pivot_df[day] = None

            # Sort columns to ensure days are in order
            cols = ['Student ID', 'Name', 'Total Presents', 'Total Absents'] + list(range(1, days_in_month + 1))
            pivot_df = pivot_df[cols]

            # Write to Excel sheet
            pivot_df.to_excel(writer, sheet_name=year_month, index=False)

            # Adjust column widths
            worksheet = writer.sheets[year_month]
            for column_cells in worksheet.columns:
                length = max(len(str(cell.value))+2 for cell in column_cells)
                worksheet.column_dimensions[column_cells[0].column_letter].width = length

print(f"Excel file '{excel_file_path}' created successfully.")
