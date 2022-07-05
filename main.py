# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import random
import person
import building
import math
import statistics
import matplotlib.pyplot as plt

# sight_dist = 10


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    number_of_itterations = 50
    building = building.Building(100,100)
    persons = [person.Person(random.uniform(0, building.length), random.uniform(0, building.width), random.uniform(0, 360), 1, 10) for i in
               range(100)]


    def step(people_list):
        new_people_list = []
        for p in people_list:
            p.print()
            new_person = p
            new_person.new_dir(people_list)
            new_person.new_loc()
            new_people_list.append(new_person)
        return new_people_list


    def run_all(n, people_list):
        for _ in range(n):
            people_list = step(people_list)
        return people_list


    persons = run_all(number_of_itterations, persons)

    plt.plot([p.x for p in persons], [p.y for p in persons], 'r.')

    run_all(50, persons)

    plt.plot([p.x for p in persons], [p.y for p in persons], 'b.')

    plt.show()


