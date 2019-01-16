from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import SingleGrid
import matplotlib.pyplot as plt
import random

import road
import cargrid as car


class RoadSim(Model):
    def __init__(self, lanes=2, length=500):
        super().__init__()
        print(lanes)
        self.current_id=0
        self.lanes = lanes
        self.spawn_chance = 0.5
        self.length = length

        # self.grid = road.RoadGrid(lanes=self.lanes)
        self.grid = SingleGrid(self.length, self.lanes, True)

        self.schedule = SimultaneousActivation(self)

        # car1 = car.Car()
        self.cars = []
        self.new_car()
        self.new_car(start_lane=1, speed=2)

    def init_cars(self):
        r = random.random()
        if r < self.spawn_chance:
            speed = random.randint(2,5)
            print(self.lanes)
            start_lane = random.randint(0, self.lanes - 1)
            free_space = [self.grid.is_cell_empty((x, start_lane)) for x in range(10)]
            if all(free_space):
                self.new_car(speed=speed, start_lane=start_lane)


    def new_car(self, start_lane=0, speed=1):
        new_car = car.Car(self.next_id(), self,
                            start_lane=start_lane, speed=speed)

        print(new_car.y)
        self.grid.place_agent(new_car, (new_car.x, new_car.y))
        self.cars.append(new_car)
        getattr(self, f'schedule').add(new_car)

    def step(self):
        self.schedule.step()
        self.init_cars()
        # self.carplot.set_offsets([(car[0], car[1])
        #                                 for car in self.road.env._agent_points])
        # self.carplot.set_color([car.color for car in self.cars])
        # self.visualise()

    # def run_sim(self, steps=500):
    #     # self.visualise()
    #     for _ in range(steps):
    #         # plt.draw()
    #         self.step()
    #         print("hoi")
    #         self.init_cars()
    #         # plt.pause(0.001)
    
    def visualise(self):
        plt.ion()
        self.fig = plt.figure(figsize=(50, 5), dpi=80)
        self.plot = self.fig.gca()
        self.road.visualise(self.plot)

        # print(list(list(zip(*self.cars))[0]))
        # self.carplot = self.plot.scatter([car[0] for car in self.road.env._agent_points],
        #                         [car[1] for car in self.road.env._agent_points], s=100, marker='s')
