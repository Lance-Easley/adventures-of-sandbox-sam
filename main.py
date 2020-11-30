import pygame
from classes import Player, Map
from pprint import pprint

pygame.init()

WINDOW_SIZE = (1000,600)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window
display = pygame.Surface((500,300)) # used as the surface for rendering, which is scaled

font = pygame.font.SysFont('Calibri', 16)
moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0
can_jump = False

true_scroll = [0,0]

def load_map(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


global animation_frames
animation_frames = {}

def load_animation(path,frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 1
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.jpg'
        # player_animations/idle/idle_0.png
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((255,255,255))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def change_action(action_var,frame,new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var,frame
        

animation_database = {}

animation_database['run'] = load_animation('player/run',[7,7,7,7,7,7])
animation_database['idle'] = load_animation('player/idle',[70,15,70,15])


game_map = load_map('world')

grass_img = pygame.image.load('items/grass.jpg')
dirt_img = pygame.image.load('items/dirt.jpg')
stone_img = pygame.image.load('items/stone.jpg')
coal_img = pygame.image.load('items/coal.jpg')
iron_img = pygame.image.load('items/iron.jpg')
ruby_img = pygame.image.load('items/ruby.jpg')
uranium_img = pygame.image.load('items/uranium.jpg')
diamond_img = pygame.image.load('items/diamond.jpg')


mining_img = pygame.image.load('items/pickaxe.jpg').convert()
mining_img.set_colorkey((255,255,255))

building_img = pygame.image.load('items/place.jpg').convert()
building_img.set_colorkey((255,255,255))

inv_img = pygame.image.load('inventory/inventory.jpg').convert()
inv_img.set_colorkey((255,255,255))

inv_select = pygame.image.load('inventory/select.jpg').convert()
inv_select.set_colorkey((255,255,255))


player_action = 'idle'
player_frame = 0
player_flip = False


player_rect = pygame.Rect(0,100,12,30)

def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

blocks = {'grass': 0, 'dirt': 0, 'stone': 0, 'coal': 0, 'iron': 0, 'ruby': 0, 'uranium': 0, 'diamond': 0, 'wood': 0}
hotbar = {'s1': None, 's2': None, 's3': None, 's4': None, 's5': None, 's6': None, 's7': None, 's8': None, 's9': None}
hb_positions = {'s1': 166, 's2': 186, 's3': 206, 's4': 226, 's5': 246, 's6': 266, 's7': 286, 's8': 306, 's9': 326}
block_choice = '0'

clock = pygame.time.Clock()
is_building = False
run = True
while run: # game loop
    display.fill((146,244,255)) # clear screen by filling it with blue (146,244,255)

    pos = pygame.mouse.get_pos()
    m_x = pos[0] / 32 + (true_scroll[0] / 16)
    m_y = pos[1] / 32 + (true_scroll[1] / 16)
    player_rel_x = (pos[0] - (WINDOW_SIZE[0] // 2 + 24))
    player_rel_y = (pos[1] - (WINDOW_SIZE[1] // 2 - 20))
    # print(player_rel_x, player_rel_y)

    true_scroll[0] += (player_rect.x-true_scroll[0]-(WINDOW_SIZE[0] // 4 + 6))/10
    true_scroll[1] += (player_rect.y-true_scroll[1]-(WINDOW_SIZE[1] // 4 - 15))/10
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(grass_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile == '2':
                display.blit(dirt_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile == '3':
                display.blit(stone_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile == '4':
                display.blit(coal_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile == '5':
                display.blit(iron_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile == '6':
                display.blit(ruby_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile == '7':
                display.blit(uranium_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile == '8':
                display.blit(diamond_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x*16,y*16,16,16))
            x += 1
        y += 1
    
    if is_building:
        display.blit(building_img,((pos[0] // 2 + 10, pos[1] // 2 + 10)))
    if not is_building:
        display.blit(mining_img,((pos[0] // 2 + 10, pos[1] // 2 + 10)))

    # slot1_text = font.render(f"{blocks['1'][1]}", True, (255,255,0))
    # slot1_textRect = slot1_text.get_rect()
    # slot1_textRect.topleft = (472, 508)

    # slot2_text = font.render(f"{blocks['2'][1]}", True, (255,255,0))
    # slot2_textRect = slot2_text.get_rect()
    # slot2_textRect.topleft = (512, 508)

    # slot3_text = font.render(f"{blocks['3'][1]}", True, (255,255,0))
    # slot3_textRect = slot3_text.get_rect()
    # slot3_textRect.topleft = (552, 508)

    # slot4_text = font.render(f"{blocks['4'][1]}", True, (255,255,0))
    # slot4_textRect = slot4_text.get_rect()
    # slot4_textRect.topleft = (592, 508)

    # slot5_text = font.render(f"{blocks['5'][1]}", True, (255,255,0))
    # slot5_textRect = slot5_text.get_rect()
    # slot5_textRect.topleft = (642, 508)

    # slot6_text = font.render(f"{blocks['6'][1]}", True, (255,255,0))
    # slot6_textRect = slot6_text.get_rect()
    # slot6_textRect.topleft = (692, 508)

    # slot7_text = font.render(f"{blocks['7'][1]}", True, (255,255,0))
    # slot7_textRect = slot7_text.get_rect()
    # slot7_textRect.topleft = (742, 508)

    # slot8_text = font.render(f"{blocks['8'][1]}", True, (255,255,0))
    # slot8_textRect = slot8_text.get_rect()
    # slot8_textRect.topleft = (792, 508)

    # slot9_text = font.render(f"{blocks['9'][1]}", True, (255,255,0))
    # slot9_textRect = slot9_text.get_rect()
    # slot9_textRect.topleft = (792, 508) # add 40 to x value for each new block

    display.blit(inv_img,((WINDOW_SIZE[0] // 4 - 88, 250))) # hotbar

    for key, value in hotbar.items():
        if 'grass' == value:
            display.blit(grass_img,((hb_positions[key], 254)))
        if 'dirt' == value:
            display.blit(dirt_img,((hb_positions[key], 254)))
        if 'stone' == value:
            display.blit(stone_img,((hb_positions[key], 254)))
        if 'coal' == value:
            display.blit(coal_img,((hb_positions[key], 254)))
        if 'iron' == value:
            display.blit(iron_img,((hb_positions[key], 254)))
        if 'ruby' == value:
            display.blit(ruby_img,((hb_positions[key], 254)))
        if 'uranium' == value:
            display.blit(uranium_img,((hb_positions[key], 254)))
        if 'diamond' == value:
            display.blit(diamond_img,((hb_positions[key], 254)))
    
    # display.blit(grass_img,((186, 254)))
    # display.blit(dirt_img,((206, 254)))
    # display.blit(stone_img,((226, 254)))
    # display.blit(coal_img,((246, 254)))
    # display.blit(iron_img,((266, 254)))
    # display.blit(ruby_img,((286, 254)))
    # display.blit(uranium_img,((306, 254)))
    # display.blit(diamond_img,((326, 254)))

    if block_choice == '1':
        display.blit(inv_select,((163, 251)))
    elif block_choice == '2':
        display.blit(inv_select,((183, 251)))
    elif block_choice == '3':
        display.blit(inv_select,((203, 251)))
    elif block_choice == '4':
        display.blit(inv_select,((223, 251)))
    elif block_choice == '5':
        display.blit(inv_select,((243, 251)))
    elif block_choice == '6':
        display.blit(inv_select,((263, 251)))
    elif block_choice == '7':
        display.blit(inv_select,((283, 251)))
    elif block_choice == '8':
        display.blit(inv_select,((303, 251)))
    elif block_choice == '9':
        display.blit(inv_select,((323, 251)))


    player_movement = [0,0]
    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 5:
        vertical_momentum = 5


    if player_movement[0] == 0:
        player_action,player_frame = change_action(player_action,player_frame,'idle')
    if player_movement[0] > 0:
        player_flip = False
        player_action,player_frame = change_action(player_action,player_frame,'run')
    if player_movement[0] < 0:
        player_flip = True
        player_action,player_frame = change_action(player_action,player_frame,'run')


    player_rect,collisions = move(player_rect,player_movement,tile_rects)
    # print(player_rect.x, player_rect.y)

    if collisions['bottom'] == True:
        vertical_momentum = 0
        can_jump = True
    if collisions['top'] == True:
        vertical_momentum = 0


    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 1
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    display.blit(pygame.transform.flip(player_img,player_flip,False),(player_rect.x-scroll[0],player_rect.y-scroll[1]))


    for event in pygame.event.get(): # event loop
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_SPACE:
                if air_timer < 6 and can_jump:
                    vertical_momentum = -3.2
                    can_jump = False
            if event.key == pygame.K_e:
                is_building = not is_building
            if event.key == pygame.K_1:
                block_choice = '1'
                is_building = True
            if event.key == pygame.K_2:
                block_choice = '2'
                is_building = True
            if event.key == pygame.K_3:
                block_choice = '3'
                is_building = True
            if event.key == pygame.K_4:
                block_choice = '4'
                is_building = True
            if event.key == pygame.K_5:
                block_choice = '5'
                is_building = True
            if event.key == pygame.K_6:
                block_choice = '6'
                is_building = True
            if event.key == pygame.K_7:
                block_choice = '7'
                is_building = True
            if event.key == pygame.K_8:
                block_choice = '8'
                is_building = True
            if event.key == pygame.K_9:
                block_choice = '9'
                is_building = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_a:
                moving_left = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            y = 0
            for layer in game_map:
                x = 0
                for index, tile in enumerate(layer):
                    if int((abs(player_rel_x) ** 2 + abs(player_rel_y) ** 2) ** 0.5) <= 150:
                        if not is_building:
                            if tile != '0':
                                if (m_x > x and m_x < x + 1) and (m_y > y and m_y < y + 1):
                                    block = game_map[game_map.index(layer)][index]
                                    if block == '1':
                                        blocks['grass'] += 1
                                    elif block == '2':
                                        blocks['dirt'] += 1
                                    elif block == '3':
                                        blocks['stone'] += 1
                                    elif block == '4':
                                        blocks['coal'] += 1
                                    elif block == '5':
                                        blocks['iron'] += 1
                                    elif block == '6':
                                        blocks['ruby'] += 1
                                    elif block == '7':
                                        blocks['uranium'] += 1
                                    elif block == '8':
                                        blocks['diamond'] += 1
                                    elif block == '9':
                                        blocks['wood'] += 1
                                    game_map[game_map.index(layer)][index] = '0'
                        else:
                            if tile == '0':
                                if (m_x > x and m_x < x + 1) and (m_y > y and m_y < y + 1):
                                    if block_choice != '0' and blocks[block_choice] > 0:
                                        game_map[game_map.index(layer)][index] = block_choice
                                        if block_choice == '1':
                                            blocks['1'] -= 1
                                        elif block_choice == '2':
                                            blocks['2'] -= 1
                                        elif block_choice == '3':
                                            blocks['3'] -= 1
                                        elif block_choice == '4':
                                            blocks['4'] -= 1
                                        elif block_choice == '5':
                                            blocks['5'] -= 1
                                        elif block_choice == '6':
                                            blocks['6'] -= 1
                                        elif block_choice == '7':
                                            blocks['7'] -= 1
                                        elif block_choice == '8':
                                            blocks['8'] -= 1
                                        elif block_choice == '9':
                                            blocks['9'] -= 1
                        x += 1
                y += 1
    
    # print(int((abs(player_rel_x) ** 2 + abs(player_rel_y) ** 2) ** 0.5))

    for key in blocks:
        if blocks[key] > 0 and key not in hotbar.values():
            for h_key, value in hotbar.items():
                if value == None:
                    hotbar[h_key] = key
                    break
        elif blocks[key] == 0 and blocks[key] in hotbar.values():
            for h_key, value in hotbar.items():
                if value == blocks[key]:
                    hotbar[h_key] = None
    
    print(hotbar)

    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))

    # screen.blit(grass_text, grass_textRect)
    # screen.blit(dirt_text, dirt_textRect)
    # screen.blit(stone_text, stone_textRect)
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()