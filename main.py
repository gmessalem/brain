import random
import person
import building
import point
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")


if __name__ == '__main__':
    number_of_people = 10
    number_of_itterations = 100
    fire_radius = 10
    # number_of_fires = 2

    my_building = building.Building(length=100, width=160, doors={"north" : building.Building.Door(loc=70, width=20),
                                                                  "south" : building.Building.Door(loc=20, width=10),
                                                                  "east": building.Building.Door(loc=30, width=10)},
                                    fires=[point.Point(20, 20), point.Point(80, 70), point.Point(40, 50), point.Point(2, 90)])

    # make sure steps are not equal or longer than door sizes
    persons = [person.Person(loc=point.Point(random.uniform(0, my_building.length), random.uniform(0, my_building.width)),
                             dir_deg=random.uniform(0, 360), step_size=1, sight_distance=10) for i in range(number_of_people)]

    #debug person
    # persons = [person.Person(loc=point.Point(60, 45), dir_deg=180, step_size=1, sight_distance=10)]


    def step(people_list):
        new_people_list = []
        for p in people_list:
            # print(p)
            new_person = p
            new_person.new_dir(people_list, my_building)
            new_person.new_loc()
            if new_person.loc.x > my_building.length:
                print(new_person, "elvis has left the building!")
                continue
                # new_person.loc.x = my_building.length # <-- fix this as well
            elif new_person.loc.x < 0:
                print(new_person, "elvis has left the building!")
                continue
                # new_person.loc.x = 0
            if new_person.loc.y > my_building.width:
                print(new_person, "elvis has left the building!")
                continue
                # new_person.loc.y = my_building.width
            elif new_person.loc.y < 0:
                print(new_person, "elvis has left the building!")
                continue
                # new_person.loc.y = 0
            new_people_list.append(new_person)
        return new_people_list


    plt.ion()
    fig, axs = plt.subplots()
    axs.set_aspect('equal', 'box')
    fig.tight_layout()
    plt.show(block=False)

    my_building.plot_me(plt)
    plt.pause(1)

    #plot people's starting point in red
    for p in persons:
        p.plot_me('rx')
    plt.pause(1)

    while len(persons) > 0:
        persons_new = step(persons)

        for p in persons_new:
            p.plot_me('g.')

        plt.pause(0.2)
        persons = persons_new