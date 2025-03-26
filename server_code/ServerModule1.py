import anvil.server

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#


pet = None

class Pet:
    def __init__(self, name):
        self._name = name
        self._hunger = 50
        self._happiness = 50
        self._energy = 50

    def get_status(self):
        return {
            "Type": self.__class__.__name__,
            "Name": self._name,
            "Hunger": self._hunger,
            "Happiness": self._happiness,
            "Energy": self._energy
        }

    def feed(self):
        self._hunger = max(0, self._hunger - 10)
        self._happiness += 5

    def play(self):
        self._happiness += 10
        self._energy -= 10
        self._hunger += 5

    def sleep(self):
        self._energy += 20
        self._hunger += 10

    def tick(self):
        self._hunger = min(100, self._hunger + 2)
        self._energy = max(0, self._energy - 2)
        self._happiness = max(0, self._happiness - 1)

class DogPet(Pet):
    def play(self):
        # Dogs love to play — extra happiness!
        self._happiness += 15
        self._energy -= 15
        self._hunger += 10

class CatPet(Pet):
    def sleep(self):
        # Cats are super chill — extra energy from sleep
        self._energy += 30
        self._hunger += 10

class DragonPet(Pet):
    def feed(self):
        # Dragons have BIG appetites!
        self._hunger = max(0, self._hunger - 20)
        self._happiness += 10


@anvil.server.callable
def create_pet(pet_type, name):
    global pet
    if pet_type == "Dog":
        pet = DogPet(name)
    elif pet_type == "Cat":
        pet = CatPet(name)
    elif pet_type == "Dragon":
        pet = DragonPet(name)
    else:
        pet = Pet(name)
    return pet.get_status()

@anvil.server.callable
def interact_with_pet(action):
    if pet is not None:
        if action == "feed":
            pet.feed()
        elif action == "play":
            pet.play()
        elif action == "sleep":
            pet.sleep()
        return pet.get_status()
    else:
        return None

def tick(self):
    self._hunger = min(100, self._hunger + 2)
    self._energy = max(0, self._energy - 2)
    self._happiness = max(0, self._happiness - 1)

@anvil.server.callable
def pet_tick():
    if pet is not None:
        pet.tick()
        return pet.get_status()
    else:
        return None