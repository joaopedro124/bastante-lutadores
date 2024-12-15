import pygame


class LevelEditor:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.FPS = 60
        pygame.display.set_caption("Level Editor")
        
        self.window_width = 1280
        self.window_height = 720
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        
        self.screen_pos = (0, 0)
        self.screen = pygame.Surface((self.window_width, self.window_height)).convert()
        self.screen_rect = self.screen.get_rect()
        self.background_color = (50, 50, 50)
        
        self.sprite1 = pygame.image.load("sprites/tile_ld.png").convert()
        self.sprite2 = pygame.image.load("sprites/tile_d.png").convert()
        self.sprite3 = pygame.image.load("sprites/tile_rd.png").convert()
        self.sprite4 = pygame.image.load("sprites/tile_l.png").convert()
        self.sprite5 = pygame.image.load("sprites/tile_c.png").convert()
        self.sprite6 = pygame.image.load("sprites/tile_r.png").convert()
        self.sprite7 = pygame.image.load("sprites/tile_lu.png").convert()
        self.sprite8 = pygame.image.load("sprites/tile_u.png").convert()
        self.sprite9 = pygame.image.load("sprites/tile_ru.png").convert()
        
        self.tile_size = 32
        self.all_rects = []
        self.selected_rects = {}
        self.current_button = 1
        self.current_sprite = self.sprite1
        
        self.click = False
        
    
    def handle_events(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            self._handle_keydown(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.click = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.click = False
        
    
    def handle_logic(self):
        self._highlight_rects()
        if self.click: self._get_select_rects()
        
    
    
    def handle_rendering(self):
        self.window.blit(self.screen, self.screen_pos)
        self.screen.fill(self.background_color)
        self._draw_lines()
        self._draw_sprites()
    
    
    def game_loop(self):
        self.running = True
        while self.running:
            events = pygame.event.get()
            for event in events: self.handle_events(event)
            self.handle_logic()
            self.handle_rendering()
            self._update_window()
        pygame.quit()
    
    
    
    def _update_window(self):
        pygame.display.flip()
        self.clock.tick(self.FPS)
        
        
    def _handle_keydown(self, event):
        if event.key == pygame.K_KP1:
            self.current_button = 1
        elif event.key == pygame.K_KP2:
            self.current_button = 2
        elif event.key == pygame.K_KP3:
            self.current_button = 3
        elif event.key == pygame.K_KP4:
            self.current_button = 4
        elif event.key == pygame.K_KP5:
            self.current_button = 5
        elif event.key == pygame.K_KP6:
            self.current_button = 6
        elif event.key == pygame.K_KP7:
            self.current_button = 7
        elif event.key == pygame.K_KP8:
            self.current_button = 8
        elif event.key == pygame.K_KP9:
            self.current_button = 9
            
        self.current_sprite = self._get_current_sprite()
        
        
    def _draw_lines(self):
        vertical_tiles_count = int(self.window.width / self.tile_size)
        horizontal_tiles_count = int(self.window.height / self.tile_size)
        
        for vertical_line in range(vertical_tiles_count):
            for horizontal_line in range(horizontal_tiles_count):
                
                line_color = (80, 80, 80)
                
                vertical_pos = vertical_line * self.tile_size
                vertical_start_pos = (vertical_pos, 0)
                vertical_end_pos = (vertical_line * self.tile_size, self.screen_rect.h)
                horizontal_pos = horizontal_line * self.tile_size
                horizontal_start_pos = (0, horizontal_pos)
                horizontal_end_pos = (self.screen_rect.w, horizontal_pos)
                
                pygame.draw.line(self.screen, line_color, vertical_start_pos, vertical_end_pos)
                pygame.draw.line(self.screen, line_color, horizontal_start_pos, horizontal_end_pos)
            
                rect = pygame.Rect(vertical_pos, horizontal_pos, self.tile_size, self.tile_size)
                if rect not in self.all_rects:
                    self.all_rects.append(rect)
                    
    
    def _get_current_sprite(self):
        match self.current_button:
            case 1: self.current_sprite = self.sprite1
            case 2: self.current_sprite = self.sprite2
            case 3: self.current_sprite = self.sprite3
            case 4: self.current_sprite = self.sprite4
            case 5: self.current_sprite = self.sprite5
            case 6: self.current_sprite = self.sprite6
            case 7: self.current_sprite = self.sprite7
            case 8: self.current_sprite = self.sprite8
            case 9: self.current_sprite = self.sprite9
        return self.current_sprite
                
                
    def _highlight_rects(self):
        for rect in self.all_rects:
            mouse = pygame.mouse.get_pos()
            if rect.collidepoint(mouse):
                resized_sprite = pygame.transform.scale(self.current_sprite, (self.tile_size, self.tile_size)).convert()
                colorkey = (0, 255, 0)
                resized_sprite.set_colorkey(colorkey)
                self.screen.blit(resized_sprite, (rect.x, rect.y))
                
        
    def _get_select_rects(self):
        mouse_pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        for rect in self.all_rects:
            if mouse_pressed[0]:
                if rect.collidepoint(mouse_pos):
                    self.selected_rects[self.all_rects.index(rect)] = {
                        "x": rect.x, 
                        "y": rect.y, 
                        "size": rect.width,
                        "sprite": self.current_button
                    }
            if mouse_pressed[2]:
                if rect.collidepoint(mouse_pos):
                    try:
                        del self.selected_rects[self.all_rects.index(rect)]
                    except:
                        pass
        print(self.selected_rects)
        
        
    def _draw_sprites(self):
        for sprite in self.selected_rects:
            sprite = self.selected_rects[sprite]
            sprite_image = eval(f"self.sprite{sprite["sprite"]}")
            sprite_pos = sprite["x"], sprite["y"]
            self.screen.blit(sprite_image, sprite_pos)
            



if __name__ == "__main__":
    leveleditor = LevelEditor()
    leveleditor.game_loop()