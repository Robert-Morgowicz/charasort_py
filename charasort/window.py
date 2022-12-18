# functions for pygame interraction with the game window
import sys

import pygame

black = 0, 0, 0
red = 255, 0, 0
white = 255, 255, 255

    
class button:
    def __init__(self, x, y, text, font, surface):
        self.rect = pygame.Rect(0, 0, 100, 50)
        self.rect.center = x, y
        self.surface = surface
        self.text = font.render(text, True, black)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = x, y

    def draw(self, screen):
        pygame.draw.rect(self.surface, black, self.rect, width=1, border_radius=0)
        screen.blit(self.text, self.text_rect)

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN: 
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    return True

class window:
    def __init__(self, xres, yres):
        pygame.init()
        pygame.display.set_caption('charasort')
        self.screen = pygame.display.set_mode((xres,yres))
        self.title_font = pygame.font.SysFont('arial', 64)
        self.subtitle_font = pygame.font.SysFont('arial', 48)
        self.text_font = pygame.font.SysFont('arial', 32)
        self.xres = xres
        self.yres = yres


    def draw_loading(self, datapath):
        # white out screen
        self.screen.fill(white)
        # draw loading message
        loading_text = self.title_font.render('Sorts are preparing.  Please wait warmly...', True, black)
        loading_rect = loading_text.get_rect()
        loading_rect.right = self.xres
        loading_rect.bottom = self.yres
        self.screen.blit(loading_text, loading_rect)
        # TODO: display individual files loaded as text
        pygame.display.flip()

    def draw_start(self, charas : list, datapath : str):
        # draw title text
        self.screen.fill(white)
        title_text = self.title_font.render('Open Character Sorter', True, black)
        title_rect = title_text.get_rect()
        title_rect.center = (self.xres/2, 100)
        self.screen.blit(title_text, title_rect)
        subtitle_text = self.subtitle_font.render('a.k.a charasort', True, black)
        subtitle_rect = subtitle_text.get_rect()
        subtitle_rect.center = (self.xres/2, 150)
        self.screen.blit(subtitle_text, subtitle_rect)
        # draw loading text
        loading_text = self.text_font.render(f'loaded {len(charas)} files from {datapath}', True, black)
        loading_rect = loading_text.get_rect()
        loading_rect.right = self.xres
        loading_rect.bottom = self.yres
        self.screen.blit(loading_text, loading_rect)
        # draw start button
        start_button = button(self.xres/2, self.yres/2, "Start", self.text_font, self.screen)
        start_button.draw(self.screen)
        pygame.display.flip()
        # wait for start press
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                elif start_button.click(event):
                    return
        # TODO: loading by selecting directory from file explorer option
        

    def draw_battle(self):
        self.screen.fill(white)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                #elif start_button.click(event):
                #    return