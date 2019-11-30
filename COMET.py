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
    
    def __str__(self):
        return 'Admin: {}'.format(self.username)
        
class Student(User):
    def __init__(self, id_number, password, name, unit_limit):
        super().__init__(id_number, password)
        self.name = name
        self.unit_limit = unit_limit
    
    def __str__(self):
        return 'Student: {}({}) [{}] - {}'.format(self.username, self.id_number, self.name, self.unit_limit)

class Class:
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
    
    def remove_prereq(self, index):
        del self.prereqs[index]
    
    def __str__(self):
        str = '[ {}: {} - [ '.format(self.name, self.units)
        for c in self.prereqs:
            str += '{} '.format(c.name)
        str += ']]'
        return str

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

def main():
    
    classes = []
    users = []
    users.append(Admin('admin', 'admin'))

    with open('users.txt').readlines() as users_txt: #TODO(Mscizor) Read user and class data from text
        for user in users_txt:
            pass

    with open('classes.txt').readlines() as classes_txt:
        for cl in classes_txt:
            pass

    exit_login = False
    while not exit_login:
        design_line('=', 100)
        username = input('Lozol Account Name: ')
        password = input('Lozol Account Password: ')
        design_line('=', 100)

        found = False
        for user in users:
            if user.username == username and user.password == password:
                found = True
                break

        if not found:
            print('Invalid login details.')
            query = input('Exit program? (yes or no)').lower().split()
            for s in query:
                if s == 'yes': exit_login = True
        else:
            print('Login found. Proceeding to log-in page.')
            break
    
    if not exit_login:
        pass #TODO(Mscizor) Log-in page for admin and student

    with open('users.txt', 'w') as users_txt: #TODO(Mscizor) Write user and class data to text
        for user in users:
            if isinstance(user, Admin):
                pass
            elif isinstance (user, Student):
                pass

    with open('classes.txt', 'w') as classes_txt:
        for cl in classes:
            pass

if __name__ == '__main__':
    main()