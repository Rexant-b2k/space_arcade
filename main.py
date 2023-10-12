import pygame

from const import COLORS
from data import Player
from helper import (game_init, game_session_init, paused, escape_game,
                    get_horizontal_center_position, get_middle_position,
                    generate_enemies, enemies_movement, weapon_shell_movement,
                    generate_medkits, static_objects_movement)

def main(session_data):
    run = True

    main_font = pygame.font.SysFont('comicsans', game_data['height']//18)
    lost_font = pygame.font.SysFont('comicsans', game_data['height']//15)
    
    player = Player(game_data['width'] / 2,
                    game_data['height'] * 0.87, # magic
                    session_data)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0 # works for 'defeat' message stays on screen
    
    def redraw_window():
        game_data['WINDOW'].blit(game_data['BG'], (0, 0))
        # draw text
        lives_label = main_font.render(f'Lives: {session_data["lives"]}', 1, COLORS['white'])
        level_label = main_font.render(f'Level: {session_data["level"]}', 1, COLORS['white'])
        score_label = main_font.render(f'Score: {session_data["score"]}',
                                              1, COLORS['white'])

        game_data['WINDOW'].blit(lives_label, (10, 10))
        game_data['WINDOW'].blit(level_label, (game_data['width'] - level_label.get_width() - 10, 10))
        game_data['WINDOW'].blit(score_label, 
                    (get_horizontal_center_position(score_label), 10))
        # debug_label = main_font.render('DEBUG========0.7===================++++++++++++', 1, COLORS['white'])
        # game_data['WINDOW'].blit(debug_label, (0, game_data['height'] * 0.7))

        
        for enemy in session_data['enemies']:
            enemy.draw(game_data['WINDOW'])

        for shell in session_data['weapon_shells']:
            shell.draw(game_data['WINDOW'])

        for obj in session_data['static_objects']:
            obj.draw(game_data['WINDOW'])

        player.draw(game_data['WINDOW'])

        if lost:
            lost_label = lost_font.render('You have lost!', 1, COLORS['white'])
            game_data['WINDOW'].blit(lost_label, get_middle_position(lost_label))

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

        # Enemies generation
        if len(session_data['enemies']) == 0:
            generate_enemies(session_data)

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
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player.x + session_data['player_vel'] + player.get_width() < game_data['width']: # right, size player
            player.x += session_data['player_vel']
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and player.y - session_data['player_vel'] > 0: #up
            player.y -= session_data['player_vel']
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and player.y + session_data['player_vel'] + player.get_height() + 18 < game_data['height']: # down, size player, 18 to show healthbar
            player.y += session_data['player_vel']
        if keys[pygame.K_SPACE]:
            player.shoot()

        # Weapon shell movement
        weapon_shell_movement(session_data, player)

        # Player cooldown for shooting
        player.cooldown() # extracted from player.move_lasers

        # Enemy movement
        enemies_movement(session_data, player)

        # Generate medkits
        generate_medkits(session_data, player)

        # Static objects movements
        static_objects_movement(session_data, player)



def main_menu():
    global game_data
    title_font = pygame.font.SysFont('comicsans', int(game_data['height']/12.85))
    run = True
    while run:
        game_data['WINDOW'].blit(game_data['MENU_BG'], (0, 0))
        title_label = title_font.render('Press the mouse to begin...', 1, COLORS['white'])
        game_data['WINDOW'].blit(title_label, get_middle_position(title_label))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                session_data = game_session_init() # possibly to modify in future with difficulty level
                main(session_data)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_data['WINDOW'].blit(game_data['BG'], (0, 0))
                    pygame.display.update()
                    escape_game()
    pygame.quit()


if __name__ == '__main__':
    game_data = game_init()
    main_menu()
