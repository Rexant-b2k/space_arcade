import os

import pygame

from const import WIDTH, HEIGHT, COLORS

# from main import YELLOW_SPACE_SHIP, YELLOW_LASER

# WIDTH, HEIGHT = 750, 750
WIDTH, HEIGHT = 1600, 900
# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'enemy3_small.png'))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'enemy2_small.png'))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'enemy1_small.png'))

# Player player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'main_ship3_small.png'))

# Lsers
RED_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_red.png'))
GREEN_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_green.png'))
BLUE_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_blue.png'))
YELLOW_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_yellow.png'))





def collide(obj1, obj2): # ?
    offset_x = obj2.x - obj1.x
    ofsset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, ofsset_y)) != None


class SpaceObject: # need to create base class
    '''Base object that can appear on game screen'''
    def __init__(self, pos_x, pos_y, img):
        self.x = pos_x
        self.y = pos_y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vert_vel, horiz_vel=0):
        self.y += vert_vel
        self.x += horiz_vel


class WeaponShell(SpaceObject):
    '''Base shooting object, which can make a damage'''
    def __init__(self, pos_x, pos_y, img, parent, damage=10):
        super().__init__(pos_x, pos_y, img)
        self.damage: int = damage
        self.parent: Ship = parent

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0) # ?
    
    def collision(self, obj):
        return collide(self, obj)

    def move(self, vert_vel, obj=None, damage=10, horiz_vel=0):
        super().move(vert_vel)
        exists = True
        if self.off_screen(HEIGHT):
            exists = False
        elif isinstance(obj, Player):
            if self.collision(obj):
                obj.health -= damage
                exists = False
        elif isinstance(obj, list):
            for element in obj:
                if self.collision(element):
                    obj.health -= damage
                    exists = False
        return exists


class Laser(WeaponShell):
    '''Base attack shot, moved directly down'''
    pass


class Ship(SpaceObject):
    COOLDOWN = 30 # half a second if FPS = 60

    def __init__(self, pos_x, pos_y, session_data, health=100):
        self.x = pos_x
        self.y = pos_y
        self.health = health
        self.img = None
        self.laser_img = None
        self.cool_down_counter = 0
        self.session_data = session_data

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self): # cooldown is located in main
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img, self)
            self.session_data['weapon_shells'].append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()

class Player(Ship):
    COOLDOWN = 20 # 1/3 a second if fps = 60

    def __init__(self, pos_x, pos_y, session_data, health=100):
        super().__init__(pos_x, pos_y, session_data, health)
        self.img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.img)
        self.max_health = health

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img, self)
            self.session_data['player_weapon_shells'].append(laser)
            self.cool_down_counter = 1

    def move_lasers(self, vel, objs): # change globally design
        self.cooldown()
        for laser in self.session_data['player_weapon_shells']:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.session_data['player_weapon_shells'].remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        # obj.health -= 10
                        objs.remove(obj)
                        self.session_data['score'] += 1
                        if laser in self.session_data['player_weapon_shells']: # worked even before this if
                            self.session_data['player_weapon_shells'].remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, COLORS['red'],
                         (self.x, self.y + self.img.get_height() + 10,
                         self.img.get_width(), 10))
        pygame.draw.rect(window, COLORS['green'],
                         (self.x, self.y + self.img.get_height() + 10,
                         self.img.get_width() * (self.health / self.max_health), 10))


class Enemy(Ship):
    COLOR_MAP = { # could be types later
        'red': (RED_SPACE_SHIP, RED_LASER),
        'green': (GREEN_SPACE_SHIP, GREEN_LASER),
        'blue': (BLUE_SPACE_SHIP, BLUE_LASER)
    }

    def __init__(self, pos_x, pos_y, session_data, color, health=100):
        super().__init__(pos_x, pos_y, session_data, health)
        self.img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.img)

    def shoot(self): # possible fix at parent level
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img, self) # -20 is bad. it is to fix attacking position of laser
            self.session_data['weapon_shells'].append(laser)
            self.cool_down_counter = 1
