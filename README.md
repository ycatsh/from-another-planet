![Logo](https://github.com/ycatsh/from-another-planet/assets/91330011/f5638c12-6718-4beb-8e9f-4fb21de5c59e)
<br>

![releases](https://img.shields.io/github/v/release/ycatsh/from-another-planet?logo=Github)
![downloads](https://img.shields.io/github/downloads/ycatsh/from-another-planet/total?logo=Github)
![commits](https://img.shields.io/github/commits-since/ycatsh/from-another-planet/latest?logo=Github)

From Another Planet is written in [python](https://www.python.org/) using the [pygame](https://www.pygame.org/news) library. It features intense fast-placed gameplay with a bunch of power-ups. Player is lost in an unidentified area far away from your home planet. Finish the objective and fight your way through to reach home safely.

## Latest Updates
**Player Teleportation:** The player will receive a power-up to teleport to the mouse pointer's location.  
**In-between rock collisions:** When two or more rocks collide with each other they collectively all blow up.

## How to play 
**WASD** to move / **MB1** to shoot / **MB2** for shotgun / **SPACE** to teleport

Kill the incoming enemies to advance levels, the speed of the laser and frequency of aliens (different type of aliens too) increase as levels are completed. When the enemies [reach the other end](https://www.youtube.com/watch?v=n_L3mn7uweg) of the screen, player loses a life. The rocks and laser [instantly kill](https://www.youtube.com/watch?v=n_L3mn7uweg&t=1m17s) the player on contact.    

Occasionally the player will receive a power-up to [teleport](https://www.youtube.com/watch?v=n_L3mn7uweg&t=18) to game crosshair and upon getting 30 kills the player can use a shotgun which has a cooldown of 300 ticks. Rocks can collide with each other or the player can shoot at the rocks at least 5 times to [blow them up](https://www.youtube.com/watch?v=n_L3mn7uweg&t=54).


## Download
You can do any one of the following to run the game. Downloading from releases is recommended.  

Head to [releases](https://github.com/ycatsh/from-another-planet/releases) and download the latest version. After downloading and extracting the zip file run `game.exe`   

Otherwise, To run or build with the source code: download the repository and the required dependencies from `requirements.txt` then run the python file. You can also create your own build using the source code:
1. Install [`pyinstaller`](https://pypi.org/project/pyinstaller/) from pip 
2. In the project directory run `pyinstaller game.py --onefile --noconsole`
3. delete `build/` and create a new folder for the game
4. Drag the `assets/` folder and `game.exe` from `dist/` into the new folder 
5. Run the executable  
  
  
## Gameplay Video
https://github.com/ycatsh/from-another-planet/assets/91330011/92122f19-cc9d-4051-99ea-499dd7a285f1
