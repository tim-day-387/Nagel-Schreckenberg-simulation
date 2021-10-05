# General Imports
import sys, simulation.road, simulation.speedLimits, random, importlib, config
from simulation.car import Car
from representation import Representation
from simulationManager import SimulationManager
from simulation.trafficGenerators import *

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
speedLimits1 = simulation.speedLimits.SpeedLimits(config.speedLimits, config.maxSpeed)
speedLimits2 = simulation.speedLimits.SpeedLimits(config.speedLimits, config.maxSpeed + 100)
road1 = simulation.road.Road(config.lanes, config.length, speedLimits1)
simulation1 = SimulationManager(road1, config.trafficGenerator, config.updateFrame)
road2 = simulation.road.Road(config.lanes, config.length, speedLimits2)
simulation2 = SimulationManager(road2, config.trafficGenerator, config.updateFrame)

# Perform simulation
print("Simulation Started.")

overallAvgSpeed = [0, 0]
iterations = 500

for x in range(iterations):
    simulation1.makeStep()
    totalCars, avgSpeed = road1.getAvgCarSpeed()
    overallAvgSpeed[0] = avgSpeed + overallAvgSpeed[0]
    simulation2.makeStep()
    totalCars, avgSpeed = road2.getAvgCarSpeed()
    overallAvgSpeed[1] = avgSpeed + overallAvgSpeed[1]


print("First: ", overallAvgSpeed[0]/iterations)
print("Second: ", overallAvgSpeed[1]/iterations)

print("Simulation Completed.")
