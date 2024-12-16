import pygame

class Player:
    def __init__(self, render_screen, rects_map):
        self.render_screen = render_screen
        self.render_screen_rect = self.render_screen.get_rect()
        self.rects_map = rects_map
        self.x = 60
        self.y = 60
        self.width = 42
        self.height = 42
        self.speed = 5
        self.x_acceleration = 5
        self.y_acceleration = 0
        self.gravity_acceleration = 1
        self.is_jumping = False
        self.is_rolling = False
        self.is_punching = False
        self.roll_count = 0
        self.roll_timer = 0
        self.punch_timer = 0
        self.punch_cooldown = False
        self.punch_cooldown_timer = 0
        self.sprite_direction = "right"
        self.sprites = {"idle": "src/assets/sprimages/player/idle.png",
                        "crouch": "src/assets/sprimages/player/crouch.png",
                        "jump": "src/assets/sprimages/player/jump.png",
                        "roll 1": "src/assets/sprimages/player/roll_1.png",
                        "roll 2": "src/assets/sprimages/player/roll_2.png",
                        "roll 3": "src/assets/sprimages/player/roll_3.png",
                        "roll 4": "src/assets/sprimages/player/roll_4.png",
                        "walking 1": "src/assets/sprimages/player/walking_1.png",
                        "walking 2": "src/assets/sprimages/player/walking_2.png",
                        "walking 3": "src/assets/sprimages/player/walking_3.png",
                        "walking 4": "src/assets/sprimages/player/walking_4.png",
                        "punch 1": "src/assets/sprimages/player/punch_1.png",
                        "punch 2": "src/assets/sprimages/player/punch_2.png",
                        "punch 3": "src/assets/sprimages/player/punch_3.png",
                        "punch 4": "src/assets/sprimages/player/punch_4.png",}
        self.sprite_animation_count = 0
        self.current_sprite = self.sprites["idle"]
        self.data = {}
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        
    def handle_logic(self):
        self.keys = pygame.key.get_pressed()
        self._handle_x_moviment()
        self._handle_y_moviment()
        self._roll_count_timer()
        
        if self.is_punching: self._punch_animation()
        if self.is_rolling: self._rolling_animation()
        else: self.speed = 5
        self._punch_animation_timer()
        self._punch_cooldown()
        self._handle_sprite_animations()
        self._update_data()
        # pygame.draw.rect(self.render_screen, (255, 0, 0), self.rect, 1)
        
        
    
    def _handle_x_moviment(self):
        if self.keys[pygame.K_a]:   self.x_acceleration = -self.speed
        elif self.keys[pygame.K_d]: self.x_acceleration = self.speed
        else:                       self.x_acceleration = 0
        self.rect.x += self.x_acceleration
        self._check_for_x_collisions()
        
    def _check_for_x_collisions(self):
        for tile in self.rects_map:
            if tile.colliderect(self.rect):
                if self.x_acceleration > 0:
                    self.rect.right = tile.left
                elif self.x_acceleration < 0:
                    self.rect.left = tile.right
                self.x_acceleration = 0
        
        
        
    def _handle_y_moviment(self):
        if self.keys[pygame.K_w] and not self.is_jumping: 
            self.y_acceleration = -15
            self.is_jumping = True
        self.y_acceleration += self.gravity_acceleration
        self.rect.y += self.y_acceleration
        self._check_for_y_collisions()
    
    def _check_for_y_collisions(self):
        for tile in self.rects_map:
            if tile.colliderect(self.rect):
                if self.y_acceleration > 0:
                    self.is_jumping = False
                    self.rect.bottom = tile.top
                elif self.y_acceleration < 0:
                    self.rect.top = tile.bottom
                self.y_acceleration = 0
        
    def _handle_sprite_animations(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_n] and not self.punch_cooldown: 
            self.is_punching = True
        elif not self.is_punching:
            if keys[pygame.K_s]:
                if keys[pygame.K_a] and self.roll_count < 4:
                    self.is_rolling = True
                    self.sprite_direction = "left"
                elif keys[pygame.K_d] and self.roll_count < 4:
                    self.is_rolling = True
                    self.sprite_direction = "right"
                else:
                    self.speed = 0
                    self.current_sprite = self.sprites["crouch"]
            elif self.is_jumping:
                self.current_sprite = self.sprites["jump"]
            elif keys[pygame.K_a]:
                self.speed = 5
                self._walking_animation()
                self.sprite_direction = "left"
            elif keys[pygame.K_d]:
                self.speed = 5
                self._walking_animation()
                self.sprite_direction = "right"
            elif keys[pygame.K_a] and keys[pygame.K_d]:
                self.current_sprite = self.sprites["idle"]
            else:
                self.current_sprite = self.sprites["idle"]
                self.sprite_animation_count = 0
                self.speed = 5
            
    def _walking_animation(self):
        match self.sprite_animation_count:
            case 0: self.current_sprite = self.sprites["walking 1"]
            case 10: self.current_sprite = self.sprites["walking 2"]
            case 20: self.current_sprite = self.sprites["walking 3"]
            case 30: self.current_sprite = self.sprites["walking 4"]
        if self.sprite_animation_count >= 30:
            self.sprite_animation_count = 0
        self.sprite_animation_count += 2.5
        
    def _rolling_animation(self):
        if self.is_rolling and self.roll_count < 3:
            self.speed = 8
            match self.sprite_animation_count:
                case 0: self.current_sprite = self.sprites["roll 1"]
                case 10: self.current_sprite = self.sprites["roll 2"]
                case 20: self.current_sprite = self.sprites["roll 3"]
                case 30: self.current_sprite = self.sprites["roll 4"]
            if self.sprite_animation_count >= 30:
                self.sprite_animation_count = 0
                self.roll_count += 1
            self.sprite_animation_count += 2
        else:
            self.is_rolling = False
            self.roll_count = 4
        
    def _roll_count_timer(self):
        if self.roll_count >= 4:
            self.roll_timer += 1
        if self.roll_timer > 100:
            self.roll_count = 0
            self.roll_timer = 0
            
    def _punch_animation(self):
        match self.sprite_animation_count:
            case 0: self.current_sprite = self.sprites["punch 1"]
            case 12: self.current_sprite = self.sprites["punch 2"]
            case 24: self.current_sprite = self.sprites["punch 3"]
            case 36: self.current_sprite = self.sprites["punch 4"]
        if self.sprite_animation_count >= 40:
            self.sprite_animation_count = 0
        self.sprite_animation_count += 3
        
    def _punch_animation_timer(self):
        if self.is_punching:
            self.punch_timer += 1
        if self.punch_timer >= 20:
            self.speed = 5
            self.is_punching = False
            self.punch_timer = 0
            self.punch_cooldown = True
            
    def _punch_cooldown(self):
        if self.punch_cooldown:
            self.punch_cooldown_timer += 1
        if self.punch_cooldown_timer >= 10:
            self.punch_cooldown_timer = 0
            self.punch_cooldown = False

    def _update_data(self):
        sprite_keys = list(self.sprites.keys())
        sprite_values = list(self.sprites.values())
        sprite_index = sprite_values.index(self.current_sprite)
        sprite = sprite_keys[sprite_index]
        self.data = {
            "x": self.rect.x,
            "y": self.rect.y,
            "sprite": sprite,
            "direction": self.sprite_direction,
        }