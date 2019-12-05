"""
    COMET Project Specifications:
        
        Create an enlistment system where students can log in to take or drop classes
        and admin can create and remove classes.

        Students will have an ID number, name, and unit limit.

        Classes will have classroom, name, units, and prerequisites.

    Program Features:
        Login Screen ::
            Menu --
                Switch to Admin Login
                Switch to Student Login
                Quit
            
            Admin Login --
                Username
                Password

            Student Login --
                ID Number
                Password

        User Privileges ::
            Admin --
                Create Class
                    Classroom Number(String)
                    Name of Class(String)
                    Number of Units(Integer)
                    Classes as Prerequisites([Class])

                Remove Class
            
            Student --
                Take Class
                Drop Class
"""
import json

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)
    
    def info(self):
        return f'Admin / {self.username} / {self.password}'
        
class Student(User):
    def __init__(self, id_number, password, name, unit_limit):
        super().__init__(id_number, password)
        self.name = name
        self.unit_limit = int(unit_limit)
    
    def info(self):
        return f'Student / {self.username} / {self.password} / {self.name} / {self.unit_limit}'

class Course:
    def __init__(self, course_name, units, prereqs):
        self.course_name = course_name
        self.units = units
        self.prereqs = prereqs

    def info(self):
        info = [f'{self.course_name} / {self.units} / ']
        if not self.prereqs:
            info.append('')
        else:
            for pr in self.prereqs:
                info.append(f'{pr} ')
        return ''.join(info)

class Class:
    def __init__(self, course_name, classroom):
        self.course_name = course_name
        self.classroom = classroom
    
    def info(self):
        return f'{self.course_name} / {self.classroom}'

class ClassAssignment:
    def __init__(self, student_id, prev_enrolled, curr_enrolled):
        self.student_id = student_id
        self.prev_enrolled = prev_enrolled
        self.curr_enrolled = curr_enrolled
    
    def info(self):
        info = [f'{self.student_id} / ']

        if not self.prev_enrolled:
            info.append(' ')
        else: 
            for pe in self.prev_enrolled:
                info.append(f'{pe} ')

        info.append('- ')
        
        if not self.curr_enrolled:
            info.append(' ')
        else:
            for ce in self.curr_enrolled:
                info.append(f'{ce} ')

        return ''.join(info)

def parse_as_user(user):
    '''Takes a string representing user info and creates a user with that information.

    Parses a string and gets the relevant information such as username and password and
    returns an instance of a sub-class of a User (either Student or Admin).

    Args:
        user: String representation of the information of the user

    Returns:
        Either a Student or an Admin with the relevant information given in the string.
    '''
    read = user.split(' / ')
    if read[0] == 'Student':
        if len(read) != 5:
            return None
        else:
            return Student(read[1], read[2], read[3], read[4])
    else:
        if len(read) != 3:
            return None
        else:
            return Admin(read[1], read[2])

def parse_as_class(cl):
    '''Takes a string representing class info and creates a class with that information.

    Parses a string and gets the course name and classroom,
    and returns an instance of a Class.

    Args:
        cl: String representation of the class

    Returns:
        A Class with the relevant information from the string
    '''
    read = cl.split(' / ')
    if len(read) != 2:
        return None
    else:
        course_name = read[0]
        classroom = read[1]
        return Class(course_name, classroom)

def parse_as_course(course):
    '''Takes a string representing course info and creates a course with that information.

    Parses a string and gets the course name, units, and prerequisites,
    and returns an instance of a Course.

    Args:
        course: String representation of a Course

    Returns:
        A Course with the relevant information from the string
    '''
    read = course.split(' / ')
    if len(read) != 3:
        return None
    else:
        return Course(read[0], int(read[1]), read[2].split())

def parse_as_assignment(assignment):
    '''Takes a string representing a student and their classes and updates the corresponding student in
    the list of users.

    Parses a string and gets the relevant information such as the student ID and their previously enrolled and
    currently enrolled classes and updates the student in the database of users

    Args:
        assignment: String representation of the student and their prev. and current classes
        users: The database of users
    
    Returns:
        A ClassAssignment with the relevant information from the string
    '''
    read = assignment.split(' / ')
    if len(read) != 2:
        return None
    else:
        prev_enrolled = read[1].split('-')[0].strip()
        curr_enrolled = read[1].split('-')[1].strip()
        return ClassAssignment(read[0], prev_enrolled.split(), curr_enrolled.split())

def design_line(s, num):
    '''Returns a line of the specified string a number of times.
    
    Args:
        s: String to be printed
        num: The amount of times 's' is printed
        end: End of the line
    
    Returns:
        A string containing a line of the given string repeated several times.
        Given '=' and 5, for example:

        '====='

        Returns an empty string if num is less than 0.
    '''

    if num < 0:
        return ''
    str = []
    for _ in range(num):
        str.append (s)
    return ''.join(str)

def enrol_class(student, classes, class_assignments):
    '''Asks student in which classes the student wants to enrol in.

    Asks the student in which classes of the already created classes the student wants to enrol in,
    taking note of unit limit and prerequisites.

    Args:
        student: The student that will enrol in classes
        classes: The already existing list of classes
        class_assignments: The already existing list of students with their current and past enrolments
    '''
    
    student_assignment = class_assignments[student.username]
    prev_enrolled = student_assignment.prev_enrolled
    curr_enrolled = student_assignment.curr_enrolled
    unit_limit = student.unit_limit

    try:
        while True:
            print('Press Ctrl + C at any time to exit enrolling of classes\n')
            print('List of Classes')

            print(design_line('-', 100))
            print(f"{'Class Name':<20}{'Classroom':<15}{'Units':<7}{'Prerequisites':<30}")

            for cl in [value for _, value in sorted(classes.items())]:
                prereq_str = ', '.join(cl.prereqs)
                if len(prereq_str) >= 25:
                    prereq_str = f'{prereq_str[:25]}...'
                print(f'{cl.name:<20}{cl.classroom:<15}{cl.units:<7}{prereq_str:<30}')

            print(design_line('-', 100))

            print('You are currently enrolled in: ')
            for ce in curr_enrolled:
                print(ce)
            
            print(design_line('-', 100))

            class_name = input('Please input the name of the class you want to enrol in: ')
            classroom = input("Please input where it's going to be held: ")
            
            # if len(class_name) == 0 or len(classroom) == 0:
            #     print('Class name or classroom name cannot be blank, please try again.')
            # elif len(class_name) >= 20:
            #     print('Class name is too long (>= 20 characters), please try again.')
            # elif len(classroom) >= 15:
            #     print('Classroom name is too long (>= 15 characters), please try again.')
            # elif f'{class_name} / {classroom}' not in classes:
            #     print('Class with same name and classroom not found, please try again.')
            # elif class_name in prev_enrolled or class_name in curr_enrolled:
            #     print('You have already enrolled in this currently/before, please try again.')
            # elif classes[f'{class_name} / {classroom}'].units == 0:
            #     pass
            # else:
            #     break

            exit_enrol = False
            while True:
                query = input('Would you like to enrol in more classes? (y/n): ').lower()
                print(design_line('-', 100))
                if 'n' in query:
                    exit_enrol = True
                    break
                elif 'y' in query:
                    break
            
            if exit_enrol:
                print('Exiting enrolling...')
                print(design_line('-', 100))
                break

    except KeyboardInterrupt:
        print('\n-- Forced exit, exiting dropping... --')
        print(design_line('-', 100))

def drop_class(student, classes, class_assignments):
    '''Asks student in which classes the student wants to drop.

    Asks the student in which classes of the already created classes the student wants to enrol in.

    Args:
        student: The student that will enrol in classes
        classes: The already existing list of classes
        class_assignments: The already existing list of students with their current and past enrolments
    '''
    try:
        while True:
            print('Press Ctrl + C at any time to exit dropping of classes\n')
    except KeyboardInterrupt:
        print('\n-- Forced exit, exiting dropping... --')
        print(design_line('-', 100))

def create_class(classes):
    '''Asks admin for inputs to create a number of new classes.

    Asks the admin for details which include name of classes, classroom number, number of units, 
    and prerequisites to create any number of new classes.

    Args:
        classes: The already existing list of classes
    '''

    try:
        while True:
            print('Press Ctrl + C at any time to exit creation\n')
            print('List of Classes')
            
            print(design_line('-', 100))
            print(f"{'Class Name':<20}{'Classroom':<15}{'Units':<7}")

            for cl in [value for _, value in sorted(classes.items())]:
                print(f'{cl.name:<20}{cl.classroom:<15}{cl.units:<7}')

            print(design_line('-', 100))

            # class_name = None
            # classroom = None
            # while True:
            #     class_name = input('Please input the name of the new class: ')
            #     classroom = input("Please input where it's going to be held: ")
            #     if len(class_name) == 0 or len(classroom) == 0:
            #         print('Class name or classroom name cannot be blank, please try again.')
            #     elif len(class_name) >= 20:
            #         print('Class name is too long (>= 20 characters), please try again.')
            #     elif len(classroom) >= 15:
            #         print('Classroom name is too long (>= 15 characters), please try again.')
            #     elif f'{class_name} / {classroom}' in classes:
            #         print('Class with same name and classroom already found, please try again.')
            #     else:
            #         break
            #     print(design_line('-', 100))
            
            # units = None
            # while True:
            #     try:
            #         units = int(input('Please input how many units the class will be worth: '))
            #         if units < 0 or units > 50:
            #             print('Units cannot be less than 0 or more than 50, please try again.')
            #         else:
            #             break
            #     except ValueError:
            #         print('Input was not an integer, please try again.') 
            #     print(design_line('-', 100))

            # prereqs = None
            # found_class = None
            # while True:
            #     prereqs = input('Please input what prereqs the class will or will not have (separated by spaces): ').split()
            #     for prereq in prereqs:
            #         if prereq not in [cl.name for cl in classes.values()]:
            #             found_class = prereq
            #             break
            #     else:
            #         break
            #     print(f'Specified class ({found_class}) was not in already existing list of classes. Please try again.')
            #     print(design_line('-', 100))

            # if not prereqs:
            #     prereqs = ['None']
            
            # new_class = Class(class_name, classroom, units, prereqs)
            # classes[f'{new_class.name} / {new_class.classroom}'] = new_class

            # print(design_line('-', 100))
            # print(f'{new_class.name} in room {new_class.classroom} with units {new_class.units} was added.')

            exit_add = False
            while True:
                query = input('Would you like to add more classes? (y/n): ').lower()
                print(design_line('-', 100))
                if 'n' in query:
                    exit_add = True
                    break
                elif 'y' in query:
                    break
            
            if exit_add:
                print('Exiting addition...')
                print(design_line('-', 100))
                break

    except KeyboardInterrupt:
        print('\n-- Forced exit, exiting addition... --')
        print(design_line('-', 100))
            
def remove_class(classes):
    '''Asks admin for inputs to delete a number of new classes.

    Asks the admin which of all the previously created classes they want to delete.

    Args:
        classes: The already existing list of classes
    '''

    try:
        while True:
            print('Press Ctrl + C at any time to exit deletion.\n')
            print('List of Classes')
            
            print(design_line('-', 100))
            print(f"{'Class Name':<20}{'Classroom':<15}{'Units':<7}")

            for cl in [value for _, value in sorted(classes.items())]:
                print(f'{cl.name:<20}{cl.classroom:<15}{cl.units:<7}')

            print(design_line('-', 100))

            # class_name = None
            # classroom = None
            # while True:
            #     class_name = input('Please input the name of the deleted class: ')
            #     classroom = input("Please input the class' classroom: ")
            #     if len(class_name) == 0 or len(classroom) == 0:
            #         print('Class name or classroom name cannot be blank, please try again.')
            #     elif len(class_name) >= 20:
            #         print('Class name is too long (>= 20 characters), please try again.')
            #     elif len(classroom) >= 15:
            #         print('Classroom name is too long (>= 15 characters), please try again.')
            #     elif f'{class_name} / {classroom}' not in classes:
            #         print('Specified combination of class and classroom is not in classes, please try again.')
            #     else:
            #         del classes[f'{class_name} / {classroom}']
            #         break
            #     print(design_line('-', 100))

            # print(design_line('-', 100))
            # print(f'{class_name} in room {classroom} was deleted.')

            exit_del = False
            while True:
                query = input('Would you like to delete more classes? (y/n): ').lower()
                print(design_line('-', 100))
                if 'n' in query:
                    exit_del = True
                    break
                elif 'y' in query:
                    break
            
            if exit_del:
                print('Exiting deletion...')
                print(design_line('-', 100))
                break

    except KeyboardInterrupt:
        print('\n-- Forced exit, exiting deletion... --')
        print(design_line('-', 100))

def create_course(courses):
    pass

def remove_course(courses):
    pass

def edit_student(edited_user, is_admin = False):
    pass

def main():
    users = {}
    courses = {}
    classes = {}
    class_assignments = {}

    with open('users.txt') as users_txt:
        for user in users_txt.readlines():
            parsed_user = parse_as_user(user.strip())
            if parsed_user is not None:
                users[parsed_user.username] = parsed_user
            
    with open('courses.txt') as courses_txt:
        for course in courses_txt.readlines():
            parsed_course = parse_as_course(course.strip('\n'))
            if parsed_course is not None:
                courses[parsed_course.course_name] = parsed_course

    with open('classes.txt') as classes_txt:
        for cl in classes_txt.readlines():
            parsed_class = parse_as_class(cl.strip())
            if parsed_class is not None:
                classes[f'{parsed_class.course_name} / {parsed_class.classroom}'] = parsed_class

    with open('class_assignments.txt') as class_assignments_txt:
        for assignment in class_assignments_txt.readlines():
            parsed_assignment = parse_as_assignment(assignment.strip())
            if parsed_assignment is not None:
                class_assignments[parsed_assignment.student_id] = parsed_assignment

    exit_login = False
    login_user = None
    while True:
        print(design_line('=', 100))
        username = input('Lozol Account Username: ')
        password = input('Lozol Account Password: ')
        print(design_line('=', 100))

        found = False
        if username not in users or users[username].password != password:
            print('Invalid login details.')
            while True:
                query = input('Exit program? (y or n): ').lower()
                if 'y' in query: 
                    exit_login = True
                    break
                elif 'n' in query:
                    break
        else:
            login_user = users[username]
            print('Login found. Proceeding to user page.')
            break
            
    if not exit_login:
        if isinstance(login_user, Admin):
            print(f'Welcome to your administrator dashboard, {login_user.username}')
            print('[1] Create Class')
            print('[2] Remove Class')
            print('[3] Create Course')
            print('[4] Remove Course')
            # print('[3] Edit Student Information')
            num = int(input('Please enter your choice: '))
            print(design_line('=', 100))
            choices = {1 : create_class, 2 : remove_class, 3 : create_course, 4 : remove_course}
            if num == 1 or num == 2:
                choices[num](classes)
            elif num == 3 or num == 4:
                pass
                # choices[num](courses)
            else:
                pass
                # print(design_line('=', 100))
                # students = {i : student for i, student in users if isinstance(student, Student)}
                # for student in enumerate(students):
                #     print(f'[{i + 1}] {student.name}')
                # num = input('Please enter the full name of the student to be edited: ')
        elif isinstance(login_user, Student):
            print(f'Welcome to your Lozol Account, {login_user.name}')
            print('[1] Enrol in Class')
            print('[2] Drop a Class')
            # print('[3] Edit your Information')
            num = int(input('Please input your choice: '))
            choices = {1 : enrol_class, 2 : drop_class, 3 : edit_student} #TODO(Mscizor) : Finish defined functions here
            if num == 1 or num == 2:
                choices[num](login_user, classes, class_assignments)

    print (design_line('=', 100))
    print ('Exiting...')

    with open('users.txt', 'w') as users_txt:
        for i, user in enumerate(users.values()):
            users_txt.write(user.info())
            if i != len(users.values()) - 1:
                users_txt.write('\n')

    with open('courses.txt', 'w') as courses_txt:
        for i, user in enumerate(courses.values()):
            courses_txt.write(user.info())
            if i != len(courses.values()) - 1:
                courses_txt.write('\n')

    with open('classes.txt', 'w') as classes_txt:
        for i, cl in enumerate(classes.values()):
            classes_txt.write(cl.info())
            if i != len(classes.values()) - 1:
                classes_txt.write('\n')

    with open('class_assignments.txt', 'w') as class_assignments_txt:
        for i, st in enumerate(class_assignments.values()):
            class_assignments_txt.write(st.info())
            if i != len(class_assignments.values()) - 1:
                class_assignments_txt.write('\n')

if __name__ == '__main__':
    main()