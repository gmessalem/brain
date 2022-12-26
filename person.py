import math
import random
import statistics
import matplotlib.pyplot as plt

cone_angular_width = 100
debug_global_person_id = 0

#todo add point

# return angle between 0 and 360 degrees
def normalize_angle(ang):
    while ang < 0:
        ang += 360
    while ang > 360:
        ang -= 360
    return ang



class Person:
    # global debug_global_person_id
    def __init__(self, loc, dir_deg, step_size, sight_distance):
        global debug_global_person_id
        self.loc = loc
        self.dir_deg = dir_deg # angle from positive x axis in degrees
        self.step_size = step_size
        self.sight_distance = sight_distance
        debug_global_person_id += 1
        self.name = str(debug_global_person_id)

    def __str__(self):
        return 'Person(name=' + self.name + ', loc=' + str(self.loc) + ', dir=' + str(self.dir_deg) + ', step_size=' \
               + str(self.step_size) + ', sight_dist=' + str(self.sight_distance) + ')'

    def plot_me(self, colorstyle):
        plt.plot([self.loc.x], [self.loc.y], colorstyle)

    def plot_debug(self, ax):
        ax.annotate("", xy=(self.loc.x + self.sight_distance*math.cos(math.radians(self.dir_deg)),
                            self.loc.y + self.sight_distance*math.sin(math.radians(self.dir_deg))),
                    xytext=(self.loc.x, self.loc.y), arrowprops = dict(arrowstyle="->"))

    def distance_between_points(self, p1, p2):
        return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

    def angle_to(self, p):
        return self.angle_between_points(self.loc, p)

    def in_angular_view(self, p):
        counter_clock_wise = normalize_angle(self.dir_deg + cone_angular_width/2)
        clock_wise = normalize_angle(self.dir_deg - cone_angular_width / 2)
        alpha = normalize_angle(self.angle_to(p))
        if counter_clock_wise > clock_wise: #hakol beseder
            #debug print
            # print("counter_clock: " + str(counter_clock_wise) + "\nclock: " + str(clock_wise) + "\nalpha: " + str(alpha))
            return (alpha<counter_clock_wise and alpha>clock_wise)
        else: #oh no no no
            return (alpha<counter_clock_wise or alpha>clock_wise)

    def angle_between_points(self, p1, p2):
        return math.degrees(math.atan2(p2.y-p1.y, p2.x-p1.x))

    def new_loc(self):
        new_x = self.loc.x + self.step_size * math.cos(math.radians(self.dir_deg))
        new_y = self.loc.y + self.step_size * math.sin(math.radians(self.dir_deg))
        self.loc.x = new_x
        self.loc.y = new_y

    ####################################
    #   method: choose_new_dir()
    #
    #   Choose a direction and set the self.dir_deg accordingly. Steps to follow:
    #   1. Can i see a fire? if so, turn away.
    #   2. Can i see a door? doors? if so, turn towards middle of nearest door.
    #   3. Can i see a wall? walls? if so, turn to avoid collision.
    #   4. Turn in direction of median of people direction
    #
    def new_dir(self, people_list, building):
        #is there a fire? if so, turn away from it
        nearest_fire_dir = self.get_nearest_fire_in_my_view(building)
        if nearest_fire_dir != None:
            # print(self, "i see a fire. turning away from it.")
            self.dir_deg = normalize_angle(nearest_fire_dir)
            return
        # is there a door? if so, get new direction of door
        nearest_door_dir = self.get_nearest_door_in_my_view(building)
        if nearest_door_dir != None:
            # print(self, "i see a door. going to it.")
            corners = building.doors.get(nearest_door_dir).get_corners()
            angle = (self.angle_to(corners[0]) + self.angle_to(corners[1])) / 2
            self.dir_deg = normalize_angle(angle)
            return
        # else avoid wall
        if self.i_see_wall(building):
            # print(self, "i see a wall. avoiding it.")
            self.dir_deg = normalize_angle((self.wall_avoidance_dir(building) + self.dir_deg) / 2)
            return

        # else take direction of crowd
        people_i_see_angles_list = []
        for neighbor in people_list:
            if self is not neighbor:
                if self.in_angular_view(neighbor.loc) and (self.distance_between_points(self.loc, neighbor.loc) <= self.sight_distance):
                    people_i_see_angles_list.append(neighbor.dir_deg)
        if len(people_i_see_angles_list) > 0:
            # print(self, "i see people. going in their general direction.")
            self.dir_deg = (statistics.median(people_i_see_angles_list) + self.dir_deg)/2

    def get_nearest_fire_in_my_view(self, building):
        nearest_fire = {'dir': None, 'distance': 9999}
        for fire in building.fires:
            distance = self.distance_between_points(self.loc, fire)
            if distance <= self.sight_distance:
                if self.in_angular_view(fire):

                    if distance < nearest_fire['distance']:
                        nearest_fire['distance'] = distance
                        nearest_fire['dir'] = normalize_angle(self.angle_to(fire) + 180)
        return nearest_fire['dir']



    def get_nearest_door_in_my_view(self, building):
        nearest_door = {'dir': None, 'distance': 9999}
        for dir in building.doors:
            door = building.doors.get(dir)
            corners = door.get_corners()
            distance = []
            distance.append(self.distance_between_points(self.loc, corners[0]))
            distance.append(self.distance_between_points(self.loc, corners[1]))
            # print("door[" + dir + "] : " + str(door) + ", min distance: " + str(min(distance)))
            min_distance = min(distance)
            if min_distance <= (self.sight_distance * building.door_lighting):
                if self.in_angular_view(corners[0]) or self.in_angular_view(corners[1]):
                    if min_distance < nearest_door['distance']:
                        nearest_door['distance'] = min_distance
                        nearest_door['dir'] = dir
        return nearest_door['dir']

    def ten_point_arc(self):
        dot_list = []
        max_sight = self.dir_deg + cone_angular_width/2
        min_sight = self.dir_deg - cone_angular_width / 2

        for ang in range(math.floor(min_sight), math.floor(max_sight), math.floor(cone_angular_width/10)):
            x_dot = self.loc.x + self.sight_distance * math.cos(math.radians(ang))
            y_dot = self.loc.y + self.sight_distance * math.sin(math.radians(ang))
            dot_list.append((x_dot, y_dot))
        return dot_list

    def corner_check(self, building):
        view_dot_list = self.ten_point_arc()
        out_of_bounds_list = []
        for point in view_dot_list:
            if point[0] > building.length or point[0] < 0:
                out_of_bounds_list.append("x")
            elif point[1] > building.width or point[1] < 0:
                out_of_bounds_list.append("y")
        if "x" in out_of_bounds_list and "y" in out_of_bounds_list:
            return True
        else:
            return False

    def avoid_corners(self, building):
        if self.corner_check(building):
            while self.corner_check(building):
                self.dir_deg = random.uniform(0, 360)

    def i_see_wall(self, building):
        view_dot_list = self.ten_point_arc()
        for point in view_dot_list:
            if point[0] > building.length or point[0] < 0:
                if 90 >= self.dir_deg > 0 or 180 >= self.dir_deg > 90:
                    return True
                elif 270 <= self.dir_deg < 360 or 180 < self.dir_deg <= 270:
                    return True
            elif point[1] > building.width or point[1] < 0:
                if 90 > self.dir_deg >= 0 or 270 < self.dir_deg <= 360:
                    return True
                elif 180 >= self.dir_deg > 90 or 180 <= self.dir_deg < 270:
                    return True
        return False

    def wall_avoidance_dir(self, building):
        self.avoid_corners(building)
        view_dot_list = self.ten_point_arc()
        new_dir_list = [self.dir_deg]
        for point in view_dot_list:
            if point[0] > building.length or point[0] < 0:
                if 90 >= self.dir_deg > 0 or 180 >= self.dir_deg > 90:
                    new_dir_list.append(90)
                elif 270 <= self.dir_deg < 360 or 180 < self.dir_deg <= 270:
                    new_dir_list.append(270)
            if point[1] > building.width or point[1] < 0:
                if 90 > self.dir_deg >= 0:
                    new_dir_list.append(0)
                elif 270 < self.dir_deg <= 360:
                    new_dir_list.append(360)
                elif 180 >= self.dir_deg > 90 or 180 <= self.dir_deg < 270:
                    new_dir_list.append(180)
        return statistics.median(new_dir_list)

