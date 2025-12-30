import cv2
import numpy as np
import os
from PIL import Image, ImageDraw

def create_realistic_face(student_id, name, variation_seed=0):
    """Create a more realistic face image that can be detected by face_recognition"""
    
    # Set random seed for consistent faces per student
    np.random.seed(hash(student_id) % 1000)
    
    # Create larger image for better detection
    img_size = 500
    img = np.ones((img_size, img_size, 3), dtype=np.uint8) * 245  # Very light background
    
    # Create face using PIL for smoother shapes
    pil_img = Image.fromarray(img)
    draw = ImageDraw.Draw(pil_img)
    
    center_x, center_y = img_size // 2, img_size // 2
    
    # Draw head (larger ellipse)
    head_width = 140 + np.random.randint(-20, 20)
    head_height = 180 + np.random.randint(-20, 20)
    skin_color = (220 + np.random.randint(-30, 10), 
                  180 + np.random.randint(-20, 15), 
                  150 + np.random.randint(-15, 15))
    
    # Head shape
    draw.ellipse([center_x - head_width//2, center_y - head_height//2 + 30,
                  center_x + head_width//2, center_y + head_height//2 + 30], 
                 fill=skin_color, outline=None)
    
    # Hair
    hair_color = (60 + np.random.randint(0, 100), 
                  40 + np.random.randint(0, 80), 
                  20 + np.random.randint(0, 60))
    draw.ellipse([center_x - head_width//2 - 10, center_y - head_height//2 + 10,
                  center_x + head_width//2 + 10, center_y + head_height//2 - 80], 
                 fill=hair_color, outline=None)
    
    # Convert back to numpy
    img = np.array(pil_img)
    
    # Add facial features using OpenCV for more precise control
    
    # Eyes
    eye_y = center_y - 10 + np.random.randint(-10, 10)
    left_eye_x = center_x - 35 + np.random.randint(-5, 5)
    right_eye_x = center_x + 35 + np.random.randint(-5, 5)
    
    # Eye whites
    cv2.ellipse(img, (left_eye_x, eye_y), (15, 8), 0, 0, 360, (255, 255, 255), -1)
    cv2.ellipse(img, (right_eye_x, eye_y), (15, 8), 0, 0, 360, (255, 255, 255), -1)
    
    # Eye pupils
    cv2.circle(img, (left_eye_x, eye_y), 7, (50, 50, 50), -1)
    cv2.circle(img, (right_eye_x, eye_y), 7, (50, 50, 50), -1)
    
    # Eye reflections
    cv2.circle(img, (left_eye_x - 3, eye_y - 2), 2, (200, 200, 200), -1)
    cv2.circle(img, (right_eye_x - 3, eye_y - 2), 2, (200, 200, 200), -1)
    
    # Eyebrows
    eyebrow_color = tuple(max(0, c - 50) for c in hair_color[:3])
    cv2.ellipse(img, (left_eye_x, eye_y - 20), (20, 5), 0, 0, 180, eyebrow_color, 3)
    cv2.ellipse(img, (right_eye_x, eye_y - 20), (20, 5), 0, 0, 180, eyebrow_color, 3)
    
    # Nose
    nose_y = center_y + 20
    nose_pts = np.array([[center_x, nose_y - 15], 
                         [center_x - 8, nose_y + 5], 
                         [center_x, nose_y + 8], 
                         [center_x + 8, nose_y + 5]], np.int32)
    
    nose_color = tuple(max(0, c - 30) for c in skin_color)
    cv2.fillPoly(img, [nose_pts], nose_color)
    
    # Nostrils
    cv2.circle(img, (center_x - 5, nose_y + 5), 2, tuple(max(0, c - 60) for c in skin_color), -1)
    cv2.circle(img, (center_x + 5, nose_y + 5), 2, tuple(max(0, c - 60) for c in skin_color), -1)
    
    # Mouth
    mouth_y = center_y + 55
    mouth_color = (150, 80, 80)
    
    # Upper lip
    cv2.ellipse(img, (center_x, mouth_y), (25, 8), 0, 0, 180, mouth_color, -1)
    # Lower lip
    cv2.ellipse(img, (center_x, mouth_y + 5), (22, 8), 0, 180, 360, mouth_color, -1)
    
    # Mouth line
    cv2.line(img, (center_x - 22, mouth_y), (center_x + 22, mouth_y), (120, 60, 60), 2)
    
    # Add some random facial marks for uniqueness
    for _ in range(2):
        mark_x = center_x + np.random.randint(-50, 50)
        mark_y = center_y + np.random.randint(-40, 40)
        mark_color = tuple(max(0, c - np.random.randint(10, 30)) for c in skin_color)
        cv2.circle(img, (mark_x, mark_y), 2, mark_color, -1)
    
    # Add name label at bottom
    cv2.putText(img, student_id, (20, img_size - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    cv2.putText(img, name, (20, img_size - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    
    return img

# Create Images directory if it doesn't exist
os.makedirs('Images', exist_ok=True)

# Sample student data (using IDs from the sendDataToDatabase.py)
students = [
    ("F21BINCE1M04001", "Muhammad Abid"),
    ("F21BINCE1M04002", "M. Israr Khalil"),
    ("F21BINCE1M04004", "Abdul Hanan"),
    ("F21BINCE1M04007", "Faghia Qammar"),
    ("F21BINCE1M04008", "Muhammad Sameer Khan")
]

print("Creating realistic sample face images...")

for i, (student_id, name) in enumerate(students):
    print(f"Creating face for {name} ({student_id})...")
    
    # Create realistic face image
    face_img = create_realistic_face(student_id, name, i)
    
    # Save the image
    filename = f'Images/{student_id}.jpg'
    cv2.imwrite(filename, face_img)
    print(f"✅ Saved: {filename}")

print("\n🎉 Realistic sample face images created successfully!")
print("📝 These images should be detectable by face_recognition library")
print("🔧 Run: python encodeGenerator.py to generate face encodings")
print("🚀 Then run: python face_attendance_offline.py to test face recognition")
