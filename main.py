import os
import json
from canvasapi import *

# Config
URL = "https://canvas.nus.edu.sg"
TOKEN = "21450~xyXhGeH8xP4hQcBxZwQ34afUCcYPZKWwLTMMcBAw9EEzcAGE6Mmz3mAkT4ZMH2w3"
DOWNLOAD_FOLDER = "/Users/ngshijun/Desktop/NUS/Y4S1"
CHECKER = '/Users/ngshijun/Desktop/NUS/Y4S1/checker.json'

canvas = Canvas(URL, TOKEN)
user = canvas.get_user('self')

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

if not os.path.exists(CHECKER):
    with open(CHECKER, 'w') as f:
        f.write('{}')
    checker = {}
else:
    with open(CHECKER, 'r') as f:
        checker = json.load(f)

courses = user.get_courses(enrollment_state='active')

for course in courses:
    course_code = course.course_code
    course_name = course.name
    print(f"Course {course_code} - {course_name}")

    if course_code not in checker:
        checker[course_code] = {}

    for folder in course.get_folders():
        folder_name = folder.full_name[13:]
        print(f"Folder {folder_name}")

        if not os.path.exists(f"{DOWNLOAD_FOLDER}/{course_code}/{folder_name}"):
            os.makedirs(f"{DOWNLOAD_FOLDER}/{course_code}/{folder_name}")

        try:
            for file in folder.get_files():
                file_name = file.display_name
                print(f"File   {file_name}")

                if file_name not in checker:
                    checker[file_name] = 1
                    file.download(f"{DOWNLOAD_FOLDER}/{course_code}/{folder_name}/{file_name}")
        except:
            continue

with open(CHECKER, 'w') as f:
    json.dump(checker, f, indent=4)