# General Imports
import sys, simulation.road, simulation.speedLimits, random, importlib, config
from simulation.car import Car
from simulationManager import SimulationManager
from simulation.trafficGenerators import *
from tabulate import tabulate
from simulation.intersection import intersection
import numpy as np

# Check for correct number of imports
if len(sys.argv) != 2:
    print("Usage: python3 nagel.py module_with_config")
    exit()

# Grab config from first arguement
config = importlib.import_module(sys.argv[1])

# Set Seed
random.seed(config.seed)

# Create intersections list
def createInters(numOfRoads, vertices):
    output = []

    for i in range(numOfRoads):
        output.append(intersection(vertices[i][0], vertices[i][1]))

    return output

# Create speedLimts list
def createSpeedLimits(numOfRoads):
    output = []

    for i in range(numOfRoads):
        output.append(simulation.speedLimits.SpeedLimits(config.speedLimits, config.maxSpeed))

    return output

# Create roads list
def createRoads(numOfRoads):
    output = []

    for i in range(numOfRoads):
        output.append(simulation.road.Road(config.lanes, config.length, speedLimits[i]))

    return output

# Create simulations list
def createSims(numOfRoads):
    output = []

    for i in range(numOfRoads):
        output.append(SimulationManager(road[i], trafficGenerator, config.updateFrame))

    return output

# Main Simulation, Tables
def main(numSims):
    # Define allocated
    allocated = [0] * (numSims + 1)
    
    # Run each iteration 
    for x in range(iterations):
        # Run each simulation
        for y in range(numSims):
            # Decide whether to use initial value
            if x == 0:
                trafficGenerator.carPerUpdate = initialCars[y]
            else:
                trafficGenerator.carPerUpdate = allocated[y]

            # Iterate simulation
            simulation[y].makeStep()

        # Reset allocated
        allocated = [0] * (numSims + 1)

        # Collect Stats on each simulation
        for y in range(numSims):
            # Update cars leaving roads
            for i in intersections:
                allocated = i.applyRule(allocated, simulation, road, deadCars)
            
            # Account for new deadCars
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

# Simulation parameters
numRoads = 8
overallAvgSpeed = [0] * numRoads
initialCars = [0] * numRoads
allocated = [0] * (numRoads + 1)
deadCars = [0] * numRoads
iterations = 5000
initialCars[0] = 20
overallTotalCars = [0] * numRoads
vertices = [[7, [1, 2, 0]], \
            [1, [3, 4]], \
            [2, [5, 6]], \
            [3, [7]], \
            [4, [7]], \
            [5, [7]], \
            [6, [7]], \
            [0, [7]]]


# Set some simulation parameters
simulation.car.Car.slowDownProbability = config.slowDownProbability
simulation.car.Car.laneChangeProbability = config.laneChangeProbability

# Generate different objects
trafficGenerator = TestTrafficGenerator(0)
speedLimits = createSpeedLimits(numRoads)
road = createRoads(numRoads)
simulation = createSims(numRoads)
intersections = createInters(numRoads, vertices)

# Run the Program
main(numRoads)
