"""
Sean Nishi
11/16/2022
Lunk Menu
"""

import pygame
from settings import *

class MainMenu:
    #Contains game state and vars for the main menu
    def __init__(self):
        self.start_screen_path = 'images/start_screen.png'
        #load menu image
        self.menu_image = pygame.image.load(MAIN_MENU_BACKGROUND_PATH)
        #font
        self.font = pygame.font.SysFont('Corbel', 40)
        #font color, black
        self.font_color = (255, 255, 255)

        self.display_surface = pygame.display.get_surface()

        #render menu text on screen
        self.menu_text = [self.font.render('New Game', True, 40),
        self.font.render('Options', True, 40),
        self.font.render('Credits', True, 40),
        self.font.render('Quit', True, 40)]

        self.text_increment = 50
        self.menu_text_size = [180, 40]

        self.text = self.font.render('quit', True, self.font_color)

    #destructor that returns the main menu user input
    def __del__(self):
        #return self.men
        pass

    def run(self):
        self.display_surface.blit(self.menu_image, (0, 0))
        self.draw_menu_options()
        self.menu_selection()
        
    def draw_menu_options(self):
        #get mouse position as tuple
        self.mouse = pygame.mouse.get_pos()
        #shade in button when mouse hovers over it
        for text in self.menu_text:
            if WINDOW_WIDTH/2 <= self.mouse[0] <= WINDOW_WIDTH/2+self.menu_text_size[0] and self.text_increment <= self.mouse[1] <= self.text_increment+self.menu_text_size[1]:
                pygame.draw.rect(self.display_surface, (170, 170, 170), [WINDOW_WIDTH/2, self.text_increment, self.menu_text_size[0], self.menu_text_size[1]])
                self.display_surface.blit(text, (WINDOW_WIDTH/2, self.text_increment))
            else:
                pygame.draw.rect(self.display_surface, (100, 100, 100), [WINDOW_WIDTH/2, self.text_increment, self.menu_text_size[0], self.menu_text_size[1]])
                self.display_surface.blit(text, (WINDOW_WIDTH/2, self.text_increment))
            self.text_increment+=50
        self.text_increment = 50
        
    def menu_selection(self):
        #event to handle clicking on menu options
        self.text_increment = 50
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                #menu_option = self.menu_text.count()
                #hovering over menu option
                for text in self.menu_text:
                    if WINDOW_WIDTH/2 <= self.mouse[0] <= WINDOW_WIDTH/2+self.menu_text_size[0] and self.text_increment <= self.mouse[1] <= self.text_increment+self.menu_text_size[1]:
                        pygame.quit()
                    self.text_increment+=50
