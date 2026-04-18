from typing import List, Dict, Optional
from enum import Enum

class Component:
    def __init__(self, x:int, y:int, r:int):
        self.pos_x : int = x
        self.pos_y : int = y
        self.orientation : int = r
        self.input = 0
        self.output = 0
        
    def get_input_positions(self) -> List[tuple]:
        """Returns a list of (x, y) grid coordinates this component expects power from."""
        if self.orientation == 270: return [(self.pos_x, self.pos_y - 1)] # W
        if self.orientation == 0:   return [(self.pos_x - 1, self.pos_y)] # A
        if self.orientation == 90:  return [(self.pos_x, self.pos_y + 1)] # S
        if self.orientation == 180: return [(self.pos_x + 1, self.pos_y)] # D
        return [(self.pos_x - 1, self.pos_y)] # fallback

    def get_output_positions(self) -> List[tuple]:
        """Returns a list of (x, y) grid coordinates this component sends power to."""
        if self.orientation == 90:  return [(self.pos_x, self.pos_y - 1)] # W
        if self.orientation == 180: return [(self.pos_x - 1, self.pos_y)] # A
        if self.orientation == 270: return [(self.pos_x, self.pos_y + 1)] # S
        if self.orientation == 0:   return [(self.pos_x + 1, self.pos_y)] # D
        return [(self.pos_x + 1, self.pos_y)] # fallback        
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

class BlueLed(Component):
    def compute(self):
        if self.input >= 1:
            self.output = 1
        else:
            self.output = 0
    @property
    def texture(self) -> str:
        if self.input >= 1:
            return "blue_led_on"
        else:
            return "led_off"

class RedLed(Component):
    def compute(self):
        if self.input >= 1:
            self.output = 1
        else:
            self.output = 0
    @property
    def texture(self) -> str:
        if self.input >= 1:
            return "red_led_on"
        else:
            return "led_off"

class GreenLed(Component):
    def compute(self):
        if self.input >= 1:
            self.output = 1
        else:
            self.output = 0
    @property
    def texture(self) -> str:
        if self.input >= 1:
            return "green_led_on"
        else:
            return "led_off"

class Buzzer(Component):
    def compute(self):
        if self.input >= 1:
            self.output = 1
        else:
            self.output = 0
    @property
    def texture(self) -> str:
        if self.input >= 1:
            return "buzzer_on"
        else:
            return "buzzer_off"

class Wire(Component):
    def compute(self):
        self.output = self.input
    
    @property
    def texture(self) -> str:
        return "wire"


class CrossWire(Component):
    def compute(self):
        self.output = self.input

    def get_input_positions(self) -> List[tuple]:
        return [
            (self.pos_x, self.pos_y - 1), # W
            (self.pos_x - 1, self.pos_y), # A
            (self.pos_x, self.pos_y + 1), # S
            (self.pos_x + 1, self.pos_y)  # D
        ]

    def get_output_positions(self) -> List[tuple]:
        return [
            (self.pos_x, self.pos_y - 1),
            (self.pos_x, self.pos_y + 1),
            (self.pos_x - 1, self.pos_y),
            (self.pos_x + 1, self.pos_y)
        ]

    @property
    def texture(self) -> str:
        return "cross_wire"

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
        # reset board
        for comp in self.components:
            comp.input = 0
            comp.output = 0

        # since batteries create the signal we need to find every single instance of a battery on the grid
        batteries = [c for c in self.components if isinstance(c, Battery)]
        
        # store all components that are part of proper circuit
        powered_components = set()

        for battery in batteries:
            stack = [(battery, [battery])]
            
            while stack:
                current, path = stack.pop()
                
                # look at all components that it gives power to
                for target_pos in current.get_output_positions():
                    neighbor = self.grid.get(target_pos)
                    
                    if not neighbor:
                        continue
                        
                    if (current.pos_x, current.pos_y) not in neighbor.get_input_positions():
                        continue 
                            
                    if isinstance(neighbor, Switch) and not getattr(neighbor, "_Switch__toggle", False):
                        continue 
                            
                    if neighbor == battery and len(path) > 2:
                        for comp in path:
                            powered_components.add(comp)
                        continue 
                            
                    if neighbor not in path:
                        stack.append((neighbor, path + [neighbor]))

        # power components with proper signal
        for comp in self.components:
            if comp in powered_components:
                comp.input = 1
                comp.compute()
                # batteries output powerwires bulbs pass it along if in a loop
                if not isinstance(comp, Bulb): 
                    comp.output = 1