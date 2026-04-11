try:
    x = int(input("Enter x: "))
    y = int(input("Enter y: "))

    print("Result: ", x ** y)
    
except ValueError:
    print("Please enter numbers only!")