import random
import person
import building
import matplotlib.pyplot as plt


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


    plt.plot([p.x for p in persons], [p.y for p in persons], 'r.')
    for _ in range(number_of_itterations):
        persons = step(persons)
        plt.plot([p.x for p in persons], [p.y for p in persons], 'g.')

    plt.plot([p.x for p in persons], [p.y for p in persons], 'b.')

    plt.show()


