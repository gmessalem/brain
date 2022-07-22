import random
import person
import building
import matplotlib.pyplot as plt


if __name__ == '__main__':
    number_of_itterations = 100

    my_building = building.Building(length=100, width=160, doors={"north" : building.Building.Door(70, 20),
                                                                  "south" : building.Building.Door(20, 10),
                                                                  "east": building.Building.Door(30, 10)})

    # make sure steps are not equal or longer than door sizes
    persons = [person.Person(random.uniform(0, my_building.length), random.uniform(0, my_building.width),
                             random.uniform(0, 360), step_size=1, sight_distance=10) for i in range(100)]


    def step(people_list):
        new_people_list = []
        for p in people_list:
            # print(p)
            new_person = p
            new_person.new_dir(people_list, my_building)
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

    my_building.plot_me()

    #plot people's starting point in red
    plt.plot([p.x for p in persons], [p.y for p in persons], 'r.')

    for _ in range(number_of_itterations):
        persons = step(persons)
        plt.plot([p.x for p in persons], [p.y for p in persons], 'g.')

    plt.plot([p.x for p in persons], [p.y for p in persons], 'b.')

    plt.show()
