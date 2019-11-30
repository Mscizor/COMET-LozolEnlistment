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
                    Classroom Number (String)
                    Name of Class (String)
                    Number of Units (Integer)
                    Classes as Prerequisites ([Class])

                Remove Class
            
            Student --
                Take Class
                Drop Class
"""

class User (object):
    def __init__ (self, username, password):
        self.username = username
        self.password = password
    
class Admin (User):
    def __init__ (self, username, password):
        super ().__init__ (username, password)
    
    def __str__ (self):
        return 'Admin: {}'.format (self.username)
        
class Student (User):
    def __init__ (self, id_number, password, name, unit_limit):
        super ().__init__ (id_number, password)
        self.name = name
        self.unit_limit = unit_limit
    
    def __str__ (self):
        return 'Student: {} ({}) [{}] - {}'.format (self.username, self.id_number, self.name, self.unit_limit)

class Class:
    def __init__ (self, name, units, prereqs):
        self.name = name
        self.units = units
        self.prereqs = prereqs
        
    def set_name (self, new_name):
        self.name = new_name
        
    def set_units (self, new_units):
        self.units = new_units
            
    def add_prereq (self, new_prereq):
        self.prereqs.append (new_prereq)
    
    def remove_prereq (self, index):
        del self.prereqs[index]
    
    def __str__ (self):
        str = '[ {}: {} - [ '.format (self.name, self.units)
        for c in self.prereqs:
            str += '{} '.format (c.name)
        str += ']]'
        return str

def design_bar (char, num, end = '\n'):
    str = ""
    for _ in range(num):
        str += char
    print (str, end = end)

classes = []
users = []
users.append (Admin ('admin', 'admin'))

design_bar ('=', 100)
username = input ('Lozol Account Name: ')
password = input ('Lozol Account Password: ')
design_bar ('=', 100)

found = False
for user in users:
    if user.username == username and user.password == password:
        found = True
        break

if not found:
    print ('Invalid login details.')
else:
    print ('Login found. Proceeding to log-in page.')