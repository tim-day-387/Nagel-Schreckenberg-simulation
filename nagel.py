# General Imports
import sys, pygame, simulation.road, simulation.speedLimits, random, importlib, config
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
pygame.init()
screen = pygame.display.set_mode(config.size)
clock = pygame.time.Clock()
simulation.car.Car.slowDownProbability = config.slowDownProbability
simulation.car.Car.laneChangeProbability = config.laneChangeProbability
speedLimits = simulation.speedLimits.SpeedLimits(config.speedLimits, config.maxSpeed)
road = simulation.road.Road(config.lanes, config.length, speedLimits)
simulation = SimulationManager(road, config.trafficGenerator, config.updateFrame)
representation = Representation(screen, road, simulation)

# Run simulation
while simulation.running:
    # Process key presses
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            simulation.processKey(event.key)

    # Update and display simulation
    clock.tick_busy_loop(config.maxFps)
    dt = clock.get_time()
    simulation.update(dt)
    representation.draw(dt * simulation.timeFactor)
    pygame.display.flip()
