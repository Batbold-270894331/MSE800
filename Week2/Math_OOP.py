import sys

class Calculator:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def add(self):
        return self.a + self.b

    def subtract(self):
        return self.a - self.b

    def multiply(self):
        return self.a * self.b

    def divide(self):
        if self.b == 0:
            return "Error: Division by zero"
        return self.a / self.b
    

def get_number(prompt):
    while True:
        user_input = input(prompt)

        if user_input.lower() == "q":
            print("Exiting program...")
            sys.exit()

        try:
            return float(user_input)
        except ValueError:
            print("Please enter a valid number or 'q' to exit.")

def choose_operation():
    print("\nChoose an operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("q - exit")
    return input("Enter choice (1-4 or q): ")

def main():
    print("\nChoose an operation [q-exit]:\n")

    a = get_number("Enter first number: ")
    b = get_number("Enter second number: ")

    calc = Calculator(a, b)

    choice = choose_operation()

    if choice == "1":
        print("Result:", calc.add())
    elif choice == "2":
        print("Result:", calc.subtract())
    elif choice == "3":
        print("Result:", calc.multiply())
    elif choice == "4":
        print("Result:", calc.divide())
    elif choice == "q":
        print("Exiting...")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()