class Aquarium:

    # Singleton instance
    __instance = None

    def __new__(cls):

        if cls.__instance is None:
            cls.__instance = super(Aquarium, cls).__new__(cls)

            # Initialize inventory once
            cls.__instance.fish_inventory = {}

        return cls.__instance

    # Add fish to aquarium
    def add_fish(self, fish):

        category = fish.get_category()

        if category in self.fish_inventory:
            self.fish_inventory[category] += 1
        else:
            self.fish_inventory[category] = 1

    # Display inventory
    def display_inventory(self):

        print("\nAquarium Inventory:")

        for category, count in self.fish_inventory.items():
            print(f"Fish Category: {category} | Count: {count}")