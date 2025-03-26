import anvil.server

# --- Pet Classes ---

class Pet:
    def __init__(self, name, hunger=50, happiness=50, energy=50):
        self._name = name
        self._hunger = hunger
        self._happiness = happiness
        self._energy = energy

    def get_status(self):
        return {
            "Name": self._name,
            "Type": self.__class__.__name__,
            "Hunger": self._hunger,
            "Happiness": self._happiness,
            "Energy": self._energy
        }

    def to_dict(self):
        return {
            "name": self._name,
            "hunger": self._hunger,
            "happiness": self._happiness,
            "energy": self._energy,
            "type": self.__class__.__name__
        }

    @staticmethod
    def from_dict(data):
        cls = {"DogPet": DogPet, "CatPet": CatPet, "DragonPet": DragonPet}.get(data["type"], Pet)
        return cls(
            name=data["name"],
            hunger=data["hunger"],
            happiness=data["happiness"],
            energy=data["energy"]
        )
  
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

# --- Subclasses ---

class DogPet(Pet):
    def play(self):
        self._happiness += 15
        self._energy -= 15
        self._hunger += 10

class CatPet(Pet):
    def sleep(self):
        self._energy += 30
        self._hunger += 10

class DragonPet(Pet):
    def feed(self):
        self._hunger = max(0, self._hunger - 20)
        self._happiness += 10

# --- Server Functions ---

@anvil.server.callable
def create_pet(pet_type, name):
    if pet_type == "Dog":
        pet = DogPet(name)
    elif pet_type == "Cat":
        pet = CatPet(name)
    elif pet_type == "Dragon":
        pet = DragonPet(name)
    else:
        pet = Pet(name)

    anvil.server.session['pet'] = pet.to_dict()
    return pet.get_status()

@anvil.server.callable
def get_pet_status():
    pet_data = anvil.server.session.get('pet', None)
    if pet_data:
      pet = Pet.from_dict(pet_data)
      anvil.server.session["pet"] = pet.to_dict()  # <== THIS LINE IS CRUCIAL
      return pet.get_status()
    else:
      return None

@anvil.server.callable
def interact_with_pet(action):
    pet_data = anvil.server.session.get('pet', None)
    if pet_data:
      pet = Pet.from_dict(pet_data)   
      if action == "feed":
          pet.feed()
      elif action == "play":
          pet.play()
      elif action == "sleep":
          pet.sleep()
      anvil.server.session["pet"] = pet.to_dict()  # <== THIS LINE IS CRUCIAL
      return pet.get_status()
    else:
        return None

@anvil.server.callable
def pet_tick():
    pet_data = anvil.server.session.get('pet', None)
    if pet_data:
      pet = Pet.from_dict(pet_data)
      pet.tick()
      anvil.server.session["pet"] = pet.to_dict()  # <== THIS LINE IS CRUCIAL
      return pet.get_status()
    else:
        return None