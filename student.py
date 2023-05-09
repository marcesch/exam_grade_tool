"""
keep things organized, keeps track of the student class

"""


class Student:
    def __init__(self, firstname: str, lastname: str):
        self.firstname = firstname
        self.lastname = lastname

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    def __repr__(self):
        return f"{self.firstname} {self.lastname}"

    def __eq__(self, other):
        if other == None:
            return False
        if type(other) != Student:
            raise RuntimeError(f"Cannot compare students to other object of type {type(other)}")
        return other.firstname == self.firstname and other.lastname == self.lastname

    def __hash__(self):
        return hash(''.join([self.firstname, self.lastname]))

    def change_name(self, new_first: str, new_last: str):
        """
        :return:
        """
        self.firstname = new_first
        self.lastname = new_last

# TODO what other reasonable functions are there for students?