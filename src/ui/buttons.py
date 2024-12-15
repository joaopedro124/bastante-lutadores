import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, xandy: tuple, wandh: tuple, image: pygame.Surface, screen: pygame.Surface):
        super().__init__()
        self.x, self.y = xandy
        self.width, self.height = wandh
        self.image = self.transform_image_size(image)
        self.screen = screen
        
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        
    def update(self):
        self.screen.blit(source=self.image, dest=self.rect)
        
    
    def transform_image_size(self, image):
        RGB_COLORKEY = (0, 255, 0)
        resized_image = pygame.transform.scale(image, size=(self.width, self.height))
        resized_image.set_colorkey(RGB_COLORKEY)
        return resized_image