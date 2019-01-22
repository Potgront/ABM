""" Module which defines the car agents
"""
from mesa import Agent
import numpy as np


class Car(Agent):
    """
    Defines the properties and behaviour of each car agent.
    """
    def __init__(self, unique_id, model, start_lane=0, speed=1):
        super().__init__(unique_id, model)
        self.start_lane = start_lane
        self.lane = start_lane
        self.x = 0
        self.y = start_lane
        self.pos = (self.x, self.y)
        self.speed = speed
        self.max_speed = speed
        self.braked = 0

    def is_free(self, lane, view=1):
        '''
        Checks if the lane is free.
            view: how many places to look ahead
            lane: which lane to check: -1 = right, 0 = same, 1 = left
        '''
        view = self.speed*1.1
        a = -1*int(5*self.speed/self.max_speed)
        if lane == 0:
            '''
            Dont check behind if staying in the same lane
            '''
            a = 1
        view = int(min(self.model.length-self.x-1, view))
        if view == lane == 0:
            return True
        if not self.model.lanes > (self.y + lane) >= 0:
            return False
        for x in range(a, view+1):
            if (self.x+x, self.y+lane) in self.model.occupied:
                return False
        return True
        # cells = [(self.x+x, self.y+_lane) for x in range(_a, _view+1)]
        # contents = self.model.grid.get_cell_list_contents(cells)
        # return not contents
        # bool_list = [self.model.grid.is_cell_empty((self.x+x, self.y+_lane))
        #              for x in range(_a, _view+1)]
        # if not bool_list:
        #     return True
        # return all(bool_list)

    def is_slowed(self):
        """
        Check if the agent is below their maximum speed
        """
        return self.speed < self.max_speed

    def check_speed(self):
        """
        Check if the car has recently braked and otherwise can speed up.
        """
        if self.braked:
            self.braked -= np.random.randint(0, self.braked+1)
        diff = self.max_speed - self.speed
        speedup = min(np.random.randint(1, diff+1), 10)
        while speedup and not self.is_free(speedup):
            speedup -= 1
        self.speed += speedup

    def step(self):
        """
        Perform the initial scheduled agent step.
        """
        if self.speed == 0:
            if self.is_free(0):
                self.x += 1
            elif self.is_free(-1):
                self.x += 1
                self.y -= 1
            elif self.is_free(1):
                self.x += 1
                self.y += 1

        elif self.is_free(0):
            '''
            Move ahead if the current speed allows
            '''
            self.x += self.speed
            if self.is_free(-1):
                '''
                Move a lane to the right if speed allows
                '''
                self.y -= 1

        elif self.is_free(1):
            '''
            Move a lane to the left if the speed allows
            '''
            self.x += self.speed
            self.y += 1

        else:
            '''
            Slow down 1 tick if none are possible
            '''
            self.braked = 5
            self.speed = max(self.speed-1, 0)
            while self.speed and not\
                    self.is_free(0):
                self.speed = max(self.speed-1, 0)
            self.x += self.speed

        self.model.move(self, (self.x, self.y))

        if self.is_slowed():
            self.check_speed()

    # def advance(self):
    #     """
    #     Perform the closing scheduled agent step.
    #     """
