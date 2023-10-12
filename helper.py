import os
from typing import List #, Dict, Type

import pygame
import random
from screeninfo import get_monitors, Monitor

from const import COLORS, WS_RESOLUTIONS
from data import Enemy, Medkit, Player, StaticObject, WeaponShell


def get_screen_res():
    monitors: List[Monitor] = get_monitors()
    width, height = monitors[0].width, monitors[0].height
    display: int = 0
    final_resolution = None
    for i in range(len(monitors)):
        if monitors[i].is_primary == True:
            width = monitors[i].width
            height = monitors[i].height
            display = i
    baseheight = width / 16 * 9
    if height <= baseheight: # 16:9 monitor or less (4:3)
        # height is max
        for res in WS_RESOLUTIONS:
            if WS_RESOLUTIONS[res][1] <= height:
                final_resolution = res
                break
    else: # superwide
        # width is max
        for res in WS_RESOLUTIONS:
            if WS_RESOLUTIONS[res][0] <= width:
                final_resolution = res
                break
    if not final_resolution:
        final_resolution = '1280x720 (HD)'
    # print('DEBUG', final_resolution)
    return WS_RESOLUTIONS[final_resolution], display, final_resolution


def game_init():
    ((screen_width, screen_height), display, final_res) = get_screen_res()
    pygame.font.init() # maybe pygame.init?
    global game_data
    pygame.display.set_caption('Space Arcade')

    game_data = {
        'resolution': WS_RESOLUTIONS[final_res],
        # 'music': False,
        # 'sounds': False,
        'FPS': 60,
        'width': screen_width,
        'height': screen_height,
        'display': display,
        'WINDOW': pygame.display.set_mode((screen_width, screen_height)),
        'BG': pygame.transform.scale(pygame.image.load(os.path.join('assets', 'space_bg.webp')), (screen_width, screen_height)),
        'MENU_BG': pygame.transform.scale(pygame.image.load(os.path.join('assets', 'main_menu.webp')), (screen_width, screen_height))

    }
    return game_data

def game_session_init():
    session_data = {
        'score': 0,
        'enemies': [],
        'weapon_shells': [],
        'static_objects': [],
        'level': 0,
        'lives': 5,
        'wave_length': 5,
        'enemy_vel': 1,
        'player_vel': game_data['width'] // 320, # 5 in 1600*900
        'laser_vel': 5,
        'laser_damage': 10,
        'static_vel': 2,
        'screen_height': game_data['height']
    }

    return session_data

def get_horizontal_center_position(obj):
    global game_data
    return game_data['width'] / 2 - obj.get_width() / 2

def get_vertical_center_position(obj):
    return game_data['height'] / 2 - obj.get_height() / 2

def get_middle_position(obj):
    return (get_horizontal_center_position(obj),
            get_vertical_center_position(obj))

def paused():
    global game_data
    pause: bool = True
    pause_font = pygame.font.SysFont('comicsans', 70)

    while pause:
        pause_label = pause_font.render('Pause. Press any key to continue', 1, COLORS['violet'])
        game_data['WINDOW'].blit(pause_label, get_middle_position(pause_label))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                pause = False

def escape_game():
    global game_data
    pause: bool = True
    escape_font = pygame.font.SysFont('comicsans', 70)

    while pause:
        pause_label_first = escape_font.render('Are you going to leave game?', 1, COLORS['violet'])
        pause_label_second = escape_font.render('Press Enter to end the game or ESC to return', 1, COLORS['violet'])
        game_data['WINDOW'].blit(pause_label_first, (get_horizontal_center_position(pause_label_first), game_data['height']/2 - pause_label_first.get_height())) # was HEIGHT
        game_data['WINDOW'].blit(pause_label_second, (get_horizontal_center_position(pause_label_second), game_data['height']/2 + pause_label_first.get_height())) # was WIDTH
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = False
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    pygame.quit()
                    quit()


def generate_enemies(session_data):
    session_data['level'] += 1
    session_data['wave_length'] += 5 # add 5 more enemies each level
    for _ in range(session_data['wave_length']):
        enemy = Enemy(random.randrange(50, game_data['width'] - 100),
                        random.randrange(-1500, -100), # -1500*level/5
                        session_data,
                        random.choice(['red', 'blue', 'green']))
        session_data['enemies'].append(enemy)


def enemies_movement(session_data, player: Player): # possible to remove player if move collide inside Space object class
    enemy: Enemy
    for enemy in session_data['enemies'][:]:
        if enemy.is_dead():
            session_data['enemies'].remove(enemy)
            session_data['score'] += 1
            continue
        enemy.move(session_data['enemy_vel'])
        enemy.cooldown() # refresh cooldown to shoot

        if (enemy.y <= game_data['height'] * 0.7 and
            random.randrange(0, 2*game_data['FPS']) == 1): # each ~ 2 sec
            enemy.shoot()

        if enemy.collide(player):
            player.health -= 10
            session_data['score'] += 1
            session_data['enemies'].remove(enemy)
        elif enemy.y + enemy.get_height() > game_data['height']:
            session_data['lives'] -= 1
            session_data['enemies'].remove(enemy)


def weapon_shell_movement(session_data, player: Player) -> None:
    shell: WeaponShell
    for shell in session_data['weapon_shells'][:]:
        if shell.parent == player:
            target = session_data['enemies']
            speed = -session_data['laser_vel']
        else:
            target = player
            speed = session_data['laser_vel']
        shell_exists = shell.move(speed, target, session_data['laser_damage'])
        if not shell_exists:
            session_data['weapon_shells'].remove(shell)

def generate_medkits(session_data, player: Player):
    probability = 30 # each 30 sec
    if player.health <= 20:
        probability = 10
    elif player.health <= 70:
        probability = 20
    if random.randrange(0, probability*game_data['FPS']) == 1:
        medkit = Medkit(random.randrange(50, game_data['width'] - 100),
                        random.randrange(-1500, -100))
        session_data['static_objects'].append(medkit)


def static_objects_movement(session_data, player: Player):
    obj: StaticObject
    for obj in session_data['static_objects'][:]:
        obj_h_vel = session_data['static_vel']
        if obj.y > game_data['height'] * 0.7:
            obj_h_vel = random.randrange(-session_data['static_vel'],
                                       0,3 * session_data['static_vel'])
        obj.move(obj_h_vel)
        if obj.collide(player):
            player.health += 50
            if player.health >= player.max_health:
                player.health = player.max_health
            session_data['static_objects'].remove(obj)
