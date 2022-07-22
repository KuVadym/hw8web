import sqlite3

def execute_query(sql: str) -> list:
    with sqlite3.connect('students_grades.db') as con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()

#5 студентов с наибольшим средним баллом по всем предметам.
def five_best():
    sql = """
    SELECT ROUND(AVG(s.grade), 4), st.student_name
    FROM students as st
        LEFT JOIN scores s ON  s.student_id = st.id
    GROUP BY st.student_name
    ORDER BY ROUND(AVG(s.grade), 4)
    DESC
    LIMIT 5
    """
    print(f'five best students {execute_query(sql)}')

#1 студент с наивысшим средним баллом по одному предмету.
def the_nuber_one():
    sql = """
    SELECT ROUND(AVG(s.grade), 4), sub.lesson, st.student_name
    FROM students as st
        LEFT JOIN scores s ON  s.student_id = st.id
        LEFT JOIN subjects sub ON  s.subjects_id = sub.id
    GROUP BY sub.lesson, st.student_name
    ORDER BY ROUND(AVG(s.grade), 4)
    DESC
    LIMIT 5
        """
    print(f'The best student for each subject {execute_query(sql)}')

#средний балл в группе по одному предмету.
def avg_scor_in_thread():
    sql = """
    SELECT g.group_number, ROUND(AVG(s.grade), 4), sub.lesson 
    FROM groups as g
        LEFT JOIN students st ON st.group_id = g.id
        LEFT JOIN scores s ON  s.student_id = st.id
        LEFT JOIN subjects sub ON  s.subjects_id = sub.id
    GROUP BY g.group_number, sub.lesson
    """
    print(f'avg score in groups by subjects is ({execute_query(sql)}')


#Средний балл в потоке.
def avg_scor():
    sql = """
    SELECT AVG(grade)
    FROM scores
    """
    print(f'avg score in thread is ({execute_query(sql)}')
#Какие курсы читает преподаватель.
def teachers_lessons():
    sql = """
    SELECT s.lesson, t.teacher_name 
    FROM teachers as t
        LEFT JOIN subjects s ON s.teacher_id = t.id
    """
    print(f'Subjects that teachers do: {execute_query(sql)}')

   
#Список студентов в группе.
def students_in_group(group_num):
    sql = f"""
    SELECT g.group_number, st.student_name
    FROM students as st
        LEFT JOIN groups g ON st.group_id = g.id
    WHERE g.group_number = {group_num}
    """
    print(f'Students list in {group_num} group {execute_query(sql)}')

#Оценки студентов в группе по предмету.
def grades_students_in_group(group_num):
    sql = f"""
    SELECT g.group_number, st.student_name, sc.grade
    FROM subjects as s
        LEFT JOIN scores sc ON sc.subjects_id = s.id
        LEFT JOIN students st ON sc.student_id = st.id
        LEFT JOIN groups g ON st.group_id = g.id
    WHERE g.group_number = {group_num}
    """
    print(f'Students list in {group_num} group {execute_query(sql)}')

#Оценки студентов в группе по предмету на последнем занятии.
def student_grade_by_subject_in_last_lesson():
    sql = f"""
    SELECT st.student_name, sub.lesson, s.grade, s.date_of_grade
    FROM students as st
        LEFT JOIN scores s ON s.student_id = st.id
        LEFT JOIN subjects sub ON s.subjects_id = sub.id
    WHERE s.date_of_grade = (SELECT MAX(date_of_grade) FROM scores)
    """
    print(f'Students grades by subject on last lesson {execute_query(sql)}') 

 
#Список курсов, которые посещает студент.
def students_subjects():
    sql = f"""
    SELECT DISTINCT st.student_name, sub.lesson
    FROM students as st
        LEFT JOIN scores s ON s.student_id = st.id
        LEFT JOIN subjects sub ON s.subjects_id = sub.id
    """
    print(f'Subjects that have each student {execute_query(sql)}') 


#Список курсов, которые студенту читает преподаватель.
def subjects_which_teacher_teach_each_student():
    sql = f"""
    SELECT DISTINCT st.student_name, sub.lesson, t.teacher_name
    FROM students as st
        LEFT JOIN scores s ON s.student_id = st.id
        LEFT JOIN subjects sub ON s.subjects_id = sub.id
        LEFT JOIN teachers t ON sub.teacher_id = t.id
    """
    print(f'Subjects that each teacher read each student {execute_query(sql)}') 



#Средний балл, который преподаватель ставит студенту.
def avg_score_student_from_teacher():
    sql = f"""
    SELECT ROUND(AVG(s.grade), 4), st.student_name, t.teacher_name
    FROM students as st
        LEFT JOIN scores s ON s.student_id = st.id
        LEFT JOIN subjects sub ON s.subjects_id = sub.id
        LEFT JOIN teachers t ON sub.teacher_id = t.id
    GROUP BY st.student_name, t.teacher_name
    """
    print(f'Averege grade that each teacher graded student {execute_query(sql)}')



#Средний балл, который ставит преподаватель.
def avg_score_by_teacher():
    sql = f"""
    SELECT ROUND(AVG(s.grade), 4), t.teacher_name
    FROM teachers as t
        LEFT JOIN subjects sub ON sub.teacher_id = t.id
        LEFT JOIN scores s ON s.subjects_id = sub.id
    GROUP BY t.teacher_name
    """
    print(f'Averege grade that each teacher graded student {execute_query(sql)}')

"""
five_best()
avg_scor_in_thread()
avg_scor()
the_nuber_one()
teachers_lessons() 
students_in_group(input('input group num: '))
grades_students_in_group(input('input group num: '))
student_grade_by_subject_in_last_lesson()
students_subjects()
subjects_which_teacher_teach_each_student()
avg_score_student_from_teacher()
avg_score_by_teacher()
    """