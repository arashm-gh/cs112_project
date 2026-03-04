import sys, os
from typing import List
from enum import Enum
import pygame as pg
from components import *

class GameState(Enum):
    LOAD_ASSETS = 1
    PLACEMENT = 2
    RUN = 3
    QUIT = 4

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((1920, 1080))
        pg.display.set_caption("Digital Circuit Simulator")
        self.__running = True
        self.gs : GameState = GameState.LOAD_ASSETS
        self.__clock = pg.time.Clock()
        self.cell_size = 64
        self.grid_width = 26   # number of columns
        self.grid_height = 14  # number of rows
        self.offset_x = 64
        self.offset_y = 64
        self.circuit = Circuit([])
        self.assets = None
        self.tools = [
            ("Battery", Battery, "battery"),
            ("Switch", Switch, "switch_off"),   # we'll update texture based on state
            ("Wire", Wire, "wire"),              # you may need a wire.png
            ("Bulb", Bulb, "bulb_off"),
        ]
        self.selected_tool_index = 0
        self.tool_rects = []              # will be filled each frame

    def run(self):
        while self.__running:
            self._game_input()
            self._update()
            self._draw()
            self.__clock.tick(60)
        pg.quit()
        sys.exit(0) # applications quit with different "error codes" - a 0 means everything went well and there were no errors

    def _update(self): # python technically doesn't have private methods so we're just gonna not use this outside of the class
        match self.gs:
            case GameState.LOAD_ASSETS:
                self.assets = {}
                assets_path = os.path.join("assets", "textures")
                for filename in os.listdir(assets_path):
                    if filename.endswith(".png"):
                        name = os.path.splitext(filename)[0]
                        full_path = os.path.join(assets_path, filename)
                        try:
                            image = pg.image.load(full_path).convert_alpha()
                            image = pg.transform.scale(image, (self.cell_size, self.cell_size))
                            self.assets[name] = image
                        except pg.error as e:
                            print(f"Could not load {filename}: {e}")
                self.gs = GameState.PLACEMENT
            case GameState.PLACEMENT:
                pass
            case GameState.RUN:
                pass
            case GameState.QUIT:
                self.__running = False
    def _draw(self):
        self.screen.fill((100, 100, 100))

        for x in range(self.grid_width):
            for y in range(self.grid_height):
                rect = pg.Rect(self.offset_x + x * self.cell_size, self.offset_y + y * self.cell_size, self.cell_size, self.cell_size)
                pg.draw.rect(self.screen, (120, 120, 120), rect, 1)

        for comp in self.circuit.components:
            x = self.offset_x + comp.pos_x * self.cell_size
            y = self.offset_y + comp.pos_y * self.cell_size

            img = self.assets.get(comp.texture)
            if img:
                self.screen.blit(img, (x,y))
            else: # fallback if no texture is found
                color = (0, 255, 0) if comp.output else (255, 0, 0)
                pg.draw.rect(self.screen, color, (x, y + self.cell_size // 4, self.cell_size, self.cell_size // 2))
            # Optionally draw pins
            pg.draw.circle(self.screen, (255,255,255), (x, y+self.cell_size//2), 3)  # input pin (left)
            pg.draw.circle(self.screen, (255,255,255), (x+self.cell_size, y+self.cell_size//2), 3) # output pin (right)

        self._draw_toolbar()
        pg.display.flip()

    def _game_input(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.gs = GameState.QUIT
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    print("Input")
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # check toolbar first
                    for rect, idx in self.tool_rects:
                        if rect.collidepoint(event.pos):
                            self.selected_tool_index = idx
                            return   # don't also place a component

                    # then grid
                    mx, my = event.pos
                    gx = (mx - self.offset_x) // self.cell_size
                    gy = (my - self.offset_y) // self.cell_size
                    if 0 <= gx < self.grid_width and 0 <= gy < self.grid_height:
                        # check if cell already occupied
                        existing = self.circuit.get_component_at(gx, gy)
                        if existing:
                            # if it's a switch, toggle it
                            if isinstance(existing, Switch):
                                existing.toggle()
                                self.circuit.simulate()
                        else:
                            # place new component
                            self.circuit.add_component(
                                self.tools[self.selected_tool_index][1](gx, gy, 0)
                            ) # basically, chose the class in the tools array and place it at position gx and gy with rotation of 0
                            self.circuit.simulate()
                elif event.button == 3: # remove component with right click
                    mx, my = event.pos
                    gx = (mx - self.offset_x) // self.cell_size
                    gy = (my - self.offset_y) // self.cell_size
                    if 0 <= gx < self.grid_width and 0 <= gy < self.grid_height:
                        # check if cell already occupied
                        existing = self.circuit.get_component_at(gx, gy)
                        if existing: 
                            self.circuit.remove_component(existing)
                            self.circuit.simulate()                            
    
    def _draw_toolbar(self):
        x, y = 10, 10
        w, h = 80, 30
        self.tool_rects.clear()
        for i, (name, comp_class, tex) in enumerate(self.tools):
            rect = pg.Rect(x, y, w, h)
            color = (200, 200, 200) if i == self.selected_tool_index else (150, 150, 150)
            pg.draw.rect(self.screen, color, rect)
            pg.draw.rect(self.screen, (0,0,0), rect, 2)
            font = pg.font.Font(None, 24)
            text = font.render(name, True, (0,0,0))
            self.screen.blit(text, (x+5, y+5))
            self.tool_rects.append((rect, i))   # store index for later
            x += w + 5