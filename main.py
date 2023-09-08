import pygame
import os
# import time
import random

from const import COLORS
from data import Player, Enemy, collide

pygame.font.init()

# WIDTH, HEIGHT = 750, 750
WIDTH, HEIGHT = 1600, 900
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Arcade')


# Background
# BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background-black.png')), (WIDTH, HEIGHT))
BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'space_bg.webp')), (WIDTH, HEIGHT))
MENU_BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'main_menu.webp')), (WIDTH, HEIGHT))
# MENU_BG = pygame.image.load(os.path.join('assets', 'main_menu_bg.png'))

def get_horizontal_center_position(obj):
    return WIDTH / 2 - obj.get_width() / 2

def get_vertical_center_position(obj):
    return HEIGHT / 2 - obj.get_height() / 2

def get_middle_position(obj):
    return (get_horizontal_center_position(obj),
            get_vertical_center_position(obj))

def paused(pause):
    pause_font = pygame.font.SysFont('comicsans', 70)

    while pause:
        pause_label = pause_font.render('Pause. Press any key to continue', 1, COLORS['violet'])
        WINDOW.blit(pause_label, get_middle_position(pause_label)) # magic
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                pause = False

def main():
    run = True
    FPS = 120 # change speed of game, base = 60
    level = 0
    lives = 5 # survivability of our base
    main_font = pygame.font.SysFont('comicsans', 50)
    lost_font = pygame.font.SysFont('comicsans', 60)
    
    session_data = {
        'score': 0,
        'enemies': [],
        'lasers': [] # need to replace by shots or smth like that
    }
    enemies = [] # need to move to session_data
    wave_length = 5
    enemy_vel = 1

    player_vel = 5 # speed of player
    laser_vel = 5
    player = Player(300, 630, session_data) # magic

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0
    
    def redraw_window():
        WINDOW.blit(BG, (0, 0))
        # draw text
        lives_label = main_font.render(f'Lives: {lives}', 1, COLORS['white'])
        level_label = main_font.render(f'Level: {level}', 1, COLORS['white'])
        score_label = main_font.render(f'Score: {session_data["score"]}',
                                              1, COLORS['white'])

        WINDOW.blit(lives_label, (10, 10))
        WINDOW.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        WINDOW.blit(score_label, 
                    (get_horizontal_center_position(score_label), 10))

        
        for enemy in enemies:
            enemy.draw(WINDOW)

        player.draw(WINDOW)

        if lost:
            lost_label = lost_font.render('You have lost!', 1, COLORS['white'])
            WINDOW.blit(lost_label, get_middle_position(lost_label))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
        
        if lost:
            if lost_count > FPS * 3: # 60 fps means 3 sec
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5 # add 5 more enemies each level
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100),
                              random.randrange(-1500, -100), # -1500*level/5
                              random.choice(['red', 'blue', 'green']))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            # elif event.type == pygame.KEYDOWN

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player.x - player_vel > 0: #left
            player.x -= player_vel
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player.x + player_vel + player.get_width() < WIDTH: # right, size player
            player.x += player_vel
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and player.y - player_vel > 0: #up
            player.y -= player_vel
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and player.y + player_vel + player.get_height() + 18 < HEIGHT: # down, size player, 18 to show healthbar
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
        if keys[pygame.K_p]:
            pause = True
            paused(pause)


        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*FPS) == 1: # each ~ 2 sec
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                session_data['score'] += 1
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)



        player.move_lasers(-laser_vel, enemies)

def main_menu():
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
                main()
    pygame.quit()



if __name__ == '__main__':
    main_menu()