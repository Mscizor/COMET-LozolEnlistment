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
        return f'Admin - {self.username} - {self.password}'

    def __str__(self):
        return f'Admin: {self.username} - {self.password}'
        
class Student(User):
    def __init__(self, id_number, password, name, unit_limit):
        super().__init__(id_number, password)
        self.name = name
        self.unit_limit = int(unit_limit)
    
    def info(self):
        return f'Student - {self.username} - {self.password} - {self.name} - {self.unit_limit}'

    def __str__(self):
        return f'Student - {self.username} - {self.password} - {self.name} - {self.unit_limit}'

class Class:
    # Prereqs as a str for each, to be processed later
    def __init__(self, name, classroom, units, prereqs):
        self.name = name
        self.classroom = classroom
        self.units = units
        self.prereqs = prereqs
        
    def set_name(self, new_name):
        self.name = new_name
        
    def set_classroom(self, new_classroom):
        self.classroom = new_classroom

    def set_units(self, new_units):
        self.units = new_units
            
    def add_prereq(self, new_prereq):
        self.prereqs.append(new_prereq)
    
    def remove_prereq(self, prereq):
        self.prereqs.remove(prereq)
    
    def info(self):
        info = [f'{self.name} / {self.classroom} - {self.units} - ']
        for cl in self.prereqs:
            info.append (f'{cl} ')
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
    read = user.split(' - ')
    if read[0] == 'Student':
        if len(read) < 5:
            return None
        else:
            return Student(read[1], read[2], read[3], read[4])
    else:
        if len(read) < 3:
            return None
        else:
            return Admin(read[1], read[2])

def parse_as_class(cl):
    '''Takes a string representing class info and creates a class with that information.

    Parses a string and gets the relevant information such as the class name and units,
    and returns an instance of a Class.

    Args:
        cl: String representation of the class

    Returns:
        Either a Student or an Admin with the relevant information given in the string.
    '''
    read = cl.split(' - ')
    if len(read) < 3:
        return None
    else:
        prereqs = read[2].split(' ')
        class_details = read[0].split(' / ')
        return Class(class_details[0], class_details[1], read[1], prereqs)

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

def enrol_class(student, classes):
    pass

def drop_class(student, classes):
    pass

def create_class(classes):
    '''Asks admin for inputs to create a number of new classes.

    Asks the admin for details which include name of classes, classroom number, number of units, 
    and prerequisites to create any number of new classes.

    Args:
        classes: The already existing list of classes
    '''

    while True:
        print('List of Classes')
        for cl in classes.values():
            print(f'{cl.name} in Room {cl.classroom} with units {cl.units}')

        class_name = None
        classroom = None
        while True:
            class_name = input('Please input the name of the new class: ')
            classroom = input("Please input where it's going to be held: ")
            if f'{class_name} / {classroom}' in classes:
                print('Class with same name and classroom already found, please try again.')
            else:
                break
        
        units = None
        while True:
            units = int(input('Please input how many units the class will be worth: '))
            if units < 0:
                print('Units cannot be less than 0, please try again.')
            else:
                break
        
        prereqs = None
        found_class = None
        while True:
            prereqs = input('Please input what prereqs the class will or will not have (separated by spaces): ').split()
            for prereq in prereqs:
                if prereq not in [cl.name for cl in classes.values()]:
                    found_class = prereq
                    break
            else:
                break
            
            print(f'Specified class ({found_class}) was not in already existing list of classes. Please try again.')

        if prereqs is None:
            prereqs = 'None'
        
        new_class = Class(class_name, classroom, units, prereqs)
        classes[f'{new_class.name} / {new_class.classroom}'] = new_class
        print(f'{new_class.name} in room {new_class.classroom} with units {new_class.units} was added.')

        while True:
            query = input('Would you like to add more classes? (y/n): ').lower()
            exit_add = False
            if 'n' in query:
                exit_add = True
                break
            elif 'y' in query:
                break
        
        if exit_add:
            break
        
def remove_class(classes):
    pass

def edit_student(edited_user, is_admin = False):
    pass

def main():
    classes = {}
    users = {}
    users['test'] = Admin ('test', 'test')

    with open('users.txt') as users_txt:
        for user in users_txt.readlines():
            parsed_user = parse_as_user(user.strip())
            if parsed_user is not None:
                users[parsed_user.username] = parsed_user
            
    with open('classes.txt')as classes_txt:
        for cl in classes_txt.readlines():
            parsed_class = parse_as_class(cl.strip())
            if parsed_class is not None:
                classes[f'{parsed_class.name} / {parsed_class.classroom}'] = parsed_class

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
            while (True):
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
            print('[3] Edit Student Information')
            num = input('Please enter your choice: ')
            choices = {1 : create_class(classes), 2 : remove_class(classes)}
            if num == 1 or num == 2:
                choices[num]
            else:
                pass
                # print(design_line('=', 100))
                # students = {i : student for i, student in users if isinstance(student, Student)}
                # for student in enumerate(students):
                #     print(f'[{i + 1}] {student.name}')
                # num = input('Please enter the full name of the student to be edited: ')
        elif isinstance(login_user, Student):
            print (f'Welcome to your Lozol Account, {login_user.name}')
            print ('[1] Enrol in Class')
            print ('[2] Drop a Class')
            print ('[3] Edit your Information')
            num = int(input('Please input your choice: '))
            choices = {1 : enrol_class, 2 : drop_class, 3 : edit_student(login_user)} #TODO(Mscizor) : Finish defined functions here

    print (design_line('=', 100))
    print ('Exiting...')

    with open('users.txt', 'w') as users_txt:
        for i, user in enumerate(users.values()):
            users_txt.write(user.info())
            if i != len(users.values()) - 1:
                users_txt.write('\n')

    with open('classes.txt', 'w') as classes_txt:
        for i, cl in enumerate(classes.values()):
            classes_txt.write(cl.info())
            if i != len(classes.values()) - 1:
                classes_txt.write('\n')

if __name__ == '__main__':
    main()