# Galactic Guardians:
# The Sentinel Saga
## _== Space arcade ==>>_
![Galactic Guardians: The Sentinel Saga](https://github.com/Rexant-b2k/space_arcade/blob/main/screenshots/splash.webp)
## based on:
[![N|Pygame](https://www.pygame.org/docs/_static/pygame_tiny.png)](https://www.pygame.org/)

This game, inspired by classic 80's arcades, will deep you into old-fashion fun and joy.
![Game process](https://github.com/Rexant-b2k/space_arcade/blob/main/screenshots/screen2.webp)
![Game pause](https://github.com/Rexant-b2k/space_arcade/blob/main/screenshots/screen1.webp)
![Start screen](https://github.com/Rexant-b2k/space_arcade/blob/main/screenshots/screen3.webp)

## Features
Project developing currently in progress. However the current version is fully playable.

- Three types of enemy ships
- Lasershots and fun
- Protect your base!

## Controls
| Button           | Action       |
| ---------------- | ------------ |
| A or Left Arrow  | Move left    |
| D or Right Arrow | Move Right   |
| W or Up Arrow    | Move Forward |
| S or Down Arrow  | Move Back    |
| Spacebar         | Shoot        |
| P                | Pause        |


## Installation and start the game
*Requires python and pygame library. I recommend use virtual enviroment (venv)

1. Clone this repository
2. Perform commands to prepare venv and download dependencies
```sh
python3 -m venv venv
python -m pip install --upgrade pip
source venv/bin/activate
pip install -r requirements.txt
```
3. Start the game
```sh
python main.py
```
4. Enjoy!

## Tech
Galactic Guardians uses a number of open source and proprietary projects to work properly:
- [Python] - Python 3.11
- [Pygame] - Pygame library  
  
And of course Galactic Guardians: The Sentinel Saga itself is open source with a [public repository][Space_arcade]
 on GitHub.

## Plugins

Galactic Guardians: The Sentinel Saga is currently extended with the following plugins.
Instructions on how to use them in your own application are linked below.

| Plugin       | README          |
| -------------| --------------- |
| Dillinger    | [Dillinger.io]  |

## Version history
v0.2a (current) - Lasers are not belongs ships anymore. Now if you defeat an enemy - his laser will still go on (previously - dissapered with the ship). Tech: Classes inheratances and global change to OOP approach. [16.09.2023]  
v0.1a - Base gameplay, initial refactoring of code [08.09.2023]  

## Authors
[Sergei Baryshevskii](https://www.linkedin.com/in/barysecho/)  
With gratitude to:  
[Tim Ruscica](https://www.techwithtim.net/) (approach to game development powered by pygame)

## License

BSD-3 Clause License

**Free Software, Hello everybody**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [Space_arcade]: <https://github.com/Rexant-b2k/space_arcade/>
   [git-repo-url]: <https://github.com/Rexant-b2k/space_arcade.git>
   [Pygame]: <https://www.pygame.org/>
   [Python]: <https://www.python.org/>
   [Dillinger.io]: <https://dillinger.io/>


