class Product:
    def __init__(self, identity, color, type, material, new_price, old_price):
        self.identity = identity
        self.color = color
        self.type = type
        self.material = material
        self.new_price = new_price
        self.old_price = old_price

    def print_information(self):
        print(f"Color: {self.color}\n" +
              f"Type: {self.type}\n" +
              f"Material: {self.material}\n" +
              f"New Price: {self.new_price}\n" +
              f"Old Price: {self.old_price}\n")