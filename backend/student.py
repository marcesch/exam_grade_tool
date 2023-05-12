"""
keep things organized, keeps track of the student class

"""


class Student:
    def __init__(self, firstname: str, lastname: str):
        self.firstname = firstname.lower()
        self.lastname = lastname.lower()

    def __str__(self):
        return f"{self.firstname.capitalize()} {self.lastname.capitalize()}"

    def __repr__(self):
        return f"{self.firstname.capitalize()} {self.lastname.capitalize()}"

    def __eq__(self, other):
        if other == None:
            return False
        if type(other) != Student:
            raise RuntimeError(f"Cannot compare students to other object of type {type(other)}")
        return other.firstname.lower() == self.firstname.lower() and other.lastname.lower() == self.lastname.lower()

    def __hash__(self):
        return hash(''.join([self.firstname.lower(), self.lastname.lower()]))

    def change_name(self, new_first: str, new_last: str):
        """
        :return:
        """
        self.firstname = new_first
        self.lastname = new_last

# TODO what other reasonable functions are there for students?