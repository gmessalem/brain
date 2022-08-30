import random

import matplotlib.pyplot as plt
import point

class Building:
    def __init__(self, length, width, doors, fires):
        self.length = length
        self.width = width
        self.fires = fires
        self.doors = doors.copy()
        for dir in self.doors:
            door = self.doors.get(dir)
            if door != None:
                door.building = self
                door.dir = dir

    def __str__(self):
        doors = ""
        sep = ""
        for dir in self.doors:
            doors += sep + "door[" + dir + "] = " + str(self.doors.get(dir))
            sep = ", "
        return 'Building(length=' + str(self.length) + ', width=' + str(self.width) + ', doors=' + doors + ')'

    def plot_me(self, axes):
        #walls
        axes.plot([-1, -1,self.length+1, self.length+1, -1],[-1, self.width+1, self.width+1, -1, -1], 'k-')

        #doors
        for dir in self.doors:
            door = self.doors.get(dir)
            if door != None:
                corners = door.get_corners()
                plt.plot([corners[0].x, corners[1].x],
                     [corners[0].y, corners[1].y], 'r-')

        #fires
        for fire in self.fires:
            plt.plot(fire.x, fire.y, 'yX')

    class Door:
        def __init__(self, loc, width):
            self.building = None
            self.dir = None
            self.loc = loc
            self.width = width


        def __str__(self):
            return 'Door(loc=' + str(self.loc) + ', width=' + str(self.width) + ')'

        def get_corners(self):
            corners = []
            if self.dir == "north":
                corners.append(point.Point(self.loc - self.width/2, self.building.width))
                corners.append(point.Point(self.loc + self.width/2, self.building.width))
            elif self.dir == "south":
                corners.append(point.Point(self.building.length - self.loc - self.width/2, 0))
                corners.append(point.Point(self.building.length - self.loc + self.width/2, 0))
            elif self.dir == "east":
                corners.append(point.Point(self.building.length, self.building.width - self.loc - self.width/2))
                corners.append(point.Point(self.building.length, self.building.width - self.loc + self.width/2))
            elif self.dir == "west":
                corners.append(point.Point(0, self.loc - self.width/2))
                corners.append(point.Point(0, self.loc + self.width/2))
            return corners
    class Fire:
        def __init__(self, loc):
            self.loc = loc

        def __str__(self):
            return 'Fire(loc=' + str(self.loc) + ')'