import pygame
import json

from src.globals import *
from src.ui.gameUI import *
from src.network.server import Server

from src.entities.player import Player
from src.entities.tile import Tile

class GameState:
    def __init__(self, render_screen: pygame.Surface, hoststate="server"):
        self.hoststate = hoststate
        self.render_screen = render_screen
        self.render_screen_rect = self.render_screen.get_rect()
        self._load_background()
        self.tile_group = pygame.sprite.Group()
        self.map = self._load_map()
        self._draw_map()
        self.collisions = self._get_map_collisions()
        self.player = Player(self.render_screen, self.collisions)
        self.state = None
        self._connect_to_server()
        self.server_data = {}
        
        
        
    def handle_events(self, event):
        pass
            
            
            
    def handle_logic(self):
        self._send_for_server(self.player.data)
        self.server_data = eval(self._receive_from_server())
        self.player.handle_logic()
    
    
    
    def handle_states(self) -> str:
        return self.state
    
    
    
    def handle_rendering(self):
        self.render_screen.blit(source=self.background_image, dest=self.background_image_pos)
        self.tile_group.draw(self.render_screen)
        self._render_players()
    
    
    
    
    
    def _connect_to_server(self):
        self.server_bridge = Server()
        if self.hoststate == "server": self.server_bridge.start()
        self.client = self.server_bridge.connect()
        self.playerID = self._receive_from_server()
        
    
    def _receive_from_server(self):
        data = self.client.recv(1024).decode()
        return data
    
    
    def _send_for_server(self, data):
        data = str(data).encode()
        self.client.sendall(data)
        
    
    def _load_background(self):
        self.background_image_pos = (0, 0)
        self.background_image_path = "src/assets/bgimages/game_bg.png"
        self.background_image = pygame.image.load(self.background_image_path).convert()
        
        
    def _load_map(self):
        with open("src/assets/map.json", "r") as map_file:
            map = json.load(map_file)
        return map
    
    
    def _draw_map(self):
        for tile in self.map:
            tile = self.map[tile]
            tile = Tile(tile["x"], tile["y"], tile["size"], tile["size"], tile["sprite"])
            self.tile_group.add(tile)
            
            
    def _get_map_collisions(self):
        collision_map = []
        for tile in self.map:
            tile = self.map[tile]
            tile_pos = tile["x"], tile["y"]
            tile_size = tile["size"], tile["size"]
            tile_rect = pygame.Rect(tile_pos, tile_size)
            collision_map.append(tile_rect)
        return collision_map
    
    
    def _render_players(self):
        for player in self.server_data["Players"]:
            player = self.server_data["Players"][player]
            self._handle_with_player_sprites(player)
            
    def _handle_with_player_sprites(self, player):
        try:
            sprite_height_offset = 11
            sprite_y_offset = 8
            sprite_colorkey = (0, 255, 0)
            sprite = self.player.sprites[player["sprite"]]
            sprite = pygame.image.load(sprite).convert()
            sprite = pygame.transform.scale(sprite, (self.player.width, self.player.height + sprite_height_offset))
            sprite.set_colorkey(sprite_colorkey)
            if player["direction"] == "left":
                sprite = pygame.transform.flip(sprite, True, False)
            self.render_screen.blit(sprite, (player["x"], player["y"] - sprite_y_offset))
        except: pass