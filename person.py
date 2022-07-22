import math
import random
import statistics

cone_angular_width = 50

def normalize_angle(ang):
    if ang < 0:
        ang += 360
    if ang > 360:
        ang -= 360
    return ang

class Person:

    def __init__(self, x_pos, y_pos, dir_deg, step_size, sight_distance):
        self.x = x_pos
        self.y = y_pos
        self.dir_deg = dir_deg # angle from positive x axis in degrees
        self.step_size = step_size
        self.sight_distance = sight_distance

    def __str__(self):
        return 'Person(x=' + str(self.x) + ', y=' + str(self.y) + ', dir=' + str(self.dir_deg) + ', step_size=' \
               + str(self.step_size) + ', sight_dist=' + str(self.sight_distance) + ')'

    def distance(self, other):
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

    def angle_to(self, other):
        return math.degrees(math.atan2((other.y - self.y), (other.x - self.x)))

    def in_angular_view(self, other):
        counter_clock_wise = normalize_angle(self.dir_deg + cone_angular_width/2)
        clock_wise = normalize_angle(self.dir_deg - cone_angular_width / 2)
        alpha = self.angle_to(other)
        if counter_clock_wise > clock_wise: #hakol beseder
            return (alpha<counter_clock_wise and alpha>clock_wise)
        else: #oh no no no
            return (alpha<counter_clock_wise or alpha>clock_wise)

    def in_distance_view(self, other):
        return (self.distance(other) <= self.sight_distance)

    # def angle_to_door(self, door):
    #     tmp = list(door)
    #     delt_x = tmp[0] - self.x
    #     delt_y = tmp[1] - self.y
    #     return math.atan2(delt_y, delt_x)
    #
    # def door_in_angview(self, door):
    #     print(self.dir_deg)
    #     counter_clock_wise = normalize_angle(self.dir_deg + cone_angular_width/2)
    #     clock_wise = normalize_angle(self.dir_deg - cone_angular_width/2)
    #     alpha = self.angle_to_door(door)
    #     if counter_clock_wise > clock_wise: #it's fineeee
    #         return (alpha<counter_clock_wise and alpha>clock_wise)
    #     else: #we fucked up
    #         return (alpha<counter_clock_wise or alpha>clock_wise)
    #
    # def dist_to_door(self, door):
    #     tmp = list(door)
    #     return math.sqrt((tmp[0] - self.x) ** 2 + (tmp[1] - self.y) ** 2)
    #
    # def door_in_distview(self, door):
    #     return (self.dist_to_door(door) <= self.sight_distance)
    #
    # def run_away(self, door):
    #     if self.door_in_angview(door) and self.door_in_distview(door):
    #         print("door in view")
    #         if self.dist_to_door(door) < self.step_size:
    #             self.step_size = self.dist_to_door(door)

    def new_loc(self):
        new_x = self.x + self.step_size * math.cos(math.radians(self.dir_deg))
        new_y = self.y + self.step_size * math.sin(math.radians(self.dir_deg))
        self.x = new_x
        self.y = new_y

    def dir_to_door_in_view(self, building):
        reach_list = self.ten_point_arc()

        return None

    def new_dir(self, people_list, building):
        # is there a door? if so, get new direction of door
        dir_to = self.dir_to_door_in_view(building)
        if dir_to != None:
            self.dir_deg = dir_to
            return
        # else take direction of crowd
        people_i_see_angles_list = []
        for neighbor in people_list:
            if self is not neighbor:
                if self.in_angular_view(neighbor) and self.in_distance_view(neighbor):
                    people_i_see_angles_list.append(neighbor.dir_deg)
        if len(people_i_see_angles_list) > 0:
            self.dir_deg = (statistics.median(people_i_see_angles_list) + self.dir_deg)/2

    def ten_point_arc(self):
        dot_list = []
        max_sight = self.dir_deg + cone_angular_width/2
        min_sight = self.dir_deg - cone_angular_width / 2

        for ang in range(math.floor(min_sight), math.floor(max_sight), math.floor(cone_angular_width/10)):
            x_dot = self.x + self.sight_distance * math.cos(math.radians(ang))
            y_dot = self.y + self.sight_distance * math.sin(math.radians(ang))
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

    def fuck_corners(self, building):
        if self.corner_check(building):
            while self.corner_check(building):
                self.dir_deg = random.uniform(0, 360)

    def wall_avoidance(self, building):
        self.fuck_corners(building)
        view_dot_list = self.ten_point_arc()
        new_dir_list = [self.dir_deg]
        for point in view_dot_list:
            if point[0] > building.length or point[0] < 0:
                if 90 >= self.dir_deg > 0 or 180 >= self.dir_deg > 90:
                    new_dir_list.append(90)
                elif 270 <= self.dir_deg < 360 or 180 < self.dir_deg <= 270:
                    new_dir_list.append(270)
            elif point[1] > building.width or point[1] < 0:
                if 90 > self.dir_deg >= 0 or 270 < self.dir_deg <= 360:
                    new_dir_list.append(0)
                elif 180 >= self.dir_deg > 90 or 180 <= self.dir_deg < 270:
                    new_dir_list.append(180)
        return statistics.median(new_dir_list)