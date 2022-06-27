from distutils.command.sdist import sdist
from distutils.errors import DistutilsFileError
import json
import os

from attr import asdict


#################################################### Definitions ###################################################


input_json_path = "students_database.json"
database_directory_path = "semesters_databases"

registered_courses_key = "registered_courses"
student_name_key = "student_name"

course_name_key = "course_name"
lecturers_names_key = "lecturers"


################################################# Helper Functions #################################################


def get_json_files(input_json_path):
    json_list = [json_file for json_file in os.listdir(input_json_path) if json_file.endswith('.json')]
    return json_list


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


def build_lecturer_dict(semester_dict, output_dict):
    for course in semester_dict.values():
        for lecturer in course[lecturers_names_key]:
            if lecturer not in output_dict:
                output_dict[lecturer] = [course[course_name_key]]
            elif course[course_name_key] not in output_dict[lecturer]:
                output_dict[lecturer].append(course[course_name_key])


################################################# Actual EX5 Functions #################################################


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
    lecturer_course_dict = {}
    json_files_list = get_json_files(json_directory_path)

    for json_file in json_files_list:
        json_file_path = os.path.join(json_directory_path, json_file)
        with open(json_file_path, 'r') as course_json:
            build_lecturer_dict(json.load(course_json), lecturer_course_dict)

    with open(output_json_path, 'w') as output_lecturer_dict_json:
        json.dump(lecturer_course_dict, output_lecturer_dict_json, indent = 4)