# General Imports
import random

# SimpleTrafficGenerator class
class SimpleTrafficGenerator():
    # Constructor
    def __init__(self, carPerUpdate=1):
        self.queue = 0
        self.carPerUpdate = carPerUpdate

    # Determine how to generate traffic
    def generate(self, road):
        amount = random.randint(0, self.carPerUpdate)
        self.tryGenerate(road, amount)

    # Queue cars to generate
    def tryGenerate(self, road, amount):
        added = road.pushCarsRandomly(amount + self.queue)
        self.queue += (amount - added)

# TestTrafficGenerator class
class TestTrafficGenerator():
    # Constructor
    def __init__(self, carPerUpdate=1):
        self.queue = 0
        self.carPerUpdate = carPerUpdate

    # Determine how to generate traffic
    def generate(self, road):
        amount = self.carPerUpdate
        self.tryGenerate(road, amount)

    # Queue cars to generate
    def tryGenerate(self, road, amount):
        added = road.pushCarsRandomly(amount + self.queue)
        self.queue += (amount - added)

