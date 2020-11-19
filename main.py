import pygame
from classes import Player, Map
from pprint import pprint

pygame.init()

screen_x, screen_y = (1000,800)
display = pygame.display.set_mode((screen_x, screen_y))


def collide_check(rect, colls):
    collisions = []
    for wall in colls:
        if rect.colliderect(wall):
            collisions.append(world.wall_objs().index(wall))
    return collisions


def redrawGameWindow():
    world.draw_collision(display)
    p1.draw(display)
    pygame.display.update()


#mainloop
world = Map("world")
clock = pygame.time.Clock()
collision_tolerance = max(world.x_vel, world.y_vel) * 2 + 1
p1 = Player(screen_x // 2, screen_y // 2, (255,0,0), world)
gravity = 3
run = True
while run:
    clock.tick(60)

    display.fill((125,200,255))

    w_coll = True
    a_coll = True
    s_coll = True
    d_coll = True

    redrawGameWindow()
    # skeld.wall_objs()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    
    coll_index = collide_check(p1.hitbox, world.wall_objs())
    if coll_index != []:
        for i in coll_index:
            if abs(world.wall_objs()[i].bottom - p1.hitbox.top) < collision_tolerance:
                w_coll = False
            if abs(world.wall_objs()[i].right - p1.hitbox.left) < collision_tolerance:
                a_coll = False
            if abs(world.wall_objs()[i].top - p1.hitbox.bottom) < collision_tolerance:
                s_coll = False
            if abs(world.wall_objs()[i].left - p1.hitbox.right) < collision_tolerance:
                d_coll = False

    if gravity < 3:
        gravity += 0.2

    if keys[pygame.K_a]:
        if a_coll:
            world.x += world.x_vel
    if keys[pygame.K_d]:
        if d_coll:
            world.x -= world.x_vel
    if keys[pygame.K_SPACE]:
        if s_coll:
            gravity = -3
    if keys[pygame.K_c]:
        print(world.x, world.y)

    if s_coll:
        world.y -= gravity

    if keys[pygame.K_ESCAPE]:
        display = pygame.display.set_mode((screen_x, screen_y))
        run = False

pygame.quit()