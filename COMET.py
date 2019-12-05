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
    def __init__(self, course_name, classroom, student_ids):
        self.course_name = course_name
        self.classroom = classroom
        self.student_ids = student_ids
    
    def info(self):
        info = [f'{self.course_name} / {self.classroom} / ']
        for s_id in self.student_ids:
            info.append(f'{s_id} ')
        return ''.join(info)

class PrevEnrolments:
    def __init__(self, student_id, prev_enrolled):
        self.student_id = student_id
        self.prev_enrolled = prev_enrolled
    
    def info(self):
        info = [f'{self.student_id} / ']

        if not self.prev_enrolled:
            info.append(' ')
        else: 
            for pe in self.prev_enrolled:
                info.append(f'{pe} ')

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
    if len(read) != 3:
        return None
    else:
        return Class(read[0], read[1], read[2].split())

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

def parse_as_prev_enrolments(prev_enrolments):
    '''Takes a string representing a student and their previous enrolments and returns a class representing that

    Parses a string and gets the relevant information such as the student ID and their previously enrolled courses
    returns a PrevEnrolment that links the two

    Args:
        prev_enrolments: String representation of the student and their previous enrolments

    Returns:
        A PrevEnrolments with the relevant information from the string
    '''
    read = prev_enrolments.split(' / ')
    if len(read) != 2:
        return None
    else:
        return PrevEnrolments(read[0], read[1].split())

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

def enrol_class(student, courses, classes, prev_enrolments):
    '''Asks student in which classes the student wants to enrol in.

    Asks the student in which classes of the already created classes the student wants to enrol in,
    taking note of unit limit and prerequisites.

    Args:
        student: The student that will enrol in classes
        classes: The already existing list of classes
        prev_enrolments: The already existing list of students with their current and past enrolments
    '''

    prev_enrolments = prev_enrolments[student.username].prev_enrolled
    try:
        while True:
            curr_enrolled = set()
            courses_enrolled = set()
            units_remaining = student.unit_limit
            for cl in classes.values():
                if student.username in cl.student_ids:
                    courses_enrolled.add(cl.course_name)
                    curr_enrolled.add(f'{cl.course_name} / {cl.classroom}')
                    units_remaining -= courses[cl.course_name].units

            avail_classes = set()
            for cl in classes.values():
                course = courses[cl.course_name]
                # Lengthy way of checking if can fit in units and the course of the class has not been previously or currently enrolled
                if course.units <= units_remaining and cl.course_name not in courses_enrolled and cl.course_name not in prev_enrolments:
                    for prereq in course.prereqs:
                        if prereq not in prev_enrolments:
                            break
                    else:
                        avail_classes.add(cl)

            if not avail_classes:
                print('No classes available for you to enrol in (may be due to units remaining, or previous/current enrolments).')
                print('Exiting enrolment...')
                break

            print('Press Ctrl + C at any time to exit enrolling of classes\n')
            print('List of Classes')

            print(design_line('-', 100))
            print(f"{'Class Name':<20}{'Classroom':<15}")

            def take_name(cl):
                return cl.course_name

            for cl in sorted(avail_classes, key = take_name):
                print(f'{cl.course_name:<20}{cl.classroom:<15}')

            print(design_line('-', 100))

            print('You are currently enrolled in: ')
            if not curr_enrolled:
                print('No classes')
            else:
                for ce in curr_enrolled:
                    print(ce)
            
            print(design_line('-', 100))

            while True:
                course_name = input('Please input the name of the class you want to enrol in: ')
                classroom = input("Please input where it's going to be held: ")
                
                if not course_name or not classroom:
                    print('Class name or classroom name cannot be blank, please try again.')
                elif len(course_name) >= 20:
                    print('Class name is too long (>= 20 characters), please try again.')
                elif len(classroom) >= 15:
                    print('Classroom name is too long (>= 15 characters), please try again.')
                elif classes[f'{course_name} / {classroom}'] not in avail_classes:
                    print('Class with same name and classroom not found, please try again.')
                else:
                    classes[f'{course_name} / {classroom}'].student_ids.append(student.username)
                    break

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

def drop_class(student, classes):
    '''Asks student in which classes the student wants to drop.

    Asks the student in which classes of the already created classes the student wants to enrol in.

    Args:
        student: The student that will enrol in classes
        classes: The already existing list of classes
        prev_enrolments: The already existing list of students with their current and past enrolments
    '''
    
    try:
        while True:
            curr_enrolled = set()
            for cl in classes.values():
                if student.username in cl.student_ids:
                    curr_enrolled.add(cl)

            if not curr_enrolled:
                print('No available classes to drop.')
                print('Exiting dropping...')
                break

            print('Press Ctrl + C at any time to exit dropping of classes\n')
            print('List of Currently Enrolled in Classes')

            print(design_line('-', 100))
            print(f"{'Class Name':<20}{'Classroom':<15}")

            def take_name(cl):
                return cl.course_name

            for cl in sorted(curr_enrolled, key = take_name):
                print(f'{cl.course_name:<20}{cl.classroom:<15}')

            print(design_line('-', 100))

            while True:
                course_name = input('Please input the name of the class you want to drop: ')
                classroom = input("Please input where the class is held: ")
                
                if not course_name or not classroom:
                    print('Class name or classroom name cannot be blank, please try again.')
                elif len(course_name) >= 20:
                    print('Class name is too long (>= 20 characters), please try again.')
                elif len(classroom) >= 15:
                    print('Classroom name is too long (>= 15 characters), please try again.')
                elif classes[f'{course_name} / {classroom}'] not in curr_enrolled:
                    print('Class with same name and classroom not found, please try again.')
                else:
                    classes[f'{course_name} / {classroom}'].student_ids.remove(student.username)
                    break

            exit_enrol = False
            while True:
                query = input('Would you like to drop more classes? (y/n): ').lower()
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

def create_class(courses, classes):
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
            print(f"{'Class Name':<20}{'Classroom':<15}")

            if not classes:
                print('No Classes Available')
            else:
                for cl in [value for _, value in sorted(classes.items())]:
                    print(f'{cl.course_name:<20}{cl.classroom:<15}')

            print(design_line('-', 100))

            if not courses:
                print('No courses available to make a class for.')
                print('Exiting creation...')
                break

            print('List of Courses')
            print(f"{'Course Name':<20}{'Units':<7}")
            
            for c in [value for _, value in sorted(courses.items())]:
                print(f'{c.course_name:<20}{c.units:<7}')

            print(design_line('-', 100))

            course_name = None
            classroom = None
            while True:
                course_name = input('Please input the name of the course of the new class: ')
                classroom = input("Please input where it's going to be held: ")
                if not course_name or not classroom:
                    print('Course name or classroom name cannot be blank, please try again.')
                elif len(course_name) >= 20:
                    print('Course name is too long (>= 20 characters), please try again.')
                elif len(classroom) >= 15:
                    print('Classroom name is too long (>= 15 characters), please try again.')
                elif f'{course_name} / {classroom}' in classes:
                    print('Class with same name and classroom already found, please try again.')
                elif course_name not in courses:
                    print('Course not in previously made courses, please try again.')
                else:
                    classes[f'{course_name} / {classroom}'] = Class(course_name, classroom, list())
                    break
                print(design_line('-', 100))

            print(design_line('-', 100))
            print(f'{course_name} in room {classroom} was added.')

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
            print(f"{'Class Name':<20}{'Classroom':<15}")

            for cl in [value for _, value in sorted(classes.items())]:
                print(f'{cl.course_name:<20}{cl.classroom:<15}')

            print(design_line('-', 100))

            course_name = None
            classroom = None
            while True:
                course_name = input('Please input the name of the to be deleted class: ')
                classroom = input("Please input the class' classroom: ")
                if not course_name or not classroom:
                    print('Class name or classroom name cannot be blank, please try again.')
                elif len(course_name) >= 20:
                    print('Class name is too long (>= 20 characters), please try again.')
                elif len(classroom) >= 15:
                    print('Classroom name is too long (>= 15 characters), please try again.')
                elif f'{course_name} / {classroom}' not in classes:
                    print('Specified combination of class and classroom is not in classes, please try again.')
                else:
                    del classes[f'{course_name} / {classroom}']
                    break
                print(design_line('-', 100))

            print(design_line('-', 100))
            print(f'{course_name} in room {classroom} was deleted.')

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
    '''Asks admin for inputs to create a number of new courses.

    Asks the admin for details which include name of courses, number of units, 
    and prerequisites to create any number of new courses.

    Args:
        courses: The already existing list of courses
    '''

    try:
        while True:
            print('Press Ctrl + C at any time to exit creation\n')
            print('List of Courses')
            
            print(design_line('-', 100))
            print(f"{'Course Name':<20}{'Units':<7}")

            for c in [value for _, value in sorted(courses.items())]:
                print(f'{c.course_name:<20}{c.units:<7}')

            print(design_line('-', 100))

            course_name = None
            while True:
                course_name = input('Please input the name of the new course: ')
                if not course_name:
                    print('Course name cannot be blank, please try again.')
                elif len(course_name) >= 20:
                    print('Course name is too long (>= 20 characters), please try again.')
                elif course_name in courses:
                    print('Course with same name already found, please try again.')
                else:
                    break
                print(design_line('-', 100))
            
            units = None
            while True:
                try:
                    units = int(input('Please input how many units the course will be worth: '))
                    if units < 0 or units > 50:
                        print('Units cannot be less than 0 or more than 50, please try again.')
                    else:
                        break
                except ValueError:
                    print('Input was not an integer, please try again.') 
                print(design_line('-', 100))

            prereqs = None
            while True:
                prereqs = input('Please input what prereqs the course will or will not have (separated by spaces): ').strip().split()
                for prereq in prereqs:
                    if prereq not in courses:
                        break
                else:
                    break
                print('At least one of the prerequisites specified was not in already existing list of classes. Please try again.')
                print(design_line('-', 100))

            if not prereqs:
                prereqs = ['None']
            
            new_course = Course(course_name, units, prereqs)
            courses[course_name] = new_course

            print(design_line('-', 100))
            print(f'{new_course.course_name} with units {new_course.units} was added.')

            exit_add = False
            while True:
                query = input('Would you like to add more courses? (y/n): ').lower()
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

def remove_course(courses, classes):
    '''Asks admin for inputs to remove a number of new courses.

    Asks the admin which of all the previously created courses they want to delete.

    Args:
        courses: The already existing list of courses
    '''

    try:
        while True:
            unavail_courses = set()
            for course in courses.values():
                unavail_courses.update(course.prereqs)

            for cl in classes.values():
                unavail_courses.add(cl.course_name)
            
            avail_courses = set()
            for c in [c for _, c in sorted(courses.items())]:
                if c.course_name not in unavail_courses:
                    avail_courses.add(c)

            if not avail_courses:
                print('No available courses to delete (may be because all courses have a class/is a prerequisite of a current course).')
                print('Exiting deletion...')
                break

            print('Press Ctrl + C at any time to exit creation\n')
            print('List of Courses that can be Deleted')
            
            print(design_line('-', 100))
            print(f"{'Course Name':<20}{'Units':<7}")

            for c in avail_courses:
                print(f'{c.course_name:<20}{c.units:<7}')
            print(design_line('-', 100))

            course_name = None
            while True:
                course_name = input('Please input the name of the to be deleted course: ')
                if not course_name:
                    print('Course name cannot be blank, please try again.')
                elif len(course_name) >= 20:
                    print('Course name is too long (>= 20 characters), please try again.')
                elif course_name not in avail_courses:
                    print('Course name not found, please try again.')
                else:
                    del courses[course_name]
                    break
                print(design_line('-', 100))

            print(design_line('-', 100))
            print(f'{course_name} was deleted.')

            exit_del = False
            while True:
                query = input('Would you like to delete more courses? (y/n): ').lower()
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


def main():
    users = {}
    courses = {}
    classes = {}
    prev_enrolments = {}

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
            parsed_class = parse_as_class(cl.strip('\n'))
            if parsed_class is not None:
                classes[f'{parsed_class.course_name} / {parsed_class.classroom}'] = parsed_class

    with open('prev_enrolments.txt') as prev_enrolments_txt:
        for p_enrol in prev_enrolments_txt.readlines():
            parsed_p_enrol = parse_as_prev_enrolments(p_enrol.strip('\n'))
            if parsed_p_enrol is not None:
                prev_enrolments[parsed_p_enrol.student_id] = parsed_p_enrol

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
            num = int(input('Please enter your choice: '))
            print(design_line('=', 100))
            if num == 1:
                create_class(courses, classes)
            elif num == 2:
                remove_class(classes)
            elif num == 3:
                create_course(courses)
            elif num == 4:
                remove_course(courses, classes)
        elif isinstance(login_user, Student):
            print(f'Welcome to your Lozol Account, {login_user.name}')
            print('[1] Enrol in Class')
            print('[2] Drop a Class')
            num = int(input('Please input your choice: '))
            if num == 1:
                enrol_class(login_user, courses, classes, prev_enrolments)
            elif num == 2:
                drop_class(login_user, classes)

    print (design_line('=', 100))
    print ('Exiting...')

    while True:
        save = input('Save changes? (y/n): ').lower()
        if 'y' in save:
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

            with open('prev_enrolments.txt', 'w') as prev_enrolments_txt:
                for i, st in enumerate(prev_enrolments.values()):
                    prev_enrolments_txt.write(st.info())
                    if i != len(prev_enrolments.values()) - 1:
                        prev_enrolments_txt.write('\n')
            break
        elif 'n' in save:
            break

if __name__ == '__main__':
    main()