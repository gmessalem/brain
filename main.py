import random
import person
import building
import point
import statistics
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")

#doors:
#doors={"north" : building.Building.Door(loc=50, width=10),
                                                                  # "south" : building.Building.Door(loc=50, width=10),
                                                                  # "east": building.Building.Door(loc=75, width=10),
                                                                  # "west": building.Building.Door(loc=75, width=10)}

# fires=[point.Point(50, 145), point.Point(50, 5), point.Point(5, 75), point.Point(95, 75)]

if __name__ == '__main__':
    number_of_people = 100
    number_of_itterations = 20
    fire_radius = 10
    lethality_limit = 250
    with_graphics = False

    # my_building = building.Building(length=110, width=165, doors={"north" : building.Building.Door(loc=55, width=10),
    #                                                               "south" : building.Building.Door(loc=55, width=10),
    #                                                               "east": building.Building.Door(loc=82.5, width=10),
    #                                                               "west": building.Building.Door(loc=82.5, width=10)},
    #                                 fires=[point.Point(55, 5), point.Point(5, 82.5), point.Point(105, 82.5)],
    #                                 door_lighting=1)

    my_building = building.Building(length=110, width=165, doors={"north" : building.Building.Door(loc=55, width=10),
                                                                  "south" : building.Building.Door(loc=55, width=10),
                                                                  "east": building.Building.Door(loc=82.5, width=10),
                                                                  "west": building.Building.Door(loc=82.5, width=10)},
                                    fires=[point.Point(55, 140), point.Point(55, 25), point.Point(25, 82.5), point.Point(85, 82.5)],
                                    door_lighting=1)



    #debug person
    # persons = [person.Person(loc=point.Point(60, 45), dir_deg=180, step_size=1, sight_distance=10)]


    def step(people_list):
        global lethality_limit
        global lethality_countdown
        new_people_list = []
        for p in people_list:
            # print(p)
            new_person = p
            new_person.new_dir(people_list, my_building)
            new_person.new_loc()
            if new_person.loc.x > my_building.length:
                # print(new_person, "elvis has left the building!")
                continue
                # new_person.loc.x = my_building.length # <-- fix this as well
            elif new_person.loc.x < 0:
                # print(new_person, "elvis has left the building!")
                continue
                # new_person.loc.x = 0
            if new_person.loc.y > my_building.width:
                # print(new_person, "elvis has left the building!")
                continue
                # new_person.loc.y = my_building.width
            elif new_person.loc.y < 0:
                # print(new_person, "elvis has left the building!")
                continue
                # new_person.loc.y = 0
            new_people_list.append(new_person)
        lethality_countdown -= 1
        if lethality_countdown <= 0:
            # print("Simulation Time: " + str(lethality_limit) + " steps\nCasualties: " + str(len(people_list)/number_of_people*100) + "%")
            return new_people_list
        return new_people_list

    multi_run_casualties_percent = []

    for _ in range(number_of_itterations):
        lethality_countdown = lethality_limit

        # make sure steps are not equal or longer than door sizes
        persons = [
            person.Person(loc=point.Point(random.uniform(0, my_building.length), random.uniform(0, my_building.width)),
                          dir_deg=random.uniform(0, 360), step_size=1, sight_distance=10) for i in
            range(number_of_people)]

        if with_graphics == True:
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



        while lethality_countdown > 0:
            persons_new = step(persons)

            if with_graphics == True:
                for p in persons_new:
                    p.plot_me('g.')

                plt.pause(0.2)
            persons = persons_new
        multi_run_casualties_percent.append(round(len(persons)/number_of_people*100)) #something is wrong, bug here
    print(multi_run_casualties_percent)
    print("The average percent of casualties over", str(number_of_itterations), "runs is:",str(statistics.mean(multi_run_casualties_percent)) + "%")
    print(statistics.stdev(multi_run_casualties_percent))