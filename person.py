import math
import statistics

cone_angular_width = 40

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

    def print(self):
        print(self.x, self.y, self.dir_deg)

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
            self.dir_deg = statistics.median(people_i_see_angles_list)

    # def new_dir(self, people_list):
    #     dir_list = []
    #     updated_dir = 0
    #     max_sight = p.dir + 20
    #     min_sight = p.dir - 20
    #     for neighbor in people_list:
    #         if p is not neighbor:
    #             alpha = math.atan2((neighbor.y - p.y), (neighbor.x - p.x))
    #             if alpha > min_sight and alpha < max_sight:
    #                 if p.distance(neighbor) <= sight_dist:
    #                     dir_list.append(neighbor.dir)
    #                     updated_dir = statistics.median(dir_list)
    #                 else:
    #                     updated_dir = p.dir
    #             else:
    #                 updated_dir = p.dir
    #     p.dir = updated_dir