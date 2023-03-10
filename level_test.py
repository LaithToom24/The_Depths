import pygame
from Settings import *
from Level import Level
from SpriteSheet import *
from Player import Revised
from EnemyGenerator import EnemyGenerator
from Button import Button

pygame.init()

pygame.display.set_caption("The Depths")

clock = pygame.time.Clock()

tile_width, tile_height = 25, 25
tileset = Tileset(pygame.image.load("Enviroment/ground.png").convert_alpha(), tile_dimensions=(tile_width, tile_height))

def draw_grid():
    for i in range(int(SCREEN_WIDTH/tile_width)):
        pygame.draw.line(screen, (255, 255, 255), (i*tile_width, 0), (i*tile_width, SCREEN_HEIGHT))
    for i in range(int(SCREEN_HEIGHT/tile_height)):
        pygame.draw.line(screen, (255, 255, 255), (0, i*tile_height), (SCREEN_WIDTH, i*tile_height))

jump_frames_right = spritesheet(spritesheet=pygame.image.load("Mobs/Colour1/Outline/120x80_PNGSheets/_Jump.png").convert(), width=120, height=80, frames=3)
jump_frames_right = jump_frames_right.get_images()

jump_frames_left = [pygame.transform.flip(x, True, False) for x in jump_frames_right]

walking_animation_right = spritesheet(spritesheet=pygame.image.load("Mobs/Colour1/Outline/120x80_PNGSheets/_Run.png").convert(), width=120, height=80, frames=10)
walking_animation_right = walking_animation_right.get_images()

walking_animation_left = [pygame.transform.flip(x, True, False) for x in walking_animation_right]

idle_animation_right = spritesheet(spritesheet=pygame.image.load("Mobs/Colour1/Outline/120x80_PNGSheets/_Idle.png").convert(), width=120, height=80, frames=10)
idle_animation_right = idle_animation_right.get_images()

idle_animation_left = [pygame.transform.flip(x, True, False) for x in idle_animation_right]

fall_frames_right = spritesheet(spritesheet=pygame.image.load("Mobs/Colour1/Outline/120x80_PNGSheets/_Fall.png").convert(), width=120, height=80, frames=3)
fall_frames_right = fall_frames_right.get_images()

fall_frames_left = [pygame.transform.flip(x, True, False) for x in fall_frames_right]

attack_frames_right = spritesheet(spritesheet=pygame.image.load("Mobs/Colour1/Outline/120x80_PNGSheets/_AttackNoMovement.png").convert(), width=120, height=80, frames=4)
attack_frames_right = attack_frames_right.get_images()

attack_frames_left = [pygame.transform.flip(x, True, False) for x in attack_frames_right]

hit_frames_right = spritesheet(spritesheet=pygame.image.load("Mobs/Colour1/Outline/120x80_PNGSheets/_Hit.png").convert(), width=120, height=80, frames=1)
hit_frames_right = hit_frames_right.get_images()

hit_frames_left = [pygame.transform.flip(x, True, False) for x in hit_frames_right]

dying_frames_right = spritesheet(spritesheet=pygame.image.load("Mobs/Colour1/Outline/120x80_PNGSheets/_Death.png").convert(), width=120, height=80, frames=10)
dying_frames_right = dying_frames_right.get_images()

dying_frames_left = [pygame.transform.flip(x, True, False) for x in dying_frames_right]

background = pygame.Surface((64, 64))
background_img = pygame.image.load("Enviroment/walls_far.png").convert_alpha()
background.blit(background_img, (0, 0), ((310, 192), (64, 64)))

pillars = pygame.Surface((48, 128))
pillars_img = pygame.image.load("Enviroment/env_objects.png").convert_alpha()
pillars.blit(pillars_img, (0, 0), ((208, 0), (48, 128)))
pillars = pygame.transform.scale(pillars, (SCREEN_HEIGHT*2/3, SCREEN_HEIGHT*2))
pillars.set_colorkey((0, 0, 0))

level_map = [[0 for i in range(int(SCREEN_WIDTH/tile_width)*2)] for i in range(int(SCREEN_HEIGHT/tile_height)*2)]

for i in range(len(level_map[0])):
    level_map[0][i] = 3
    level_map[len(level_map)-1][i] = 3

for i in range(len(level_map)):
    level_map[i][0] = 3
    level_map[i][len(level_map[0])-1] = 3

row = 5
level_map[row][3] = 3
level_map[row][12] = 3

row = 8
for i in range(5, 10):
    level_map[row][i] = 1
level_map[row-1][8], level_map[row-1][9] = 1, 1
level_map[row-2][9] = 1

row = 12
for i in range(4, 5):
    level_map[row][i] = 1

for i in range(15, 16):
    level_map[i][20] = 3
    level_map[i][50] = 3

row = 16
for i in range(len(level_map[row])-3):
    if not(56 <= i < 61 or 80 <= i < 82 or 84 <= i < 86):
        level_map[row][i] = 1
level_map[row][len(level_map[row])-3] = 2

row = 23
for i in range(25, 35):
    level_map[row][i] = 3

row = 24
for i in range(len(level_map[row])-3):
    if not(14 <= i < 17 or 90 <= i < 93):
        level_map[row][i] = 1

level_map[row][len(level_map[row])-3] = 2

row = 40
for i in range(10, 50):
    level_map[row][i] = 1
for i in range(55, 70):
    level_map[row][i] = 1
for i in range(75, 100):
    level_map[row][i] = 1

row = 50
for i in range(0, 20):
    level_map[row][i] = 1
for i in range(26, 60):
    level_map[row][i] = 1
for i in range(65, 90):
    level_map[row][i] = 1

dont_check: list[bool] = []
def move_tiles(index: int, row: int, tiles: tuple[int], endpoints: tuple[int]):
    global timer, dont_check, shift_y
    player_on_tile = False
    if len(dont_check)-1 < index:
        for tile in tiles:
            level.moving_tiles[(row, tile)] = True
        dont_check.append(False)
    speed = -1
    if not(dont_check[index]) and level.hitboxes[(row, tiles[0])][0].top-1 < endpoints[0]:
        speed = 1
    elif level.hitboxes[(row, tiles[0])][0].bottom+1 > endpoints[1]:
        speed = -1
        dont_check[index] = True
    else:
        dont_check[index] = False
    for tile in tiles:
        level.hitboxes[(row, tile)][0].y += speed
        level.original_hitboxes[(row, tile)].y += speed
        if player.on_tile(level, row, tile):
            player_on_tile = True
    if player_on_tile and player.hitbox.center[1] > SCREEN_HEIGHT*0.45 and (speed < 0 and player.hitbox.center[1] < SCREEN_HEIGHT*0.6 or speed > 0 and player.hitbox.center[1]-5 < SCREEN_HEIGHT*0.6) and -SCREEN_HEIGHT <= shift_y-speed <= 0:
        shift_y -= speed

def convert_map(array: list[list[int]]):
    for row in array:
        for num in row:
            if num == 1:
                array[array.index(row)][row.index(num)] = tileset.get_tile(pos=(195, 10), dimensions=[15, 30], tile_type=1)
            elif num == 2:
                x = row.index(num)
                for i in range(3):
                    array[array.index(row)][x+i] = tileset.get_tile(pos=(195+30*i, 10), dimensions=[20, 20], tile_type=1)
            elif num == 3:
                array[array.index(row)][row.index(num)] = tileset.get_tile(pos=(50, 160), dimensions=(20, 15), tile_type=0)
    return array

level_map = convert_map(level_map)

tile_types = [
             [0, 0]
,            [0, 5]
             ]

level = Level(mapped_tiles=level_map, name="Catacombs", tile_types=tile_types)

player = Revised(
        velocity=[3, 4],
        framesUP = None,
        framesDOWN = None,
        framesLEFT = walking_animation_left,
        framesRIGHT = walking_animation_right,
        framesIDLE_r = idle_animation_right,
        framesIDLE_l = idle_animation_left,
        framesJUMP_l=jump_frames_left,
        framesJUMP_r=jump_frames_right,
        framesFALL_l=fall_frames_left,
        framesFALL_r=fall_frames_right,
        framesATTACK_l=attack_frames_left,
        framesATTACK_r=attack_frames_right,
        framesHIT_l=hit_frames_left,
        framesHIT_r=hit_frames_right,
        framesDYING_l=dying_frames_left,
        framesDYING_r=dying_frames_right,
        width=35,
        height=80,
        starting_pos=(0, 10*tile_height),
        offset_x = 42.5, offset_y = 40,
        offset_width = -11,
        offset_height = -40
        )

generator = EnemyGenerator(limit=20, pos=(30*tile_width, 10*tile_height))

def pause_game(self):
    global pause
    if self.clicked:
        pause = not(pause)

pause_button_icon = pygame.Surface((33, 31))
pause_button_icon.blit(pygame.image.load("Icons/pixil-layer-1.png").convert_alpha(), (0, 0), (33*1, 33*5, 33, 31))
pause_button_icon.set_colorkey((0, 0, 0))
pause_button_icon_hover = pygame.Surface((33, 31))
pause_button_icon_hover.blit(pygame.image.load("Icons/Golden.png").convert_alpha(), (0, 0), (33*1, 33*5, 33, 31))
pause_button_icon_hover.set_colorkey((0, 0, 0))
pause_button = Button(icon_hover=pause_button_icon_hover, icon=pause_button_icon, width=33, height=31, pos=(SCREEN_WIDTH-33, 0), action=pause_game)
pause_screen = font_1.render("Paused", 1, (255, 255, 255))
pause_screen_size = font_1.size("Paused")

title = title_font.render("The Depths", 1, (255, 255, 255))
title_size = title_font.size("The Depths")

def start_game(self):
    global start_screen, pause
    if self.clicked:
        start_screen = False
        pause = False

start_button_text = font_2.render("New Game", 1, (255, 255, 255))
start_button_text_size = font_2.size("New Game")
start_button_icon = pygame.Surface(start_button_text_size)
start_button_icon.blit(start_button_text, (0, 0))
start_button_icon_hover = pygame.Surface(start_button_text_size)
pygame.draw.rect(start_button_icon_hover, rect=((0, 0), start_button_text_size), color=(50, 50, 50))
start_button_icon_hover.blit(start_button_text, (0, 0))
start_button = Button(icon_hover=start_button_icon_hover, icon=start_button_icon, width=start_button_text_size[0], height=start_button_text_size[1], pos=((SCREEN_WIDTH-start_button_text_size[0])/2, 100), action=start_game)

run = True
pause = False
start_screen = True
shift_x, shift_y = 0, 0
while run:
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                run = False

    if start_screen:
        screen.blit(title, ((SCREEN_WIDTH-title_size[0])/2, 50))
        start_button.main()
    elif not(pause):
        for x in range(int(SCREEN_HEIGHT/64)*2+2):
            for i in range(2*int(SCREEN_WIDTH/64)+2):
                screen.blit(background, (64*i+shift_x, 64*x+shift_y))

        for i in range(0, int(SCREEN_WIDTH/5), 2):
            screen.blit(pillars, ((SCREEN_WIDTH/5)*i+shift_x, shift_y))

        keys = pygame.key.get_pressed()

        if SCREEN_WIDTH*0.5 <= player.hitbox.center[0] <= SCREEN_WIDTH*0.6:
            player.scrolling_x = not(shift_x+player.velocity[0] >= 0 or shift_x-player.velocity[0] <= -SCREEN_WIDTH)
            if not(player.attacking):
                if not(player.detect_right_collision(level)) and keys[pygame.K_RIGHT] and shift_x-player.velocity[0] >= -SCREEN_WIDTH:
                    shift_x -= player.velocity[0]
                elif not(player.detect_left_collision(level)) and (keys[pygame.K_LEFT]) and shift_x+player.velocity[0] <= 0:
                    shift_x += player.velocity[0]
        else:
            player.scrolling_x = False

        if SCREEN_HEIGHT*0.5 <= player.hitbox.center[1] <= SCREEN_HEIGHT*0.6:
            player.scrolling_y = not(shift_y >= 0 or shift_y <= -SCREEN_HEIGHT)
            if player.falling:
                if shift_y-player.falling_momentum >= -SCREEN_HEIGHT:
                    shift_y -= player.falling_momentum
                else:
                    shift_y = -SCREEN_HEIGHT
            elif player.jumping:
                if shift_y+player.jumping_momentum <= 0:
                    shift_y += player.jumping_momentum
                else:
                    shift_y = 0
        else:
            player.scrolling_y = False

        move_tiles(0, 16, [i for i in range(14, 17)], (24*tile_height+5+shift_y, 17*tile_height+shift_y))
        move_tiles(1, 40, [i for i in range(20, 25)], (55*tile_height+5+shift_y, 35*tile_height+shift_y))

        level.update_hitboxes(shift_x, shift_y)

        level.render(draw_hitboxes=False)
        # draw_hitboxes()
        player.main(level, shift_x, shift_y, right=keys[pygame.K_RIGHT], left=keys[pygame.K_LEFT], jump=keys[pygame.K_SPACE], attack=keys[pygame.K_a], fire=keys[pygame.K_1], enemy_dict=generator.enemies)

        generator.main(level, shift_x, shift_y, player)

        player.render_hud()
        if player.dead:
            shift_x = 0
            shift_y = 0
        elif keys[pygame.K_d]:
            shift_x = 0
            shift_y = 0
            player.die()
    else:
        player.fell_at_time = pygame.time.get_ticks()
        for key in generator.enemies.keys():
            if generator.enemies[key] != 0:
                generator.enemies[key].fell_at_time = pygame.time.get_ticks()
        screen.blit(pause_screen, ((SCREEN_WIDTH-pause_screen_size[0])/2, (SCREEN_HEIGHT-pause_screen_size[1])/2))

    if not(start_screen):
        pause_button.main()

    pygame.display.flip()

    clock.tick(60)

    # print(round(clock.get_fps()))

pygame.quit()
