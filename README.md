# Nagel-Schreckenberg Simulation

[![Python](https://github.com/tim-day-387/Nagel-Schreckenberg-simulation/actions/workflows/python-app.yml/badge.svg)](https://github.com/tim-day-387/Nagel-Schreckenberg-simulation/actions/workflows/python-app.yml)

Traffic simulation based on Nagel-Schreckenberg model with:
* n lanes
* traffic lights
* speed limits
* obstacles
* intersections

## Running the Model

To run simulation: 
```
python nagel.py config.someLights
```

## How to create simulation?
Copy existing simulation in ```config``` directory, and read the comments in sample configs.
## Lane change model

In each iteration

1. Car checks maximum speed it can achieve on it's current position (x, lane) and adjacent lane (x, lane+1).
2. If the potential maximal speed on lane+1 is higher it checks safe conditions: 
  * There is no car car on (x, lane+2) to avoid collision caused by two parallel cars changing lane to lane+1.
  * Distance to previous car on lane+1 is greater that it's speed to avoid emergency braking of previous car.
3. Change lane with probability P.

Same steps for lane-1
