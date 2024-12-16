import pygame
import json

from src.globals import *
from src.utils import show_error

from src.states.menu import MenuState
from src.states.game import GameState


class Game:
    def __init__(self):
        pygame.init()
        
        self.TITLE = "Bastante Lutadores"
        pygame.display.set_caption(self.TITLE)
        
        self.FPS = 60
        self.clock = pygame.time.Clock()
        
        self.user_settings = self._import_user_settings()
        self.window_width = self.user_settings["Window Width"]
        self.window_height = self.user_settings["Window Height"]
        self.window = pygame.display.set_mode(size = (self.window_width, self.window_height))
        
        self.render_screen_width = 1280
        self.render_screen_height = 720
        self.render_screen_position = (0, 0)
        self.render_screen_color = (20, 20, 20)
        self.render_screen = pygame.Surface(size=(self.render_screen_width, self.render_screen_height)).convert() # .convert for performance
        self.render_screen_x_factor = self.render_screen_width / self.window_width
        self.render_screen_y_factor = self.render_screen_height / self.window_height
        
        self.current_state = MenuState(self.render_screen, self.window)
        self.next_state = None # will be returning from handle_logic
        
        self.is_game_running = True
        self.start_game_loop()
        
    
    def start_game_loop(self): #
        while self.is_game_running:
            self.handle_events()
            self.handle_states()
            self.handle_logic()
            self.handle_rendering()
            self.update_game()
        pygame.quit()
        
    def handle_events(self): #
        events = pygame.event.get()
        for event in events:
            self.current_state.handle_events(event=event)
            if event.type == pygame.QUIT:
                self.is_game_running = False
                
    def handle_states(self): #
        self.next_state = self.current_state.handle_states()
        if self.next_state == HOST_STATE:
            self.current_state = GameState(self.render_screen, hoststate="server")
        elif self.next_state == CLIENT_STATE:
            self.current_state = GameState(self.render_screen, hoststate="client")
        elif self.next_state == QUIT_STATE:
            self.is_game_running = False
                
    def handle_logic(self): #
        self.current_state.handle_logic()
    
    def handle_rendering(self): #
        render_screen_resized = pygame.transform.scale(surface=self.render_screen, size=(self.window_width, self.window_height))
        self.window.blit(source=render_screen_resized, dest=self.render_screen_position)
        self.render_screen.fill(self.render_screen_color)
        self.current_state.handle_rendering()
        
    def update_game(self):
        pygame.display.flip()
        self.clock.tick(self.FPS)
            
            
            
            
    def _import_user_settings(self) -> dict:
        USER_SETTINGS_PATH = "src/user_settings.json"
        READ_MODE = "r"
        data = {}
        try:
            with open(USER_SETTINGS_PATH, READ_MODE) as settings:
                data = json.load(settings)
            return data
        except:
            self.is_game_running = False
            show_error("user_settings.json is missing")
        
        
if __name__ == "__main__":
    game = Game()