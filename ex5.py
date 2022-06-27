import json
import os

input_json_path = "students_database.json"
database_directory_path = "semesters_databases"

registered_courses_key = "registered_courses"
student_name_key = "student_name"


def get_students_courses_dict(input_json_path):
    with open(input_json_path, 'r') as f:
        students_courses_dict = json.load(f)

    return students_courses_dict


def get_technion_courses(students_courses_json):
    students_courses_dict = get_students_courses_dict(students_courses_json)
    courses = []

    for student_item in students_courses_dict.values():
        for course_name in student_item[registered_courses_key]:
            if course_name not in courses:
                courses.append(course_name)

    return courses


def names_of_registered_students(input_json_path, course_name):
    students_courses_dict = get_students_courses_dict(input_json_path)

    students_list = []
    for student_item in students_courses_dict.values():
        if course_name in student_item[registered_courses_key]:
            students_list.append(student_item[student_name_key])

    # TODO: what about an empty list?
    return students_list


def enrollment_numbers(input_json_path, output_file_path):
    courses = get_technion_courses(students_courses_json=input_json_path)
    courses.sort()

    with open(output_file_path, 'w') as f:
        for course_name in courses:
            enroll_num = len(names_of_registered_students(
                input_json_path, course_name))
            course_enroll_number_str = '"' + \
                course_name + '" ' + str(enroll_num) + "\n"
            f.write(course_enroll_number_str)


def courses_for_lecturers(json_directory_path, output_json_path):
    """
    This function writes the courses given by each lecturer in json format.

    :param json_directory_path: Path of the semsters_data files.
    :param output_json_path: Path of the output json file.
    """
    pass
