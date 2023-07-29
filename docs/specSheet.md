# Lunk Game Spec Sheet
## version 1.0

## Table of contents
- [Objective](#objective)
- [Game Flow](#game-flow)
    - [Puzzle](#puzzle)
    - [Defeat Enemies](#defeat-enemies)
    - [Save Friendlies](#save-friendlies)
    - [Escort](#escort)
- [Player Movement](#player-movement)
    - [Wall Collisions](#wall-collisions)
    - [Player Rotation](#player-rotation)
      - [Movement Rotation](#movement-rotation)
      - [Animation Rotation](#animation-rotation)
      - [Player Status](#player-status)
- [Map](#map)
    - [Landscape Map](#landscape-map)
    - [Entity Map](#entity-map)
    - [Entity Detection](#entity-detection)
    - [Level Generation](#level-generation)
- [Enemy Movement](#enemy-movement)
- [Enemy Interaction](#enemy-interaction)
    - [Attack Enemy Options](#attack-enemy-options)
    - [Enemy Attack Damsel](#enemy-attack-damsel)
- [Damsel Movement](#damsel-movement)
- [HUD Elements](#hud-elements)
    - [Score System](#score-system)
        - [High Score](#high-score)
        - [Boredom Meter](#boredom-meter)
- [Map Rendering System](#map-rendering-system)
- [Tile Set Support](#tile-set-support)


## Objective
The main objective of Lunk, the player character, is to complete the level specific objective before the player character gets [bored](#boredom-meter).
The secondary objective is for the player to get the highest score possible while playing each level.

Lunk positive interactions:
* Lunk wants to crush his enemies.
* Lunk wants to save the damsels.

Positive interactions will result in:
* add gameplay time to the Player's [Boredom Meter](#boredom-meter)
* add to the Player's [High Score](#high-score)
* an affirmative grunt of approval from the player character


Lunk negative interactions:
* fall off the map, reappear somewhere random
* crush damsel
* ingest non-tasty things

Negative interaction will result in:
* removing gameplay time from the player's [Boredom Meter](#boredom-meter)
* angry chat boxes from the player's character complaining and being distracting
  * this will be increased in intensity as more negative interactions are completed

## Game Flow
There will be a dynamic amount of enemies on the map based on difficulty.
There will be a static amount of damsels in distress on the map.
The map can have landscape entities that act as barriers.

A cutscene of the camera panning across the map should be shown at the start of each level for players to plan their approach.

Level types include the following:

### Puzzle
Player explores a premade map. Player interacts with different entities (Items, enemies, friendlies) in a certain order to unlock the next part of the map.
Hints are given through objects in the map or text prompts on the screen that lead towards solutions..

#### Example:
Prompt appears saying “Hungry!!”
Go to berry bush because the player is hungry
Player becomes able to destroy wall blocking the next area due to “no hungry”
ETC…

### Defeat Enemies
Only enemy entities spawn, anywhere from a single boss that needs to be defeated with items to many small enemies that need to be defeated within a time limit.

Difficulty is affected by previous completion times. Completion times taken into account are specifically the defeat enemy levels.

#### Example:
##### Regular Defeat Enemies
Multiple enemies spawn on the map, the player must defeat them all as quickly as possible.
The boredom meter will be emphasized on this level type as the lose condition. If the boredom meter hits 0, the player loses. Enemies will do increased damage to the boredom meter and the player will be told this in the starting prompt.

At the end of the level of this type, the player will see a prompt with the end results of how many additional enemies will be added to the next level based on this level's completion performance.

##### Boss Level Defeat Enemies
A single enemy will have increased HP. Multiple attacks will be needed to defeat the boss. The player has the option to just run into the boss when the appropriate “Crush” action is queued up but this will give the minimum possible score for passing and make the next defeat multiple enemies level much harder.

At the end of the level of this type, the player will see a prompt with the end results of how many additional hit points will be added to the next level based on this level's completion performance.

### Save Friendlies
Player will be incentivized to plan an optimal route to save the maximum amount of damsels. There should always be multiple paths the player can take to add variety and challenge to this level type. Levels should be structured such that deviating from the optimal route should have negative consequences, but not be unfun to play. The consequences will involve dead damsels or a lower completion time.

#### Example:
Multiple enemies are spawned near multiple damsels on the map in a way that the damsels are in immediate danger. The player will be able to save the damsels by running in a specific route and killing or distracting enemies in the correct order. If the wrong order is chosen, damsels will be killed due to not making it in time. If enemies are not killed or distracted, damsels may be killed.

The level ends when every damsel is killed or saved. Damsels within a certain distance of the player will trail along and be considered “saved” after a certain amount of time but can still be killed by enemies. If enemies are within a certain distance of “saved” damsels they are no longer marked as “saved”.

### Escort
Damsel has a HP indicator based on the difficulty selected.
A single NPC damsel in distress runs through the level in a set path slightly slower than the player. Enemies will attack the walking NPC until they make it to the end of the level. Player must defend the NPC, this can be through killing or distracting enemies before they kill the damsel.

#### Example:
The player moves faster than the damsel but not by too much. Enemies will ignore the player in this level type and target only the damsel. The damsel has a predefined path that must be completed without dying to complete the level.


## Player Movement
Lunk always goes forward, but he can choose to turn to the left or the right.

This means movement is rotational in nature. Lunk's heading will be adjusted but not suddenly altered. The purpose of this movement system is to give Lunk the feeling of an unwieldy character who is hard to control directly. The player can steer Lunk, but not command him. The same thought process was used when creating Lunks abilities and enemy interactions.

If Lunk falls off the map, he jumps back up so high that the landing spot is a random area within a 10 by 10 area near the fall point

### Wall Collisions
If Lunk initiates a wall collision there will be 2 potential outcomes:
* Lunk turns around
  * Lunk pauses movement for 1 second while slowly turning around
  * Lunk chooses a new direction to run from a random direction not facing the wall
  * Lunk resumes running
* Lunk keeps going
  * The wall is destroyed
  * Lunk moves forward
  * Boredom meter is reduced by x max percent. x should be set to something very large, potentially 25% of max meter.

Each option has a 50% chance of happening.

### Player Rotation
The player rotation effects the sprite animation and where the sprite is moving.
Due to Lunk always going forward, as the sprite rotates, the rotation determines which direction points forward.
The Direction is stored in a vector containing the X and Y orientation in a grid from -1 to 1 as shown below:

<img src="./specSheetImages/sprite-directions.PNG" width="300" height="300" style="padding-left: 50px;">

#### Movement Rotation
The player movement rotation refers to rotating the X and Y direction with the left and right keyboard buttons.
As the player runs foward, this rotation steers the player.

#### Animation Rotation
The player animation rotation refers to the animation rotation offset that is used when displaying the player's animation images.
With no rotation, there are only animations for the four cardinal directions. Animation rotation adds in a rotation to the displayed animation
in alignment with the current directional rotation. 

The animation used during this rotation will be defined by the player status.

#### Player Status

The player status is determined by the current player rotation. The options are listed below:

* Up:

  This status is when the direction vector falls within the northern most section of the direction sphere.
* Down:

  This status is when the direction vector falls within the southern most section of the direction sphere.
* Left:

  This status is when the direction vector falls within the western most section of the direction sphere.
* Right:

  This status is when the direction vector falls within the eastern most section of the direction sphere.

The player status determines which animation frame will be active.

## Wall Tracking
The movable objects including the player, enemies, and allies will at all times be aware of the surrounding walls. This will be done by comparing the wall positions to the moveable entity positions on each move. For simple "turn around" logic, the moveable objects will store the last free tile location as well as the last wall hit location. when turning away from a wall it will help ensure they do not try to run through the wall and can turn around.


## Map
There are multiple map files stored per level. A map file is a CSV file containing the location of a tilesheet asset. Each layer of objects within the map will have it's own CSV file.
The 2 essential maps are the landscape map and the entity map, but there will be additional maps stored that contain item locations such as rocks, trees, shrubs, and sign posts ect.

### Landscape Map
The map will be stored as CSV files containing integers associated with a landscape on the tileset.
A internal mapping of values to tileset locations will be stored for simple tileset lookup based on the CSV file.

### Entity Map
The entity map will be the same size as the landscape map, but hold and array of objects instead of primitives. Each object will contain all the entities within that map location.
If nothing can be interacted with, the map location will be set an empty array. This map will not exist as a file, and instead will be managed in memory.

### Entity Detection
Any entities that can interact with each other will be listed on the entity map. Collisions and other interactions such as movement towards entities under specific conditions will be done by checking against the entity map.

Entities will know where they are on the entity map by storing their own location indivdually. Both the individual location and the entity map location should be updated on movement.

### Level Generation
Each map will be created manually in the Tiled map editor program.

In the future, new maps will be automatically generated as they are needed for endless gameplay options. The algorithm to generate maps should be defined here at that time.

## Enemy Movement
Enemies will wander the map after being spawned.

* if a damsel is within 10 squares, enemies will walk generally toward the damsel
* if a damsel is within 4 squares, enemies will run directly towards the damsel
* if Lunk is greater than 5 squares enemies will walk generally away from Lunk
* if Lunk is less than 5 squares and a damsel is within 10 squares, enemies will run directly towards Lunk to stop him from saving the damsel
* if enemy is blocked (on a wall or other object), walk towards Lunk

## Enemy Interaction
When the hit box interacts, rotate through the 3 abilities described [here](#attack-enemy-options).

### Attack Enemy Options
Options will rotate through every enemy interaction in a loop. The options to attack an enemy are:
* Crush

  The simplest enemy interaction. Any enemy is simply crushed beneath Lunk's feet with no chance of survival.
* Throw

  Lunk chooses to remove his enemy from sight by tossing it out like the trash. Enemies will fly forward 2 or 3 spaces before dying in the embrace of the ground.
If a damsel is crushed by Lunk's flying enemy, Lunk losses his points from his [health bar](#health-bar).
* Eat

  Lunk gets hungry, he eats his enemy. Eating can be positive or negative depending on what is eaten.

### Enemy Attack Damsel
Enemies will try to kill or kidnap damsels if they see any.

The mechanics of this are to be decided.

## Damsel Movement
Damsels will wander the map when spawned.

* if an enemy if within 6 squares of a damsel, they will walk in the opposite direction
    * this is ignored if Lunk is nearby in favor of Lunk related logic
* if Lunk is within 12 squares of a damsel, they will walk towards Lunk
* if Lunk is within 5 squares of a damsel, they will stand still and make heart emojis at Lunk

## HUD Elements

The HUD will show the following at all times of gameplay:

* 3 score system components 
* a pause game button
    * when paused, allow the user to continue or exit the game.

### Score System
#### High Score
Lunk gains points for doing things he likes to do.
Each favorable action adds to the total high score for an amount specific to each action

#### Boredom Meter
Lunk can only do so many things he doesn't like doing before deciding to sleep and ignore everything.
The Boredom Meter is a countdown to Lunk sleeping out of anger. When it reaches 0, the game is over.
Each level has a set timer that ticks up to the moment Lunk goes to sleep from boredom.

## Map Rendering System
The map shall not be rerendered unless the player object is within x% of the screen width.

If the player has crossed the rerendering border, the map and player will rerender repeatedly moving the player position slowly back to the center of the view port until the player is centered in the screen.

## Tile Set Support
There will be support for reading images in from a tileset or spritesheet of images. 
A tileset is defined as a single image storing many subimages in a grid. This grid of images can be parsed for internal use by knowing the coordinates of specific images within the tileset grid.

Tilesets are used to create landscape maps in an external programed called tiled. These tiled maps are exported as an CSV of integer values that map to a subimage within the tileset.
Internal mapping that matches tiled mapping is stored for seemless integration between generated maps and pygame.
