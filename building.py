import matplotlib.pyplot as plt

class Building:
    def __init__(self, length, width, doors):
        self.length = length
        self.width = width
        self.doors = doors.copy()

    def plot_me(self):
        #walls
        plt.plot([0, 0,self.length, self.length, 0],[0, self.width, self.width, 0, 0], 'k-')
        #north door
        door = self.doors.get("north")
        if door != None:
            plt.plot([door.door_loc - door.door_width / 2, door.door_loc + door.door_width / 2],
                 [self.width, self.width], 'r-')
        #east door
        door = self.doors.get("east")
        if door != None:
            plt.plot([self.length, self.length],
                 [self.width - door.door_loc - door.door_width / 2, self.width - door.door_loc + door.door_width / 2], 'r-')
        #south door
        door = self.doors.get("south")
        if door != None:
            plt.plot([self.length - door.door_loc - door.door_width / 2,
                  self.length - door.door_loc + door.door_width / 2], [0, 0], 'r-')
        #west door
        door = self.doors.get("west")
        if door != None:
            plt.plot([0, 0], [door.door_loc - door.door_width / 2, door.door_loc + door.door_width / 2], 'r-')

    class Door:
        def __init__(self, door_loc, door_width):
            self.door_loc = door_loc
            self.door_width = door_width

# mydoors = {}
# mydoors["north"] = Building.Door(70, 20)
# mydoors["south"] = Building.Door(20, 10)
# mydoors["west"] = Building.Door(30, 10)
#
# myBuilding = Building(100, 159, mydoors)
# fig, axs = plt.subplots()
# axs.set_aspect('equal', 'box')
# fig.tight_layout()
# myBuilding.plot_me()
# plt.show()