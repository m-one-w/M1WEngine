import pygame


class BerryBush(pygame.sprite.Sprite):
    # other init options: sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))
    def __init__(self, pos, groups):
        super().__init__(groups)
        # self.sprite_type = sprite_type
        self.image = pygame.image.load("graphics/berry_bush/berryBush.png")
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
