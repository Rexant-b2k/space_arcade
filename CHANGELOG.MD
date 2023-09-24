
# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).
 
## [Unreleased (0.3-alpha)] - yyyy-mm-dd
 
Here I am writing upgrading notes for brands. It's my effort to make them as
straightforward as possible.
 
### Added
- 'Game init' function and entity of same name, which keep base game data to launch.
- 'get screen res' function, based on 3rd party screeninfo module, which initialize all displays and find their resolutions and the primary one.
- 'Escape game' function to have an ability to leave the game.
- Helper module to move there callable functions from main module.

 
### Changed
  
#### Tech
    
- 'Game init' entity keep data of of resolution, screen refresh constant, initialized game window, and paths to background and menubackground splash screens with transformation to current resolution.
- 'get screen resolution' collects info about all connected displays, their resolutions and which of them is primary. If no primary (in a case of Virtual Machine) - uses the first one available. Basing on screen resolution - find the most proper game resolution (maximum closest (equal or smaller one) to current display resolution). Analyze if display is squared, widescreen or superwide and calculate best game window size from **minimal** parameter.
- Since all objects in game are 'SpaceObjects' inheritors and collision is possible only between this type of objects, function 'collide' was removed from global scope if data module and moved to SpaceObject as a method. All nessesary changes in main and helper modules were made.
- Replaced 'paused' and 'escape game' reaction to pygame.Keydown from pygame.key.get_pressed()
- Enemy generations is now made as a dedicated function and moved to helper module
- Enemy movement is now made as a dedicated function and moved to helper module
- Weapon shell movement is now made as a dedicated function and moved to helper module
- Changed the order in WS_RESOLUTION constant to help 'get_screen_res' function.
- Added helpers to find the middle horizontal, vertial and total position on screen.
- screeninfo module adeed to requirements.txt

#### Gameplay

- 'Escape game' (ESC button) can now be pressed in main menu
- Player movement speed changed to variable which depends on screen resolution. Now, it is a constant time to move player from left edge position to the right one regardless of resolution.
- background pictures are now transforms to correspond current resolution
- Enemy ships don't attack in bottom part of screen (30%) anymore to reduce instant death of player by unexpected shots.

### Fixed
- 'Pause' function no more switch on/off rapidly following game pressing events. ('Pygame' usually copies input keys pressed)

#### Known issues
- ship models and weapon shells are not scalable, basing by screen size
- all speeds and not scalable by screen resolution
 
## [0.2-alpha] - 2023-09-16
  
Here we would have the update steps for 0.2-alpha for people to follow. This update is dedicated for game classes changes.  
The development was being made in OOP_Improvements branch.
 
### Added
- 'Game session' entity, which keeps data of active session
- 'Score' attribute to count player's activity such as destroying enemies.
- Each WeaponShell (including Laser) now contain the information of the ship, who created it

 
### Changed
  
#### Tech
    
- Game elements are not belonged to each other. Instead, they become part of game session entity.
- Reduced code in inherited classes. Class Laser containt only 'pass' keyword inside. Reduced 'init' blocks in each class
- Methods 'draw' were removed elsewhere, except SpaceObject.
- Method 'shoot' was unified in parent Ship class and removed from EnemyShip and Player class.
- Method 'move' was removed in all classes except Base 
- Ships attribute "ship_img" changed to "img" to correspond base SpaseObject class
- Since the lasers are no more part of ships, function 'move lasers" were moved to Main module. Cooldown was also moved there.
- 'Move' method in WeaponShell class were extended and added deep analysis parent/target to make sure that player's shells can attach only enemies, enemies' ones - only player ship and no each other. (Required change since Lasers were moved to 'global scope' of game tech design - to 'game session').


#### Gameplay

- Reduced the cooldown of shooting for Player from 1/2 to 1/3 of second   

### Fixed
 
- Lasers are not disappearing when enemy ship is destroyed

### Known issues
  
- Function 'collide' is out of classes
  
## [0.1-alpha] - 2023-09-08
 
### Added
- Base game functionality based on Pygame module:  
You have to protect your own base (lives counter) and not allow any enemy to reach it. Your lifebar decreases if you get shot of collide with enemy.
- Constants module. Keeps color map and list of resolutions
- Base pause function (with limitations)
   
### Changed
- Game is being adapted for widescreen resolution
- Ship models were changed for hi-res models made by MidJourney
- Background and menu background images replaced for hi-res splash screens
- Classes are moved to dedicated module Data.
- Created new hierarchy of game classes. Now it is a base class 'Space objects', all other clasees inheritates from it. Created only map of classes yet.
- pygame module added to requirememnts.txt

 
### Fixed
 
- Available hardcode elements were replaced by variables and constants

### Known issues
  
- Enemy lasers disappear when ship was destroyed