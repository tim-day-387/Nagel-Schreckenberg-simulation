# SpeedLimits class
class SpeedLimits:
    # Constructor
    def __init__(self, speedLimits, maxSpeed):
        self.speedLimits = speedLimits
        self.maxSpeed = maxSpeed

    # Update the speed limit
    def update(self):
        for speedLimit in self.speedLimits:
            speedLimit.update()

    # Return the max speed
    def getLimit(self, pos):
        for speedLimit in self.speedLimits:
            if speedLimit.active and speedLimit.inRange(pos):
                return speedLimit.speedLimit
        return self.maxSpeed

    # Determine if should stop
    def shouldStop(self, pos):
        return self.getLimit(pos) == 0

# SpeedLimit class
class SpeedLimit:
    # Constructor
    def __init__(self, range, limit, ticks, active=True):
        # SpeedLimit( ((10, 0), (20, 0)), 3, 0) # Typical speed limit
        # SpeedLimit( ((10, 0), (20, 0)), 0) # Obstacle
        # SpeedLimit( ((10, 0), (20, 0)), 0, 10) # Traffic lights

        # Args:
        #     range: Bounds of the speed limit expressed as an rectangle.
        #     limit: The speed limit.
        #     ticks:
        #         How many cycles does it take to activate/deactivate the speed limit.
        #         Useful for simulating traffic lights.
        #     active:
        #         Whether the speed limit is active in the first cycle. Useful for
        #         simulating traffic lights.
        self.lanes = (range[0][1], range[1][1])
        self.xPos = (range[0][0], range[1][0])
        self.speedLimit = limit
        self.ticks = ticks
        self.active = active
        self.acc = 0

    # Represents a limitation on the road; it can represent a speed limit, traffic lights or an obstacle
    def createObstacle(pos):
        return SpeedLimit( range=(pos,pos), limit=0, ticks=0)

    # Determine if in range of road
    def inRange(self, pos):
        return (self.lanes[0] <= pos[1] <= self.lanes[1]) and (self.xPos[0] <= pos[0] <= self.xPos[1])

    # Update
    def update(self):
        if self.ticks <= 0:
            return
        self.acc += 1
        if self.acc >= self.ticks:
            self.acc = 0
            self.active = not self.active

