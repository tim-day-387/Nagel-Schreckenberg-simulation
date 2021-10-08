# General Imports
import random

# intersection class
class intersection:
    # Constructor
    def __init__(self, origin, destinations):
        self.origin = origin
        self.destinations = destinations

    # Update the simulation
    def applyRule(self, nodes, simulations, roads, deadCars):
        index = random.randint(0, len(self.destinations)-1)

        nodes[self.destinations[index]] = nodes[self.destinations[index]] + roads[self.origin].deadCars - deadCars[self.origin]

        return nodes
