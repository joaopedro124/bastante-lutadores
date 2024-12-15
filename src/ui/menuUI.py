import pygame

from src.ui.buttons import Button

class MenuUI:
    def __init__(self, render_screen: pygame.Surface):
        self.render_screen = render_screen
        self.render_screen_rect = render_screen.get_rect()
        
        self.start_host_button_pos = self.render_screen_rect.center
        self.start_host_button_size = (180, 60)
        self.start_host_button_image = pygame.image.load("src/assets/uiimages/host_button.png")
        self.start_host_button = Button(
            xandy=self.start_host_button_pos, wandh=self.start_host_button_size, 
            image=self.start_host_button_image, screen=self.render_screen
        )
        
        self.enter_room_button_pos = self.render_screen_rect.centerx, self.render_screen_rect.centery + 100
        self.enter_room_button_size = (180, 60)
        self.enter_room_button_image = pygame.image.load("src/assets/uiimages/enter_button.png")
        self.enter_room_button = Button(
            xandy=self.enter_room_button_pos, wandh=self.enter_room_button_size, 
            image=self.enter_room_button_image, screen=self.render_screen
        )
        
        self.quit_button_pos = self.render_screen_rect.centerx, self.render_screen_rect.centery + 200
        self.quit_button_size = (180, 60)
        self.quit_button_image = pygame.image.load("src/assets/uiimages/quit_button.png")
        self.quit_button = Button(
            xandy=self.quit_button_pos, wandh=self.quit_button_size, 
            image=self.quit_button_image, screen=self.render_screen
        )