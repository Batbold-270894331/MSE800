# Factory Design Pattern Explanation

## How the pattern is used

The code uses the **Factory Design Pattern** to create animal objects.

```python
class Factory(ABC):
    @abstractmethod
    def create_product(self, kind=None):
        pass
```

`Factory` is an abstract parent class. It defines the method `create_product()` for its subclasses.

```python
class AnimalFactory(Factory):
    def create_product(self, kind=None):
        if kind == "dog":
            animal = Dog()
        elif kind == "cat":
            animal = Cat()
        return animal
```

`AnimalFactory` creates a `Dog` object when `kind` is `"dog"` and a `Cat` object when `kind` is `"cat"`.

## Classes and subclasses

The code has two inheritance groups:

- `AnimalFactory`, `DogFactory`, and `CatFactory` are subclasses of `Factory`.
- `Dog` and `Cat` are subclasses of `Animals`.

```python
class Animals(ABC):
    @abstractmethod
    def run(self):
        pass
```

`Animals` defines the common `run()` method. `Dog` and `Cat` implement this method with their own output.

## Outcome of the code

The client code uses:

```python
factory = DogFactory()
dog = factory.create_product()
dog.run()
```

Then the output will be:

```text
I'm a Dog, I can run!!
```
