"""This module contains the general game settings."""
# Screen dimensions
WINDOW_SIZE = (1280, 720)
WINDOW_WIDTH = WINDOW_SIZE[0]
WINDOW_HEIGHT = WINDOW_SIZE[1]
WINDOW_CENTER = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

FPS = 60
TILESIZE = 16

# entity image width and height
ENTITY_WIDTH = 16
ENTITY_HEIGHT = 20

# modify model rect to have slightly less tall hitbox. Used for movement
ENTITY_HITBOX_OFFSET = -4

# image paths
GAME_ICON_PATH = "game_assets/graphics/game_icon.png"
STUDIO_SPLASH_SCREEN_PATH = "game_assets/graphics/studio_logo.png"
MAIN_MENU_BACKGROUND_PATH = "game_assets/graphics/main_menu/ground.png"

# Constant used to loop game music
LOOP_MUSIC = -1
MAIN_MENU_MUSIC = "game_assets/music/main_menu/science-documentary-169621.mp3"

CHARACTER_IMAGES = "game_assets/graphics/tiles/entities/characters/"
ITEM_IMAGES = "game_assets/graphics/tiles/entities/items/"
