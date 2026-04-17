import math

def Basic_calculator(a, b, operator):
    if operator == '+':
        return a + b
    elif operator == '-':
        return a - b
    elif operator == '*':
        return a * b
    elif operator == '/':
        if b == 0:
            return "Error: Division by zero"
        return a / b
    elif operator == '%':
        return a % b
    else:
        return "Invalid operator"
    
def factorial(n):
    if n < 0:
        return "Error: Not allow negative number"
    
    return math.factorial(n)

def main():
    print("Simple Calculator")
    try:
        operator = input("Enter operator (+, -, *, /, %, F for factorial): ")

        if operator == 'F':
            a = float(input("Enter number for factorial: "))
            result = factorial(int(a))
        else:
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
            result = Basic_calculator(a, b, operator)

        print("Result: ", result)
    
    except ValueError:
        print("Please enter valid numbers!")

main()