# views.py

from django.shortcuts import render
from django.http import JsonResponse
from .models import Person, ImageInfo

def upload_image(request):
    if request.method == 'POST':
        # Handle image upload and save data in the database
        person_id = request.POST.get('person_id')  # Example: You need to adjust this based on your form fields
        # ...

        # Save data to the database
        person, created = Person.objects.get_or_create(person_id=person_id)
        person_info = {
            'status': 'in' if created else 'out',
            'count': person.count,
        }
        # ...

        image_info = ImageInfo.objects.create(
            person=person,
            file_name=request.FILES['image'].name,
            largest_face=request.FILES['image'],
            latecomers=person_info['count'] if person_info['status'] == 'out' else 0,
            outside_count=person_info['count'] if person_info['status'] == 'in' else 0,
        )

        return JsonResponse({'success': True})
    else:
        return render(request, 'upload_image.html')

def display_data(request):
    # Fetch and display data from the database
    persons = Person.objects.all()
    image_info_list = ImageInfo.objects.all()
    # ...

    return render(request, 'display_data.html', {'persons': persons, 'image_info_list': image_info_list})




'''
# attendance_app/views.py
from django.shortcuts import render
from django.http import HttpResponse
from .models import Person, Attendance
from datetime import datetime
import os
import cv2
import pytesseract

# Your existing image processing logic here
def process_images(request):
    # Define the directory containing image files
    image_dir = "/content/"
    output_dir = "/content/Extracted_Information/"
    os.makedirs(output_dir, exist_ok=True)

    # Get a list of image file names in the directory
    image_files = [f for f in os.listdir(image_dir) if f.endswith((".jpg", ".png", ".jpeg"))]

    # Load a pre-trained face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Initialize variables
    image_info_list = []
    person_info = {}
    last_time_allowed = datetime.strptime("2023-12-31_18-00-00", "%Y-%m-%d_%H-%M-%S")
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

        # Check if the person_id exists in the database
        person, created = Person.objects.get_or_create(person_id=person_id)

        # Create an Attendance record
        Attendance.objects.create(
            person=person,
            timestamp=datetime.now(),
            file_name=image_file,
            name=name,
            roll_no=roll_no,
            course=course,
            branch=branch,
            validity=validity,
            largest_face=f"{os.path.splitext(image_file)[0]}_largest_face.jpg",
            in_out_status=person_info[person_id]["status"],
            count=person_info[person_id]["count"],
            latecomers=latecomers,
            outside_count=outside_count
        )

    # Continue with your existing logic

    return HttpResponse(f"Data added to the database and images saved in '{output_dir}'.")
'''