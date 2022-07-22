from datetime import datetime
from faker.providers import BaseProvider
import faker
from faker import Faker
from random import randint, choice
import sqlite3

NUMBER_GROUPS = 3
NUMBER_TEACHER   = 3
NUMBER_STUDENTS = 30
NUMBER_SUBJECTS = 5
NUMBER_SCORES = 20
lessons_list = ['Agriculture', 'Agriculture', 'Horticulture', 'Plant and Crop Sciences', 'Veterinary Medicine', 'Computer Science', 
                'Computing', 'IT', 'Multimedia', 'Software', 'Astronomy', 'Biology', 'Chemistry', 'Earth Sciences', 'Environmental Sciences', 
                'Food Science and Technology', 'Forensic science', 'General Sciences', 'Life Sciences', 'Materials Sciences', 'Mathematics', 
                'Physical Geography', 'Physics', 'Sports Science']

fake_lesson = Faker()
class MyProvider(BaseProvider):
    def lesson(self, lessons_list):
        result = choice(lessons_list)
        return result

fake_lesson.add_provider(MyProvider)


def generate_fake_data(number_teachers, number_students, number_subjects) -> tuple():
    fake_teachers = []  # here will save teacher names
    fake_students = []  # here will save students
    fake_subjects = []  # here will save subjects

    fake_data = faker.Faker()

    # generate teachers and add them to the list (further similarly)
    for _ in range(number_teachers):
        fake_teachers.append(fake_data.name())

    #students
    for _ in range(number_students):
        fake_students.append(fake_data.name())

    # subjects
    for _ in range(number_subjects):
        fake_subjects.append(fake_lesson.lesson(lessons_list))

    return fake_teachers, fake_students, fake_subjects


def prepare_data(teachers, students, subjects) -> tuple():
    # preparing a list of group tuples (further similarly)
    for_groups = []
    group_num = 1
    for group in range (1, NUMBER_GROUPS + 1):
        for_groups.append((group_num, ))
        group_num += 1

    # students
    for_students = []  
    for student in students:
        for_students.append((student, randint(1, NUMBER_GROUPS)))
    

    for_teachers = []
    # teachers
    for teacher in teachers:
        for_teachers.append((teacher, ))

    for_subjects = []
    # subjects
    for subject in subjects:
        for_subjects.append((subject, randint(1, NUMBER_TEACHER)))        

    # grades  (scores)
    for_score = []
    for subject in range(1, NUMBER_SUBJECTS + 1):
        # Loop through the number of subjects
        for date in range(1, NUMBER_SCORES + 1):
            # Looping through grade dates
            score_date = datetime(2022, randint(1, 3), randint(1, 28)).date()
            for student in range(1, NUMBER_STUDENTS + 1):
                # Looping through by the number of students
                for_score.append((student, subject, score_date, randint(1, 5)))

    return for_groups, for_students, for_teachers, for_subjects, for_score


def insert_data_to_db(groups, students, teachers, subjects, score) -> None:
    with sqlite3.connect('students_grades.db') as con:
        cur = con.cursor()


        sql_to_groups = """INSERT INTO groups(group_number)
                               VALUES (?)"""
        cur.executemany(sql_to_groups, groups)


        sql_to_students = """INSERT INTO students(student_name, group_id)
                               VALUES (?, ?)"""
        cur.executemany(sql_to_students, students)


        sql_to_teachers = """INSERT INTO teachers(teacher_name)
                               VALUES (?)"""
        cur.executemany(sql_to_teachers, teachers)


        sql_to_subjects = """INSERT INTO subjects(lesson, teacher_id)
                               VALUES (?, ?)"""
        cur.executemany(sql_to_subjects, subjects)


        sql_to_scores = """INSERT INTO scores(student_id, subjects_id, date_of_grade, grade)
                              VALUES (?, ?, ?, ?)"""
        cur.executemany(sql_to_scores, score)


        con.commit()


if __name__ == "__main__":
    teachers, students, subjects = generate_fake_data(NUMBER_TEACHER, NUMBER_STUDENTS, NUMBER_SUBJECTS)
    groups, students, teachers, subjects, score = prepare_data(teachers, students, subjects)
    insert_data_to_db(groups, students, teachers, subjects, score)


