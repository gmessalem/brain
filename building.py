from enum import Enum

class Compass(Enum):
    north = 0
    east = 1
    south = 2
    west = 3

class Building:
    def __init__(self, length, width, doors):
        self.length = length
        self.width = width
        self.doors = dict(doors)


    class Door:
        def __init__(self, door_loc, door_width):
            self.door_loc = door_loc
            self.door_width = door_width

# mydoors = {}
# mydoors[Compass.north] = Building.Door(50, 10)
# mydoors[Compass.south] = Building.Door(-1, 10)
# mydoors[Compass.east] = Building.Door(-1, 10)
# mydoors[Compass.west] = Building.Door(-1, 10)
# myBuilding = Building(100, 159, mydoors)