from csv import reader
from os import walk
import pygame
from settings import TILESIZE


def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=",")
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_folder(path):
    surface_list = []
    # import all images from a folder
    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + "/" + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)


def import_cut_graphic(path):
    """Cut a tileset into correct sprites

    Parameters
    ----------
    path: the filepath to find the tileset
    """

    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / TILESIZE)
    tile_num_y = int(surface.get_size()[1] / TILESIZE)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * TILESIZE
            y = row * TILESIZE
            new_surface = pygame.Surface((TILESIZE, TILESIZE))
            new_rect = pygame.Rect(x, y, TILESIZE, TILESIZE)
            new_surface.blit(surface, (0, 0), new_rect)
            cut_tiles.append(new_surface)
    return cut_tiles
