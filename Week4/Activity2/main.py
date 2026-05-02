from land import Land

def get_user_input():
    try:
        length = float(input("Length of the land: "))
        width = float(input("Width of the land: "))

        if length <= 0 or width <= 0:
            print("Dimensions must be positive numbers.")
            return None

        return length, width

    except ValueError:
        print("Invalid inputs. Please enter numeric values.")
        return None


def main():
    print("=== Land Area & Perimeter Calculator ===\n")

    user_input = get_user_input()

    if user_input:
        length, width = user_input

        land = Land(length, width)

        
        print(f"Area: {land.calculate_area()}")
        print(f"Perimeter: {land.calculate_perimeter()}")
        print("")


if __name__ == "__main__":
    main()