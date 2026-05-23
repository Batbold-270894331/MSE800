from fish import Goldfish, Shark, Angelfish, Tuna, Salmon


class FishFactory:

    @staticmethod
    def create_fish(fish_type):

        fish_type = fish_type.lower()

        if fish_type == "goldfish":
            return Goldfish()

        elif fish_type == "shark":
            return Shark()

        elif fish_type == "angelfish":
            return Angelfish()

        elif fish_type == "tuna":
            return Tuna()

        elif fish_type == "salmon":
            return Salmon()

        else:
            return None