from abc import ABC, abstractmethod


# Abstract Fish Class
class Fish(ABC):

    @abstractmethod
    def get_category(self):
        pass


# Fish Types
class Goldfish(Fish):

    def get_category(self):
        return "Goldfish"


class Shark(Fish):

    def get_category(self):
        return "Shark"


class Angelfish(Fish):

    def get_category(self):
        return "Angelfish"


class Tuna(Fish):

    def get_category(self):
        return "Tuna"


class Salmon(Fish):

    def get_category(self):
        return "Salmon"