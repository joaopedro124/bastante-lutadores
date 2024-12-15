import pygame

from src.globals import *
from src.ui.gameUI import *

class GameState:
    def __init__(self, render_screen: pygame.Surface):
        self.render_screen = render_screen
        self.render_screen_rect = self.render_screen.get_rect()
        self._load_background()
        self.map = self._load_map()
        
        self.state = None
        
    def handle_events(self, event):
        pass
            
    def handle_logic(self):
        pass
    
    def states_logic(self) -> str:
        return self.state
    
    def handle_rendering(self):
        self.render_screen.blit(source=self.background_image, dest=self.background_image_pos)
        self._draw_map()
    
    
    
    def _load_background(self):
        self.background_image_pos = (0, 0)
        self.background_image_path = "src/assets/bgimages/game_bg.png"
        self.background_image = pygame.image.load(self.background_image_path).convert()
        
    def _load_map(self):
        with open("src/assets/map.txt", "r") as map_file:
            map = eval(map_file.read())
        return map
    
    def _draw_map(self):
        tile_color = (26, 34, 43)
        for tile in self.map:
            pygame.draw.rect(self.render_screen, tile_color, tile)