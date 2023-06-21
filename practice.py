# Try/Except
# try:
#    x = 5+4
# except:
#    print("Failed")

# oop.
# An object has state and behaviours
# States = properties/attributes that define an object - color, height, name
# Behaviour = What does the object do - functionalities
# Examples are like move(), eat(), etc
# In programming states - properties & behaviours are functions/methods
class Fish():
    # Constractor of properties
    def __init__(self):
        self.name = "Bob"
        self.age = "4"
        self.color = "Silver"
        self.weight = 3

# A fnction inside a class is called a method
    def swim(self, lake): # parameter
        message = (self.name, "can swim.", lake)
        return message

    def jump(self):
        message = self.name, "can jump."
        return message


# Call the object/instantiate
fish = Fish()
print(fish.age)
print(fish.swim(L.Nakuru))
# prefer
message = fish.swim("L.Nakuru") # argument 
print(type(fish))
print(message)
