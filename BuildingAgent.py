
import random

class ConstructionMaterialAgent:
    def __init__(self, inventory_limit=100, price_table= {
        'door': 2500,
        'window': 3450,
        'wall_module': 75000,
        'toilet_seat': 2995,
        'tab': 2350,
        'shower_cabin': 8300 }):

        self.inventory_limit = inventory_limit
        self.inventory = {c: 0 for c in price_table}
        self.price_table = price_table

    def sell_materials(self, component, quantity, buyer):
        if self.inventory[component] == 0:
            return False
        if self.inventory[component] < quantity:
            quantity = self.inventory[component]
        self.inventory[component] -= quantity
        buyer.money -= quantity * self.price_table[component]
        return True

    def restock_inventory(self):
        for component in self.inventory:
            restock_amount = random.randint(0, self.inventory_limit - self.inventory[component])
            self.inventory[component] += restock_amount

    def choose_buyer(self, buyers):
        return random.choice(buyers)


class BuilderAgent:
    def __init__(self, material_agent, money=2000000, pid=None):
        self.crossover_rate = 0.6
        self.mutation_rate = 0.03
        self.material_agent = material_agent
        self.money = money
        self.inventory = {c: 0 for c in material_agent.price_table}
        self.houses_built = 0
        self.pid = pid
        self.num_houses_building = 0


    def build_house(self):
        if not self.build_floor():
            return False
        if self.build_ceiling():
            self.houses_built += 1
            self.money += 1000000
            return True
        return False


    def build_floor(self):
        needed_materials = {
            'door': 2,
            'window': 10,
            'wall_module': 5,
            'toilet_seat': 1,
            'tab': 1,
            'shower_cabin': 1
        }
        return self.purchase_materials(needed_materials)


    def build_ceiling(self):
        needed_materials = {
            'door': 1,
            'window': 3,
            'wall_module': 1
        }
        return self.purchase_materials(needed_materials)


    def purchase_materials(self, needed_materials):
        buyers = [self]
        for component, quantity in needed_materials.items():
            success = False
            attempts = 0
            while not success and attempts < 3:
                success = self.material_agent.sell_materials(
                    component, quantity, self.material_agent.choose_buyer(buyers))
                attempts += 1
            if not success:
                return False
        return True

    def swap_materials(self, other, component, quantity):
        if (self.inventory[component] >= quantity and
            other.inventory[component] >= quantity):
            self.inventory[component] -= quantity
            other.inventory[component] -= quantity
            self.inventory[component] += quantity
            other.inventory[component] += quantity
            return True
        return False

builders = []

def run_simulation(num_agents, num_years, inventory_limit, restock_interval):
    global most_houses

    material_agent = ConstructionMaterialAgent(inventory_limit=inventory_limit)
    for num in range(num_agents):
        builders.append(BuilderAgent(material_agent, pid=num+1))
    random.shuffle(builders)

    for year in range(num_years * 12):  # 12 months per year
        if year % restock_interval == 0:
            material_agent.restock_inventory()

            for builder in builders:
              builder.build_house()
          # Swap materials with 60% chance
            if random.random() < builder.crossover_rate:
                other_builder = random.choice(builders)
                while other_builder == builder:
                    other_builder = random.choice(builders)
                builder.swap_materials(other_builder,
                                       random.choice(list(builder.inventory)),
                                       random.randint(1, 3))
            # Mutate inventory with some probability
            if random.random() < builder.mutation_rate:
                component = random.choice(list(builder.inventory))
                builder.inventory[component] = random.randint(0, 5)
        most_houses = max(b.houses_built for b in builders)
        winners = [b for b in builders if b.houses_built == most_houses]
        if len(winners) > 1:
            winner = max(winners, key=lambda b: b.money)
        else:
            winner = random.choice(winners)

    return f'The best builder is Builder {winner.pid} with {most_houses} houses built and {winner.money} SEK!'

result = run_simulation(num_agents=4, num_years=5, inventory_limit=100, restock_interval=3)

def print_houses():
    houses_per_row = 11
    num_rows = (most_houses // houses_per_row) + (most_houses % houses_per_row > 0)
    for row in range(num_rows):
        for i in range(houses_per_row):
            house_num = row * houses_per_row + i + 1
            if house_num > most_houses:
                break
            print("   /¯¯¯¯¯\   ", end="")
        print()
        for i in range(houses_per_row):
            house_num = row * houses_per_row + i + 1
            if house_num > most_houses:
                break
            print("  /_______\  ", end="")
        print()
        for i in range(houses_per_row):
            house_num = row * houses_per_row + i + 1
            if house_num > most_houses:
                break
            print("  | [] [] |  ", end="")
        print()
        for i in range(houses_per_row):
            house_num = row * houses_per_row + i + 1
            if house_num > most_houses:
                break
            print("  |       |  ", end="")
        print()
        for i in range(houses_per_row):
            house_num = row * houses_per_row + i + 1
            if house_num > most_houses:
                break
            print("  |__|¯|__|  ", end="")
        print()


print('*' * 140)

print_houses()

builder_emoji = "\U0001F477"

print('-' * 140 , '\n', '\n', (builder_emoji + result).center(140), '\n', '\n' + '*' * 140)
