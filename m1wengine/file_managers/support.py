"""This module contains methods to load game assets."""
from csv import reader
from os import walk
import pygame
from m1wengine.settings import TILESIZE


def import_csv_layout(path: str) -> list[int]:
    """Read in csv values into an array.

    Parameters
    ----------
    path: str
        The filepath to read from

    Returns
    -------
    list[int]
        The list of Tile values that represent the map layout
    """
    terrain_map: list = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=",")
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_folder(path: str) -> None:
    """Import all the surfaces in a directory.

    Parameters
    ----------
    path: str
        The filepath to import from
    """
    surface_list: list = []
    # import all images from a folder
    for _, __, image_files in walk(path):
        for image in image_files:
            full_path: str = path + "/" + image
            image_surface: pygame.Surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)


def import_cut_graphic(path: str) -> list[pygame.Surface]:
    """Cut a tileset into correct sprites.

    Parameters
    ----------
    path: str
        The filepath to find the tileset

    Returns
    -------
    list[pygame.Surface]
        The list of images extracted from a larger image
    """
    surface: pygame.Surface = pygame.image.load(path).convert_alpha()
    tile_num_x: int = int(surface.get_size()[0] / TILESIZE)
    tile_num_y: int = int(surface.get_size()[1] / TILESIZE)

    cut_tiles: list = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x: int = col * TILESIZE
            y: int = row * TILESIZE
            new_surface: pygame.Surface = pygame.Surface((TILESIZE, TILESIZE))
            new_rect: pygame.Rect = pygame.Rect(x, y, TILESIZE, TILESIZE)
            new_surface.blit(surface, (0, 0), new_rect)
            cut_tiles.append(new_surface)
    return cut_tiles
