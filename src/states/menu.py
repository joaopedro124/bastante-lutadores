import pygame

from src.globals import *
from src.ui.menuUI import MenuUI

class MenuState:
    def __init__(self, render_screen: pygame.Surface):
        self.render_screen = render_screen
        self.render_screen_rect = self.render_screen.get_rect()
        self._load_background()
        
        self.MenuUI = MenuUI(render_screen=self.render_screen)
        self.ui_elements_group = pygame.sprite.Group()
        self._load_ui()
        self.state = None
        
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_buttons_click(event_pos=event.pos)
            
    def handle_logic(self):
        return 0
    
    def states_logic(self) -> str:
        return self.state
    
    def handle_rendering(self):
        self.render_screen.blit(source=self.background_image, dest=self.background_image_pos)
        self.ui_elements_group.update()
        
        
        
    def _load_background(self):
        self.background_image_pos = (0, 0)
        self.background_image_path = "src/assets/bgimages/menu_bg.png"
        self.background_image = pygame.image.load(self.background_image_path).convert()

    
    def _load_ui(self):
        self.ui_elements_group.add(
            self.MenuUI.start_host_button,
            self.MenuUI.enter_room_button,
            self.MenuUI.quit_button
        )
        
    def _handle_buttons_click(self, event_pos):
        if self.MenuUI.start_host_button.rect.collidepoint(event_pos):
            self.state = HOST_STATE
        elif self.MenuUI.quit_button.rect.collidepoint(event_pos):
            self.state = QUIT_STATE