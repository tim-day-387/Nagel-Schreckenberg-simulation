# General Imports
import sys, simulation.road, simulation.speedLimits, random, importlib, config
from simulation.car import Car
from representation import Representation
from simulationManager import SimulationManager
from simulation.trafficGenerators import *
from tabulate import tabulate
import numpy as np

# Check for correct number of imports
if len(sys.argv) != 2:
    print("Usage: python3 nagel.py module_with_config")
    exit()

# Grab config from first arguement
config = importlib.import_module(sys.argv[1])

# Set Seed
random.seed(config.seed)

# Grab info from configs and create objects
simulation.car.Car.slowDownProbability = config.slowDownProbability
simulation.car.Car.laneChangeProbability = config.laneChangeProbability
trafficGenerator = TestTrafficGenerator(0)
speedLimits = [simulation.speedLimits.SpeedLimits(config.speedLimits, config.maxSpeed), \
               simulation.speedLimits.SpeedLimits(config.speedLimits, config.maxSpeed), \
               simulation.speedLimits.SpeedLimits(config.speedLimits, config.maxSpeed)]
road = [simulation.road.Road(config.lanes, config.length, speedLimits[0]), \
        simulation.road.Road(config.lanes, config.length, speedLimits[1]), \
        simulation.road.Road(config.lanes, config.length, speedLimits[2])]
simulation = [SimulationManager(road[0], trafficGenerator, config.updateFrame), \
              SimulationManager(road[1], trafficGenerator, config.updateFrame), \
              SimulationManager(road[2], trafficGenerator, config.updateFrame)]

# Start simulation
print("Simulation Started.")

# Simulation parameters
overallAvgSpeed = [0, 0, 0]
sourceCars = 2
initialCars = [sourceCars, 0, 0]
allocated = [sourceCars, 0, 0, 0]
deadCars = [0, 0, 0]
iterations = 500
overallTotalCars = [0, 0, 0]
numSims = len(simulation)

# Iterate all simulations 
for x in range(iterations):
    for y in range(numSims):
        # Decide whether to use initial value
        if iterations == 1:
            trafficGenerator.carPerUpdate = initialCars[y]
        else:
            trafficGenerator.carPerUpdate = allocated[y]

        # Iterate simulation
        simulation[y].makeStep()

        # Update cars leaving roads
        allocated[y + 1] = road[y].deadCars - deadCars[y]
        deadCars[y] = road[y].deadCars

        # Collect stats
        totalCars, avgSpeed = road[y].getAvgCarSpeed()
        overallTotalCars[y] = totalCars + overallTotalCars[y]
        overallAvgSpeed[y] = avgSpeed + overallAvgSpeed[y]

# Table info
headers = ["Road", "Average Speed", "Average Number of Cars"]
data = np.zeros((numSims, 3))

# Populate table
for y in range(numSims):
    data[y][0] = y
    data[y][1] = overallAvgSpeed[y]/iterations
    data[y][2] = overallTotalCars[y]/iterations

# Print final results
print(tabulate(data, headers))
print("Simulation Completed.")
