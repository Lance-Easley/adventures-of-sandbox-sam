import pygame
from pprint import pprint


class Player(object):
    def __init__(self, x, y, color, map_obj):
        self.width = 26
        self.x = x - self.width // 2
        self.height = 41
        self.y = y - self.height // 2
        self.color = color
        self.hitbox = pygame.Rect(self.x - 2, self.y - 2, self.width + 2, self.height + 2)
        self.x_coord = map_obj.x
        self.y_coord = map_obj.y

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x + 1, self.y + 1, self.width - 2, self.height - 2))
    
    def convert_to_data(self):
        return self.x_coord, self.y_coord, self.color


class Map(object):
    def __init__(self, world):
        self.x = 0
        self.y = 250
        self.width = 1600
        self.height = 1600
        self.x_vel = 5
        self.y_vel = 5
        self.world_data = []
        with open(f"{world}.txt") as world_f:
            for layer in world_f.readlines():
                layer_list = []
                for tile in layer:
                    if tile != "\n":
                        layer_list.append(tile)
                self.world_data.append(layer_list)
            

    def wall_objs(self):
        tile_rects = []
        y = 0
        for layer in self.world_data:
            x = 0
            for tile in layer:
                if tile != '0':
                    tile_rects.append(pygame.Rect(self.x + (x*16),self.y + (y*16),16,16))
                x += 1
            y += 1
        return tile_rects
    
    def draw_collision(self, window):
        for wall in self.wall_objs():
            pygame.draw.rect(window, (0,255,0), wall, 1)

if __name__ == "__main__":
    Map("world")