import pygame
from pprint import pprint

with open("world.txt") as world_f:
    world_data = world_f.readlines()
    for index, line in enumerate(world_data):
        world_data[index] = line.strip('\n')
    pprint(world_data)

pygame.init()

screen_x, screen_y = (800,800)
display = pygame.display.set_mode((screen_x, screen_y))



run = True
while run:
    display.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
