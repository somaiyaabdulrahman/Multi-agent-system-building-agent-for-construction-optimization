import random

class ConstructionMaterialAgent:
    def __init__(self):
        self.inventory = {"door": 100, "outside-door": 20, "window": 200, "wall-module": 50, "toilet-seat": 100, "tab": 50, "shower-cabin": 30}
        self.prices = {"door": 2500, "outside-door": 8500, "window": 3450, "wall-module": 75000, "toilet-seat": 2995, "tab": 2350, "shower-cabin": 8300}

    def sell(self, item, quantity):
        if item in self.inventory and self.inventory[item] >= quantity:
            self.inventory[item] -= quantity
            return self.prices[item] * quantity
        else:
            return 0

class BuilderAgent:
    def __init__(self):
        self.money = 0
        self.houses = []
        self.building_materials = {"door": 0, "outside-door": 0, "window": 0, "wall-module": 0, "toilet-seat": 0, "tab": 0, "shower-cabin": 0}
        self.building_progress = []

    def build(self):
        # Check if we can build two houses at the same time
        if len(self.building_progress) >= 2:
            return

        # Check if we have enough materials to build a house
        if not self.can_build_house():
            return

        # Start building a new house
        house = {"floor": {}, "garret": {}}
        floor = self.build_floor()
        garret = self.build_garret()
        house["floor"] = floor
        house["garret"] = garret
        self.houses.append(house)
        self.building_progress.append(house)

    def build_floor(self):
        floor = {"bedroom": [], "bathroom": [], "living-room": [], "hall": []}
        # Build the bedroom
        for i in range(4):
            bedroom = self.build_bedroom()
            floor["bedroom"].append(bedroom)
        
        # Build the bathroom
        for i in range(2):
            bathroom = self.build_bathroom()
            floor["bathroom"].append(bathroom)

        # Build the living room
        living_room = self.build_living_room()
        floor["living-room"].append(living_room)
        
        # Build the hall
        hall = self.build_hall()
        floor["hall"].append(hall)
        return floor

    def build_bedroom(self):
        bedroom = {"door": 1, "window": 2, "wall-module": 4}
        self.consume_materials(bedroom)
        return bedroom

    def build_bathroom(self):
        bathroom = {"door": 1, "window": 1, "wall-module": 4, "toilet-seat": 1, "tab": 1, "shower-cabin": 1}
        self.consume_materials(bathroom)
        return bathroom

    def build_living_room(self):
        living_room = {"door": 1, "window": 3, "wall-module": 4}
        self.consume_materials(living_room)
        return living_room

    def build_hall(self):
        hall = {"outside-door": 1, "window": 1, "wall-module": 2}
        self.consume_materials
