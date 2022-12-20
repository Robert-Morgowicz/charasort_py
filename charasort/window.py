# functions for pygame interraction with the game window
import sys
import enum

import pygame

import chara

# colors
black = 0, 0, 0
grey = 200, 200, 200
red = 255, 0, 0
white = 255, 255, 255

# button actions for battle screen
class Action(enum.Enum):
    QUIT      = 0
    LEFT_WIN  = 1
    RIGHT_WIN = 2
    TIE       = 3
    UNDO      = 4
    REDO      = 5

class button:
    def __init__(self, x, y, width, height, text, font, screen, active=True):
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = x, y
        self.screen = screen
        self.text = text
        self.font = font
        self.active = active

    def draw(self):
        pygame.draw.rect(self.screen, black, self.rect, width=1, border_radius=0)
        text_obj = None
        if self.active:
            text_obj = self.font.render(self.text, True, black)
        else:
            text_obj = self.font.render(self.text, True, grey)
        text_rect = text_obj.get_rect()
        text_rect.center = self.rect.center
        self.screen.blit(text_obj, text_rect)

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    return True

class charabutton(button):
    def __init__(self, x, y, width, height, font, screen, chara):
        text = chara.name
        super().__init__(x, y, width, height, text, font, screen)
        # scale image to fit box, preserving dimensions
        img_width = chara.image.get_rect().width
        img_height = chara.image.get_rect().height
        x_bleed = img_width - (width - 2)
        y_bleed = img_height - (height - 2)
        if x_bleed > 0 or y_bleed > 0:
            # x will bleed over more, truncate by x dimension
            if x_bleed > y_bleed:
                y_proportional = int(((width - 2) / img_width) * img_height)
                self.image = pygame.transform.smoothscale(chara.image, (width - 2, y_proportional))
            # y will bleed over more
            else:
                x_proportional = int(((height - 2) / img_height) * img_width) + 2
                self.image = pygame.transform.smoothscale(chara.image, (x_proportional, height - 2))
        else:
            self.image = self.image

    def draw(self):
        # border
        pygame.draw.rect(self.screen, black, self.rect, width=1, border_radius=0)
        # superborder
        superborder_rect = self.rect.copy()
        superborder_rect.height = superborder_rect.height + 50
        pygame.draw.rect(self.screen, black, superborder_rect, width=1, border_radius=0)
        # character image
        img_rect = self.image.get_rect()
        img_rect.center = self.rect.center
        self.screen.blit(self.image, img_rect)
        # character name
        text_obj = self.font.render(self.text, True, black)
        lower_rect = pygame.Rect((self.rect.left, self.rect.bottom), (self.rect.width, superborder_rect.height - self.rect.height))
        text_rect = text_obj.get_rect()
        text_rect.center = lower_rect.center
        self.screen.blit(text_obj, text_rect)


class window:
    def __init__(self, xres, yres):
        pygame.init()
        pygame.display.set_caption("charasort")
        self.screen = pygame.display.set_mode((xres, yres))
        self.title_font = pygame.font.SysFont("arial", 64)
        self.subtitle_font = pygame.font.SysFont("arial", 48)
        self.text_font = pygame.font.SysFont("arial", 32)
        self.xres = xres
        self.yres = yres

    def loading(self, datapath):
        # white out screen
        self.screen.fill(white)
        # draw loading message
        loading_text = self.title_font.render("Sorts are preparing.  Please wait warmly...", True, black)
        loading_rect = loading_text.get_rect()
        loading_rect.right = self.xres
        loading_rect.bottom = self.yres
        self.screen.blit(loading_text, loading_rect)
        # TODO: display individual files loaded as text
        pygame.display.flip()

    def start(self, charas: list, datapath: str):
        # draw title text
        self.screen.fill(white)
        title_text = self.title_font.render("Open Character Sorter", True, black)
        title_rect = title_text.get_rect()
        title_rect.center = (self.xres / 2, 100)
        self.screen.blit(title_text, title_rect)
        subtitle_text = self.subtitle_font.render("a.k.a charasort", True, black)
        subtitle_rect = subtitle_text.get_rect()
        subtitle_rect.center = (self.xres / 2, 150)
        self.screen.blit(subtitle_text, subtitle_rect)
        # draw loading text
        loading_text = self.text_font.render(f"loaded {len(charas)} files from {datapath}", True, black)
        loading_rect = loading_text.get_rect()
        loading_rect.right = self.xres
        loading_rect.bottom = self.yres
        self.screen.blit(loading_text, loading_rect)
        # draw start button
        start_button = button(self.xres / 2, self.yres / 2, 100, 50, "Start", self.text_font, self.screen)
        start_button.draw()
        pygame.display.flip()
        # wait for start press
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif start_button.click(event):
                    return
        # TODO: loading by selecting directory from file explorer option

    def battle(self, chara1 : chara, 
                     chara2 : chara, 
                     can_undo : bool, 
                     can_redo : bool, 
                     battle_no : int) -> Action:
        # draw battle screen
        self.screen.fill(white)
        # battle No.
        battle_no_text = self.subtitle_font.render(f"Battle #{battle_no}", True, black)
        battle_no_rect = battle_no_text.get_rect()
        battle_no_rect.left = 0
        battle_no_rect.top = 0
        self.screen.blit(battle_no_text, battle_no_rect)
        # progress bar
        # TODO
        # character selects
        chara1_button = charabutton(self.xres / 4, self.yres / 2, self.xres / 3, 6 * self. yres / 8, self.text_font, self.screen, chara1)
        chara2_button = charabutton(3 * (self.xres / 4), self.yres / 2, self.xres / 3, 6 * self. yres / 8, self.text_font, self.screen, chara2)
        chara1_button.draw()
        chara2_button.draw()
        # action buttons
        tie_button  = button(self.xres / 2, self.yres / 8, 100, 50, "Tie", self.text_font, self.screen)
        undo_button = button(self.xres / 2, self.yres / 4, 100, 50, "Undo", self.text_font, self.screen, can_undo)
        redo_button = button(self.xres / 2, 3 * (self.yres / 8), 100, 50, "Redo", self.text_font, self.screen, can_redo)
        tie_button.draw()
        undo_button.draw()
        redo_button.draw()
        pygame.display.flip()
        # wait for user action
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif chara1_button.click(event):
                    return Action.LEFT_WIN
                elif chara2_button.click(event):
                    return Action.RIGHT_WIN
                elif tie_button.click(event):
                    return Action.TIE
                elif undo_button.click(event):
                    return Action.UNDO
                elif redo_button.click(event):
                    return Action.REDO

    def result():
        pass