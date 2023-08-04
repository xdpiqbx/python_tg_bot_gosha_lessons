import hashlib

class UserDTO:
    def __init__(self):
        self.__name = None
        self.__password = None

    def set_name(self, name):
        self.__name = name

    def set_pass(self, password):
        self.__password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    def get_name(self):
        return self.__name

    def get_pass(self):
        return self.__password

    def clear(self):
        self.__name = None
        self.__password = None

    def __str__(self):
        return str((self.__name, self.__password))

