import cv2
import pytesseract
import os
import csv
from datetime import datetime

# Define the directory containing image files
image_dir = "/content/"

# Create a directory to store extracted information and largest faces
output_dir = "/content/Extracted_Information/"
os.makedirs(output_dir, exist_ok=True)

# Get a list of image file names in the directory
image_files = [f for f in os.listdir(image_dir) if f.endswith((".jpg", ".png", ".jpeg"))]

# Load a pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize a dictionary to store the in/out status and count for each person
person_info = {}

# Define the last allowed time for people to go "out" and "in"
last_time_allowed = datetime.strptime("2023-12-31_18-00-00", "%Y-%m-%d_%H-%M-%S")

# Number of latecomers and people outside
latecomers = 0
outside_count = 0

# Iterate through each image file
for image_file in image_files:
    # Extract the person's ID from the image filename or any other method you have
    person_id = extract_person_id(image_file)  # Implement this function to extract the ID

    # If the person's ID is not in the dictionary, they are going in
    if person_id not in person_info:
        person_info[person_id] = {"status": "in", "count": 1}
    else:
        if person_info[person_id]["status"] == "out":
            # If the person's ID is already in the dictionary with "out" status, they are coming from "out" to "in"
            person_info[person_id]["status"] = "in"
        person_info[person_id]["count"] += 1

    # Check if the person is late
    if last_time_allowed <= datetime.now():
        latecomers += 1
    else:
        outside_count += 1

    # Construct the full path to the image
    image_path = os.path.join(image_dir, image_file)

    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale for face detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Initialize variables to keep track of the largest face and its size
    largest_face = None
    largest_face_size = 0

    # Iterate through detected faces to find the largest one
    for (x, y, w, h) in faces:
        face_size = w * h
        if face_size > largest_face_size:
            largest_face_size = face_size
            largest_face = (x, y, w, h)

    # Perform OCR to extract text from the image
    extracted_information = pytesseract.image_to_string(image)

    # Split the information into Name, Roll No, Course, Branch, and Validity
    info_lines = extracted_information.split('\n')
    name = info_lines[0]
    roll_no = info_lines[1]
    course = info_lines[2]
    branch = info_lines[3]
    validity = info_lines[4]

    # Store information for the current image
    image_info = {
        'Timestamp': datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
        'File Name': image_file,
        'Name': name,
        'Roll No': roll_no,
        'Course': course,
        'Branch': branch,
        'Validity': validity,
        'Largest Face': f"{os.path.splitext(image_file)[0]}_largest_face.jpg",  # Define here
        'In/Out Status': person_info[person_id]["status"],
        'Count': person_info[person_id]["count"],
        'Latecomers': latecomers,
        'Outside Count': outside_count
    }

    # Append the information to the list
    image_info_list.append(image_info)

    # Save only the largest face as a separate image in the output directory
    if largest_face is not None:
        x, y, w, h = largest_face
        largest_face_roi = image[y:y+h, x:x+w]
        largest_face_output_filename = os.path.splitext(image_file)[0] + '_largest_face.jpg'
        cv2.imwrite(os.path.join(output_dir, largest_face_output_filename), largest_face_roi)

# Append the extracted information to the CSV file
with open(csv_filename, mode='a', newline='') as csv_file:
    fieldnames = ['Timestamp', 'File Name', 'Name', 'Roll No', 'Course', 'Branch', 'Validity', 'Largest Face', 'In/Out Status', 'Count', 'Latecomers', 'Outside Count']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write information for each image
    for image_info in image_info_list:
        csv_writer.writerow(image_info)

# Print a message indicating the CSV file and largest face images have been created
print(f"Data added to CSV file '{csv_filename}' and largest face images have been saved in '{output_dir}'.")
