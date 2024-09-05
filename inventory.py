class Item:
    def __init__(self, name, description, type, effect = None):
        self.name = name
        self.description = description
        self.type = type
        self.effect = effect
    def use(self, target):
            """Use the item on the target (e.g., player or monster)."""
            if self.effect:
                self.effect(target)
            else:
                print(f"{self.name} has no effect.")


class Inventory:
    def __init__(self, capacity = 10) -> None:
        self.capacity = capacity
        self.items = []


    def add_item(self, item):
        if len(self.items) < self.capacity:
            self.items.append(item)
            print(f"Added {item.name} to inventory.")
        else:
            print("Inventory is full!")

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"Removed {item.name} from inventory.")
        else:
            print(f"{item.name} is not in the inventory.")

    def list_items(self):
        if self.items:
            print("Inventory:")
            for item in self.items:
                print(f"- {item.name}: {item.description}")
        else:
            print("Inventory is empty.")