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
    def __init__(self, name, units, prereqs):
        self.name = name
        self.units = units
        self.prereqs = prereqs
        
    def set_name(self, new_name):
        self.name = new_name
        
    def set_units(self, new_units):
        self.units = new_units
            
    def add_prereq(self, new_prereq):
        self.prereqs.append(new_prereq)
    
    def remove_prereq(self, prereq):
        self.prereqs.remove(prereq)
    
    def info(self):
        info = [f'{self.name} - {self.units} - ']
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
        return Class(read[0], read[1], prereqs)

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

        Returns nothing if num is less than 0.
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

def create_class(admin, classes):
    pass

def remove_class(admin, classes):
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
                classes[parsed_class.name] = parsed_class

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
            print (f'Welcome to your administrator dashboard, {login_user.username}')
            print ('[1] Create Class')
            print ('[2] Remove Class')
            print ('[3] Edit Student Information')
            num = input ('Please enter your choice: ')
            choices = {1 : create_class, 2 : remove_class, 3 : edit_student(None, True)} #TODO(Mscizor) : Finish defined functions here
        elif isinstance(login_user, Student):
            print (f'Welcome to your Lozol Account, {login_user.name}')
            print ('[1] Enrol in Class')
            print ('[2] Drop a Class')
            print ('[3] Edit your Information')
            num = int(input('Please input your choice: '))
            choices = {1 : enrol_class, 2 : remove_class, 3 : edit_student(login_user)} #TODO(Mscizor) : Finish defined functions here

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