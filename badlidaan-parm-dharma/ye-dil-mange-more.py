# --- Required Libraries ---
import cv2
import numpy as np
import os
import serial
import time

# --- Arduino Setup ---
# Update this to your Arduino COM port
arduino = serial.Serial('COM7', 9600)
time.sleep(2)  # Give Arduino time to initialize

# --- Constants ---
IMG_SIZE = (200, 200)  # Uniform resize for comparison

# --- Load Reference Images from Folders ---
def load_reference_images(folder_path="ref_images"):
    reference_data = {}
    for category in os.listdir(folder_path):
        category_path = os.path.join(folder_path, category)
        if not os.path.isdir(category_path):
            continue
        images = []
        for filename in os.listdir(category_path):
            img_path = os.path.join(category_path, filename)
            img = cv2.imread(img_path)
            if img is not None:
                img = cv2.resize(img, IMG_SIZE)
                images.append(img)
        reference_data[category] = images
    return reference_data

# --- Image Comparison Function ---
def match_item(input_image, reference_data):
    input_image = cv2.resize(input_image, IMG_SIZE)
    best_score = float('inf')
    best_category = None

    for category, images in reference_data.items():
        for ref_img in images:
            diff = cv2.absdiff(ref_img, input_image)
            score = np.sum(diff)
            if score < best_score:
                best_score = score
                best_category = category

    return best_category if best_score < 5000000 else None

# --- Main Webcam Loop ---
cap = cv2.VideoCapture(0)
ref_images = load_reference_images()

print("System is running. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    cv2.imshow("Live Feed", frame)
    category = match_item(frame, ref_images)

    if category:
        print("Detected:", category)
        if category == "organic":
            arduino.write(b'O')  # Tilt Motor 1 Right
        elif category == "plastic":
            arduino.write(b'P')  # Motor 1 Left + Motor 2 Left
        elif category == "metal":
            arduino.write(b'M')  # Motor 1 Left + Motor 2 Right
        time.sleep(3)  # Give time to actuate
    else:
        print("No match found")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
