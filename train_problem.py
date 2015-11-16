#!/usr/bin/python
import re
from sys import stdin, exit 

#Neal Strong
#Zulily Train coding problem
#11/13/2015

MAX_CARS = 50
def test_train(engine_index, car_list):
    """This function will take an index for the engine of a train, 
    and the list of all available cars. We will remove the engine
    from the list before processing. We will return a Train object
     """
    working_list = list(car_list)
    train = Train(working_list[engine_index])
    del(working_list[engine_index])
    keep_going = True
    last_count = len(working_list)
    while keep_going:
        excisions = []
        for i in range(len(working_list)):
            car = working_list[i]
            if train.can_shoehorn(car):
                train.shoehorn(car)
                excisions.append(i)
            elif train.end.back == car.front:
                train.couple(car)
                excisions.append(i)
        #handle excisions from working list at the end of each
        #for loop
        excisions.reverse()
        for item in excisions:
            del(working_list[item])
        #test to see if we should continue looping
        if len(working_list) == last_count:
            keep_going = False
        last_count = len(working_list)
    return train

def my_train_compare(train1, train2):
    train1len = train1.length()
    train2len = train2.length()
    train1name = train1.name()
    train2name = train2.name()
    if train1len == train2len:
        if train1name == train2name:
            return 0
        if train1name < train2name:
            return -1
        if train1name > train2name:
            return 1
    if train1len > train2len:
        return -1
    if train1len < train2len:
        return 1

class FreightCar:

    MIN_CAR_LENGTH = 3
    MAX_CAR_LENGTH = 10
    VALID_CAR_CHARACTERS = '[A-Z]{%s,%s}' % (MIN_CAR_LENGTH, MAX_CAR_LENGTH)
    """Class to represent a freight car object. Rules as follows:
       - A-Z characters only
       - Length between 3 and 10 inclusive
       - Front defined as lowest alphabetical value between first
         and last characters upon instantiation.
       - Possible connections on front and back with other 
         FreightCars with matching letters (ABC - CBD - DJZ) """
    def __init__(self, name):
        if len(name) not in range(self.MIN_CAR_LENGTH, self.MAX_CAR_LENGTH):
            raise ValueError("name must be between 3 and 10 characters inclusive") 
            exit(1)
        matches = re.match(self.VALID_CAR_CHARACTERS, name)
        if matches.group() != name:
            raise ValueError("invalid name. Name must be characters A-Z and \
                length between 3 and 10 inclusive")
            exit(1)
        if name[:len(name)/2] > name[len(name)/2:][::-1]:
            name = name[::-1]
        self.name = name
        self.front = name[0]
        self.back = name[-1]
        self.front_car = None
        self.back_car = None

    def __str__(self):
        return "FreightCar name: %s" % (self.name)

    def can_couple(self, car):
        """param car represents a FreightCar object, if the car can couple
         to the current car return True, otherwise return False"""
        if not isinstance(car, FreightCar):
            raise TypeError("comparison car must be of type FreightCar")
        if car.front == self.back:
            return True
        if car.back == self.front:
            return True
        return False

    def couple(self, car):
        """param car represents a FreightCar object. Couples cars together
        preferring to couple to the back of the base car object"""
        if not isinstance(car, FreightCar):
            raise TypeError("comparison car must be of type FreightCar")
        if car.front == self.back:
            self.back_car = car
            car.front_car = self
            return True
        if car.back == self.front:
            self.front_car = car
            car.back_car = self
            return True
        return False

class Train:
    """class to represent a train of FreightCars with length > 0. Class will
    track a linked list of FreightCars with an immutable front car and 0 or
    more additional cars linked together. a representation of the links will
    also be maintained for the purpose of handling possible shoehorning of 
    cars into an existing link"""
    def __init__(self, car):
        self.links = []
        self.cars = []
        if not isinstance(car, FreightCar):
            raise TypeError("initial car must be of type FreightCar")
        self.head = car
        self.end = car
        self.cars.append(car)

    def __str__(self):
        return self.name()

    def couple(self, car):
        if not isinstance(car, FreightCar):
            raise TypeError("initial car must be of type FreightCar")
        self.end.couple(car)
        self.cars.append(car)
        self.links.append(car.front)
        self.end = car

    def shoehorn(self, car):
        link_index = self.links.index(car.front)
        sub_head = link_index 
        sub_tail = link_index + 1
        self.cars[sub_head].couple(car)
        car.couple(self.cars[sub_tail])
        self.cars = self.cars[:sub_tail] + [car] + self.cars[link_index+1:]
        self.links = self.links[:sub_tail] + [car.front] + self.links[link_index:]

    def can_shoehorn(self, car):
        if car.front != car.back:
            return False
        try:
            index = self.links.index(car.front)
            return True
        except ValueError:
            return False

    def length(self):
        return len(self.cars)

    def name(self):
        out = ""
        for car in self.cars:
            out += car.name + "-"
        out = out[:-1]
        return out

if __name__ == "__main__":
    #Read the first line of input representing total number of cars
    #Value must be integer, >0, < MAX_CARS
    try:
        num_cars = int(stdin.readline())
    except ValueError:
        print "Invalid value for number of cars\n"
        print "Number of cars must be an integer\n"
        exit(1)

    if 0 < num_cars > MAX_CARS:
        print "Invalid value for number of cars\n"
        print "Number of cars must be betwen 1 and 50 inclusive\n"
        print "Number of cars was understood as %s\n" % (num_cars)
        exit(1)

    car_list = []
    for x in range(num_cars):
        freight_car = FreightCar(stdin.readline().rstrip())
        car_list.append(freight_car)

    my_trains = []
    for x in range(len(car_list)):
        train = test_train(x, car_list)
        my_trains.append(train)
        del(train)

    my_trains.sort(my_train_compare)
    print my_trains[0].name() 
    exit(0)
    
