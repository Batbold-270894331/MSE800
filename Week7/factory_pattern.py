from abc import ABC, abstractmethod

# Factory Pattern: an interface for creating objects in a super class, but allows subclasses to alter the type of objects that will be created.
class Factory(ABC):
    
    # abstract method to create product
    @abstractmethod
    def create_product(self, kind=None):
        pass

# Concrete Factory: a factory that creates animals
# class AnimalFactory(Factory):
#     def __init__(self):
#         pass

#     # concrete method to create product
#     def create_product(self, kind=None):
#         if kind == "dog":
#             animal = Dog()
#         elif kind == "cat":
#             animal = Cat()

#         return animal

# Concrete Factory: a factory that creates dogs
class DogFactory(Factory):
    
    # concrete method to create product
    def create_product(self, kind=None):
        return Dog()

# Concrete Factory: a factory that creates cats
class CatFactory(Factory):
    
    def create_product(self, kind=None):
        return Cat()

# Product: an interface for objects that the factory method creates
class Animals(ABC):

    @abstractmethod
    def run(self):
        pass

# Concrete Product: a class that implements the product interface for dogs
class Dog(Animals):

    # concrete method to run
    def run(self):
        print(f"I'm a Dog, I can run!!")

# Concrete Product: a class that implements the product interface for cats
class Cat(Animals):
    def __init__(self):
        pass

    # concrete method to run
    def run(self):
        print(f"I'm a Cat, I can run!!")




# client
factory = DogFactory()
#dog = Dog()
dog = factory.create_product()

dog.run()