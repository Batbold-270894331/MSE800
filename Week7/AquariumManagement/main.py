from fish_factory import FishFactory
from aquarium import Aquarium


def main():

    aquarium = Aquarium()

    print("=== Auckland Aquarium Management System ===")

    while True:

        print("\nEnter fish type")
        print("(Goldfish, Shark, Angelfish, Tuna, Salmon)")
        print("Type 'exit' to finish.")

        user_input = input("Fish Type: ")

        if user_input.lower() == "exit":
            break

        fish = FishFactory.create_fish(user_input)

        if fish:
            aquarium.add_fish(fish)
            print(f"{fish.get_category()} added successfully.")

        else:
            print("Invalid fish type.")

    aquarium.display_inventory()

if __name__ == "__main__":
    main()