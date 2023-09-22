import os

import pygame
import random

from const import BG, MENU_BG, COLORS, WS_RESOLUTIONS, WIDTH, HEIGHT
from data import Player, Enemy, collide

os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100"
os.environ['SDL_VIDEO_CENTERED'] = "True"

# pygame.font.init()
# pygame.display.init() # doesn't help
pygame.init()
# pygame.key.set_repeat() # doesn't help

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Arcade')

def game_init():
    game_data = {
        'resolution': WS_RESOLUTIONS['1600x900'],
        # 'music': False,
        # 'sounds': False,
        'FPS': 60,
    }
    return game_data

def game_session_init():
    session_data = {
        'score': 0,
        'enemies': [],
        'weapon_shells': [],
        'level': 0,
        'lives': 5,
        'wave_length': 5,
        'enemy_vel': 1,
        'player_vel': 5,
        'laser_vel': 5,
        'laser_damage': 10,
    }

    return session_data

def get_horizontal_center_position(obj):
    return WIDTH / 2 - obj.get_width() / 2

def get_vertical_center_position(obj):
    return HEIGHT / 2 - obj.get_height() / 2

def get_middle_position(obj):
    return (get_horizontal_center_position(obj),
            get_vertical_center_position(obj))

def paused():
    pause = True
    pause_font = pygame.font.SysFont('comicsans', 70)

    while pause:
        pause_label = pause_font.render('Pause. Press any key to continue', 1, COLORS['violet'])
        WINDOW.blit(pause_label, get_middle_position(pause_label))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                pause = False

def escape_game():
    pause = True
    escape_font = pygame.font.SysFont('comicsans', 70)

    while pause:
        pause_label_first = escape_font.render('Are you going to leave game?', 1, COLORS['violet'])
        pause_label_second = escape_font.render('Press Enter to end the game or ESC to return', 1, COLORS['violet'])
        WINDOW.blit(pause_label_first, (get_horizontal_center_position(pause_label_first), HEIGHT/2 - pause_label_first.get_height()))
        WINDOW.blit(pause_label_second, (get_horizontal_center_position(pause_label_second), HEIGHT/2 + pause_label_first.get_height()))
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
                

def main(session_data):
    run = True

    main_font = pygame.font.SysFont('comicsans', 50)
    lost_font = pygame.font.SysFont('comicsans', 60)
    
    player = Player(WIDTH / 2,
                    HEIGHT * 0.87,
                    session_data) # magic

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0 # works for 'defeat' message stays on screen
    
    def redraw_window():
        WINDOW.blit(BG, (0, 0))
        # draw text
        lives_label = main_font.render(f'Lives: {session_data["lives"]}', 1, COLORS['white'])
        level_label = main_font.render(f'Level: {session_data["level"]}', 1, COLORS['white'])
        score_label = main_font.render(f'Score: {session_data["score"]}',
                                              1, COLORS['white'])

        WINDOW.blit(lives_label, (10, 10))
        WINDOW.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        WINDOW.blit(score_label, 
                    (get_horizontal_center_position(score_label), 10))

        
        for enemy in session_data['enemies']:
            enemy.draw(WINDOW)

        for shell in session_data['weapon_shells']:
            shell.draw(WINDOW)

        player.draw(WINDOW)

        if lost:
            lost_label = lost_font.render('You have lost!', 1, COLORS['white'])
            WINDOW.blit(lost_label, get_middle_position(lost_label))

        pygame.display.update()

    while run:
        clock.tick(game_data['FPS'])
        redraw_window()

        if session_data['lives'] <= 0 or player.is_dead():
            lost = True
            lost_count += 1
        
        if lost:
            if lost_count > game_data['FPS'] * 3: # 60 fps * 3 means 3 sec
                run = False
            else:
                continue

        # possible to put in another func
        if len(session_data['enemies']) == 0:
            session_data['level'] += 1
            session_data['wave_length'] += 5 # add 5 more enemies each level
            for _ in range(session_data['wave_length']):
                enemy = Enemy(random.randrange(50, WIDTH - 100),
                              random.randrange(-1500, -100), # -1500*level/5
                              session_data,
                              random.choice(['red', 'blue', 'green']))
                session_data['enemies'].append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused()
                elif event.key == pygame.K_ESCAPE:
                    escape_game()


        keys = pygame.key.get_pressed() # possible to add info on I and help on H
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player.x - session_data['player_vel'] > 0: #left
            player.x -= session_data['player_vel']
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player.x + session_data['player_vel'] + player.get_width() < WIDTH: # right, size player
            player.x += session_data['player_vel']
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and player.y - session_data['player_vel'] > 0: #up
            player.y -= session_data['player_vel']
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and player.y + session_data['player_vel'] + player.get_height() + 18 < HEIGHT: # down, size player, 18 to show healthbar
            player.y += session_data['player_vel']
        if keys[pygame.K_SPACE]:
            player.shoot()

        # Laser movement
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

        # player cooldown
        player.cooldown() # extracted from player.move_lasers

        # enemy_movement
        for enemy in session_data['enemies'][:]:
            if enemy.is_dead():
                session_data['enemies'].remove(enemy)
                session_data['score'] += 1
                continue
            enemy.move(session_data['enemy_vel'])
            enemy.cooldown() # refresh cooldown to shoot

            if random.randrange(0, 2*game_data['FPS']) == 1: # each ~ 2 sec
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                session_data['score'] += 1
                session_data['enemies'].remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                session_data['lives'] -= 1
                session_data['enemies'].remove(enemy)



def main_menu():
    global game_data
    title_font = pygame.font.SysFont('comicsans', 70)
    run = True
    while run:
        WINDOW.blit(MENU_BG, (0, 0))
        title_label = title_font.render('Press the mouse to begin...', 1, COLORS['white'])
        WINDOW.blit(title_label, get_middle_position(title_label))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                session_data = game_session_init() # possibly to modify in future with difficulty level
                main(session_data)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    WINDOW.blit(BG, (0, 0))
                    pygame.display.update()
                    escape_game()
    pygame.quit()


if __name__ == '__main__':
    game_data = game_init()
    main_menu()
