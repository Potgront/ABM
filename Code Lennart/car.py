from mesa import Model
from mesa import Agent
import random

class Car(Agent):
    def __init__(self, unique_id, size=1, start_lane=0, speed=100):
        self.unique_id = unique_id
        self.size = size
        self.start_lane = start_lane
        self.x = 0
        self.y = start_lane + 0.5
        self.speed = speed
        self.new_x = 0

    def step(self):
        self.new_x = self.x + self.speed
    
    def advance(self):
        self.x = self.new_x

    def visualize(self, plot):
        plot.scatter(self.x, self.y, s=100, marker='s')
