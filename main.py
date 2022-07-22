import random
import person
import building
import matplotlib.pyplot as plt
import math


if __name__ == '__main__':
    number_of_itterations = 100

    mydoors = {}
    mydoors[building.Compass.north] = building.Building.Door(70, 20)
    mydoors[building.Compass.south] = building.Building.Door(20, 10)
    mydoors[building.Compass.east] = building.Building.Door(30, 10)
    mydoors[building.Compass.west] = building.Building.Door(60, 10)
    my_building = building.Building(100, 160, mydoors)

    n_door = (-1, -1)
    e_door = (-1, -1)
    s_door = (-1, -1)
    w_door = (-1, -1)

    for dir in mydoors:
        if mydoors[dir].door_loc != -1:
            if dir == building.Compass.north:
                tmp = list(n_door)
                tmp[0] = mydoors[dir].door_loc
                tmp[1] = my_building.width
                n_door = tuple(tmp)
                print(n_door)
            if dir == building.Compass.south:
                tmp = list(s_door)
                tmp[0] = (my_building.length - mydoors[dir].door_loc)
                tmp[1] = 0
                s_door = tuple(tmp)
                print(s_door)
            if dir == building.Compass.east:
                tmp = list(e_door)
                tmp[0] = my_building.length
                tmp[1] = (my_building.width - mydoors[dir].door_loc)
                e_door = tuple(tmp)
                print(e_door)
            if dir == building.Compass.west:
                tmp = list(w_door)
                tmp[0] = 0
                tmp[1] = mydoors[dir].door_loc
                w_door = tuple(tmp)
                print(w_door)

    # building = building.Building(100,100)
    persons = [person.Person(random.uniform(0, my_building.length), random.uniform(0, my_building.width), random.uniform(0, 360), 1, 10) for i in
               range(100)]


    def step(people_list):
        new_people_list = []
        for p in people_list:
            print(p)
            new_person = p
            new_person.new_dir(people_list)
            new_person.new_loc()
            new_person.dir_deg = (new_person.wall_avoidance(my_building) + new_person.dir_deg)/2
            if new_person.x > my_building.length:
                new_person.x = my_building.length
            elif new_person.x < 0:
                new_person.x = 0
            if new_person.y > my_building.width:
                new_person.y = my_building.width
            elif new_person.y < 0:
                new_person.y = 0
            new_people_list.append(new_person)
        return new_people_list


    fig, axs = plt.subplots()
    axs.set_aspect('equal', 'box')
    fig.tight_layout()

    door_list = []

    plt.plot([p.x for p in persons], [p.y for p in persons], 'r.')
    if n_door[0] != -1:
        for i in range(n_door[0] - int(mydoors[building.Compass.north].door_width/2),
                       n_door[0] + int(mydoors[building.Compass.north].door_width/2),
                       math.ceil((mydoors[building.Compass.north].door_width/50))):
            door_list.append((i, my_building.width))
    if s_door[0] != -1:
        for i in range(my_building.length - s_door[0] - int(mydoors[building.Compass.south].door_width/2),
                       my_building.length - s_door[0] + int(mydoors[building.Compass.south].door_width / 2),
                       math.ceil((mydoors[building.Compass.south].door_width / 50))):
            door_list.append((i, 0))
    if e_door[0] != -1:
        for i in range(e_door[1] - int(mydoors[building.Compass.east].door_width/2),
                       e_door[1] + int(mydoors[building.Compass.east].door_width/2),
                       math.ceil((mydoors[building.Compass.east].door_width/50))):
            door_list.append((my_building.length, i))
    if w_door[0] != -1:
        for i in range(w_door[1] - int(mydoors[building.Compass.west].door_width / 2),
                       w_door[1] + int(mydoors[building.Compass.west].door_width / 2),
                       math.ceil((mydoors[building.Compass.west].door_width / 50))):
            door_list.append((0, i))
    plt.plot([tup[0] for tup in door_list], [tup[1] for tup in door_list], 'mo')

    for _ in range(number_of_itterations):
        persons = step(persons)
        plt.plot([p.x for p in persons], [p.y for p in persons], 'g.')

    plt.plot([p.x for p in persons], [p.y for p in persons], 'b.')

    plt.show()


