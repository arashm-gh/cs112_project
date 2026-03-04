from typing import List, Dict, Optional
from enum import Enum

class Component:
    def __init__(self, x:int, y:int, r:int):
        self.pos_x : int = x
        self.pos_y : int = y
        self.orientation : int = r
        self.input = 0
        self.output = 0
        
    def compute(self):
        pass

    @property # this is called a dectorator - it'll just let me run a function when all i have to do is write .something !! it uses less space and stuff
    def texture(self) -> str:
        pass


class Battery(Component):
    def compute(self):
        self.output = 1
    
    @property
    def texture(self) -> str:
        return "battery"


class Bulb(Component):
    def compute(self):
        if self.input >= 1:
            self.output = 1
        else:
            self.output = 0
    @property
    def texture(self) -> str:
        if self.input >= 1:
            return "bulb_on"
        else:
            return "bulb_off"

class Switch(Component):
    def __init__(self, x:int, y:int, r:int):
        super().__init__(x, y, r)
        self.__toggle = False
    def compute(self):
        if self.input >= 1 and self.__toggle:
            self.output = 1
        else:
            self.output = 0
    def toggle(self):
        self.__toggle = not self.__toggle
    @property
    def texture(self) -> str:
        if self.__toggle:
            return "switch_on"
        else:
            return "switch_off"



class Wire(Component):
    def compute(self):
        self.output = self.input

class Circuit:
    def __init__(self, components : List[Component]):
        self.components = components
        self.grid : Dict[tuple, Component] = {} # dictionary where eahc position is the xy of each component
    def add_component(self, comp:Component):
        self.components.append(comp)
        self.grid[(comp.pos_x, comp.pos_y)] = comp
        self.update_connections(comp)
    def remove_component(self, comp:Component):
        if comp in self.components:
            self.components.remove(comp)
            del self.grid[(comp.pos_x, comp.pos_y)]
    def update_connections(self, comp:Component):
        left_neighbor = self.grid.get((comp.pos_x -1, comp.pos_y))
        if left_neighbor:
            pass
        right_neighbor = self.grid.get((comp.pos_x +1, comp.pos_y))
        if right_neighbor:
            pass
    def get_component_at(self, x, y):
        return self.grid.get((x, y))

    def simulate(self):
        # sort components by x coordinate (left to right)
        sorted_comps = sorted(self.components, key=lambda c: c.pos_x) # this is called an anonymous method
        for comp in sorted_comps:
            # Find left neighbour (input source)
            left_comp = self.grid.get((comp.pos_x - 1, comp.pos_y))
            if left_comp:
                try:
                    comp.input = left_comp.output
                except ValueError as e:
                    print(f"Input error for {comp}: {e}")
            else:
                comp.input = 0   # floating
            comp.compute()