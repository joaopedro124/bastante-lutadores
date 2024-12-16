import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, image):
        super().__init__()
        self.tile_sprites = {1: "src/assets/sprimages/tiles/tile_ld.png",
                             2: "src/assets/sprimages/tiles/tile_d.png",
                             3: "src/assets/sprimages/tiles/tile_rd.png",
                             4: "src/assets/sprimages/tiles/tile_l.png",
                             5: "src/assets/sprimages/tiles/tile_c.png",
                             6: "src/assets/sprimages/tiles/tile_r.png",
                             7: "src/assets/sprimages/tiles/tile_lu.png",
                             8: "src/assets/sprimages/tiles/tile_u.png",
                             9: "src/assets/sprimages/tiles/tile_ru.png"}
        
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = pygame.image.load(self.tile_sprites[image])
        self.image = pygame.transform.scale(self.image, (w, h)).convert()
        self.image_colorkey = (0, 255, 0)
        self.image.set_colorkey(self.image_colorkey)
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)