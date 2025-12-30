import pickle
import numpy as np

# Create dummy face encodings for testing (128-dimensional vectors)
# These won't work for actual face recognition, but will prevent crashes
dummy_encodings = []
student_ids = [
    "F21BINCE1M04001",
    "F21BINCE1M04002", 
    "F21BINCE1M04004",
    "F21BINCE1M04007",
    "F21BINCE1M04008"
]

print("Creating dummy encodings for testing...")

for student_id in student_ids:
    # Create a random 128-dimensional vector (face_recognition encoding size)
    dummy_encoding = np.random.random(128)
    dummy_encodings.append(dummy_encoding)
    print(f"Created dummy encoding for {student_id}")

# Save the encodings
encoded_images_with_ids = [dummy_encodings, student_ids]

with open('EncodedImages.p', 'wb') as file:
    pickle.dump(encoded_images_with_ids, file)

print(f"\nDummy encodings saved for {len(student_ids)} students")
print("Note: These are dummy encodings for testing only!")
print("Replace with real encodings using actual student photos for face recognition to work.")
