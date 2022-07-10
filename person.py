import math
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
        self.dir_deg = dir_deg # angle from positive x axis
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
        else:
            return (alpha<counter_clock_wise or alpha>clock_wise)

    def in_distance_view(self, other):
        return (self.distance(other) <= self.sight_distance)

    def new_loc(self):
        new_x = self.x + self.step_size * math.cos(math.radians(self.dir_deg))
        new_y = self.y + self.step_size * math.sin(math.radians(self.dir_deg))
        self.x = new_x
        self.y = new_y

    def new_dir(self, people_list):
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
        sight_range = max_sight - min_sight
        for ang in range(0, math.floor(sight_range), math.floor(sight_range/10)):
            x_dot = self.sight_distance * math.cos(math.radians(ang))
            y_dot = self.sight_distance * math.sin(math.radians(ang))
            dot_list.append((x_dot, y_dot))
        return dot_list