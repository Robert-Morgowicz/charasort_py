# functions for pygame interraction with the game window
import sys
import enum

import pygame

import chara

# colors
black = 0, 0, 0
grey = 200, 200, 200
l_green = 150, 255, 150
red = 255, 0, 0
white = 255, 255, 255

# button actions for battle screen
class Action(enum.Enum):
    QUIT        = 0
    LEFT_WIN    = 1
    RIGHT_WIN   = 2
    TIE         = 3
    UNDO        = 4
    REDO        = 5
    AUTO        = 6
    APPEND      = 7
    APPEND_PASS = 8
    NEW_ROUND   = 9

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
                    if self.active:
                        return True

class charabutton(button):
    def __init__(self, x, y, width, height, text_plus, font, screen, chara, active=True):
        text = chara.name
        super().__init__(x, y, width, height, text, font, screen, active)
        # how much space to give the text below
        self.text_plus = text_plus
        # scale image to fit box, preserving dimensions
        img_width = chara.image.get_rect().width
        img_height = chara.image.get_rect().height
        x_bleed = (img_width - width) / img_width
        y_bleed = (img_height - height) / img_height
        if x_bleed > 0 or y_bleed > 0:
            # x will bleed over more, truncate by x dimension
            if x_bleed >= y_bleed:
                y_proportional = int((width / img_width) * img_height)
                self.image = pygame.transform.smoothscale(chara.image, (width, y_proportional))
            # y will bleed over more
            else:
                x_proportional = int((height / img_height) * img_width)
                self.image = pygame.transform.smoothscale(chara.image, (x_proportional, height))
        else:
            self.image = chara.image

    def draw(self):
        # superborder
        superborder_rect = self.rect.copy()
        superborder_rect.height = superborder_rect.height + self.text_plus
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
        # draw borders last
        # border
        pygame.draw.rect(self.screen, black, self.rect, width=1, border_radius=0)
        pygame.draw.rect(self.screen, black, superborder_rect, width=1, border_radius=0)


class window:
    def __init__(self, xres, yres):
        pygame.init()
        pygame.display.set_caption("charasort")
        self.screen = pygame.display.set_mode((xres, yres))
        self.xres = xres
        self.yres = yres
        self.title_font = pygame.font.SysFont("arial", int(yres/10))
        self.subtitle_font = pygame.font.SysFont("arial", int(yres/16))
        self.text_font = pygame.font.SysFont("arial", int(yres/20))
        self.list_font = pygame.font.SysFont("arial", int(yres/52))
        self.xgrid = [int((i / 16) * xres) for i in range(16)]
        self.ygrid = [int((i / 16) * yres) for i in range(16)]

    def loading(self, datapath):
        # white out screen
        self.screen.fill(white)
        # draw loading message
        loading_text = self.text_font.render("Sorts are preparing.  Please wait warmly...", True, black)
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
        title_rect.center = (self.xgrid[8], self.ygrid[2])
        self.screen.blit(title_text, title_rect)
        subtitle_text = self.subtitle_font.render("a.k.a charasort", True, black)
        subtitle_rect = subtitle_text.get_rect()
        subtitle_rect.center = (self.xgrid[8], self.ygrid[4])
        self.screen.blit(subtitle_text, subtitle_rect)
        # draw loading text
        loading_text = self.text_font.render(f"loaded {len(charas)} files from {datapath}", True, black)
        loading_rect = loading_text.get_rect()
        loading_rect.right = self.xres
        loading_rect.bottom = self.yres
        self.screen.blit(loading_text, loading_rect)
        # draw start button
        start_button = button(self.xgrid[8], self.ygrid[8], self.xgrid[2], self.ygrid[1], "Start", self.text_font, self.screen)
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

    def draw_guarded(self, charas1, charas2):
        i = 1
        while i < len(charas1) and i < 2:
            if charas1[i].tied:
                guarded_chara_text = self.text_font.render(f"Tied: {charas1[i].name}", True, grey)
            else:
                guarded_chara_text = self.text_font.render(f"Guards: {charas1[i].name}", True, black)
            guarded_chara_rect = guarded_chara_text.get_rect()
            guarded_chara_rect.center = self.xgrid[4], self.ygrid[14+i]
            self.screen.blit(guarded_chara_text, guarded_chara_rect)
            i = i + 1
        i = 1
        while i < len(charas2) and i < 2:
            if charas2[i].tied:
                guarded_chara_text = self.text_font.render(f"Tied: {charas2[i].name}", True, grey)
            else:
                guarded_chara_text = self.text_font.render(f"Guards: {charas2[i].name}", True, black)
            guarded_chara_rect = guarded_chara_text.get_rect()
            guarded_chara_rect.center = self.xgrid[12], self.ygrid[14+i]
            self.screen.blit(guarded_chara_text, guarded_chara_rect)
            i = i + 1

    def battle(self, charas1 : list, 
                     charas2 : list, 
                     can_undo : bool, 
                     can_redo : bool, 
                     battle_no : int,
                     expect_no : int,
                     show_guarded : bool) -> Action:
        # draw battle screen
        self.screen.fill(white)
        # battle No.
        battle_no_text = self.subtitle_font.render(f"Battle #{battle_no}", True, black)
        battle_no_rect = battle_no_text.get_rect()
        battle_no_rect.left = 0
        battle_no_rect.top = 0
        self.screen.blit(battle_no_text, battle_no_rect)
        # progress bar
        decimal = battle_no / expect_no
        percent = int(decimal * 100)
        progress_border = pygame.Rect((self.xgrid[1], self.ygrid[1]), (self.xgrid[-2], self.ygrid[1]))
        progress_bar = pygame.Rect((self.xgrid[1], self.ygrid[1]), (int(decimal * self.xgrid[-2]), self.ygrid[1]))
        progress_text = self.text_font.render(f"{percent}%", True, black)
        progress_rect = progress_text.get_rect()
        progress_rect.center = progress_border.center
        pygame.draw.rect(self.screen, l_green, progress_bar, width=0, border_radius=0)
        pygame.draw.rect(self.screen, black, progress_border, width=1, border_radius=0)
        self.screen.blit(progress_text, progress_rect)
        # character selects
        chara1_button = charabutton(self.xgrid[4], self.ygrid[8], self.xgrid[5], self.ygrid[11], self.ygrid[1], self.text_font, self.screen, charas1[0])
        chara2_button = charabutton(self.xgrid[12], self.ygrid[8], self.xgrid[5], self.ygrid[11], self.ygrid[1], self.text_font, self.screen, charas2[0])
        chara1_button.draw()
        chara2_button.draw()
        # characters guarding info
        if show_guarded:
            self.draw_guarded(charas1, charas2)
        # action buttons
        tie_button  = button(self.xgrid[8], self.ygrid[3], self.xgrid[2], self.ygrid[1], "Tie", self.text_font, self.screen)
        undo_button = button(self.xgrid[8], self.ygrid[5], self.xgrid[2], self.ygrid[1], "Undo", self.text_font, self.screen, can_undo)
        redo_button = button(self.xgrid[8], self.ygrid[7], self.xgrid[2], self.ygrid[1], "Redo", self.text_font, self.screen, can_redo)
        tie_button.draw()
        undo_button.draw()
        redo_button.draw()
        pygame.display.flip()
        # covered Characters
        # TODO
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

    def result(self, sorted_charas):
        l_height = int(self.yres/52)
        half_xgrid = int(self.xres/32)
        display_images = 3
        true_index = 0
        display_index = 1
        display_y = l_height
        xgrid_pos = 1
        display_x = self.xgrid[1]
        self.screen.fill(white)
        while true_index < len(sorted_charas):
            chara = sorted_charas[true_index]
            # only update index if not tied
            if not chara.tied:
                display_index = true_index + 1
            # show character image
            if true_index < display_images:
                pass
                # make a rect to get the center
                reference_rect = pygame.Rect((display_x, display_y), (self.xgrid[2],  (9 * l_height)))
                (x_center, y_center) = reference_rect.center
                # construct charabutton
                entry = charabutton(x_center, y_center, self.xgrid[2],  (9 * l_height), l_height, self.list_font, self.screen, chara)
                # display charabutton
                entry.draw()
                # draw index border
                index_border_rect = pygame.Rect((display_x - half_xgrid, display_y), (half_xgrid, 10 * l_height))
                pygame.draw.rect(self.screen, black, index_border_rect, width=1, border_radius=0)
                # draw index
                index_text = self.list_font.render(f"{display_index}", True, black)
                index_rect = index_text.get_rect()
                index_rect.center = index_border_rect.center
                self.screen.blit(index_text, index_rect)
                # increment display y
                display_y = display_y + (10 * l_height)
            # just name
            else:
                pass
                # draw border
                border_rect = pygame.Rect((display_x, display_y), (self.xgrid[2], l_height))
                pygame.draw.rect(self.screen, black, border_rect, width=1, border_radius=0)
                # draw name
                name_text = self.list_font.render(f"{chara.name}", True, black)
                name_rect = name_text.get_rect()
                name_rect.center = border_rect.center
                self.screen.blit(name_text, name_rect)
                # draw index border
                index_border_rect = pygame.Rect((display_x - half_xgrid, display_y), (half_xgrid, l_height))
                pygame.draw.rect(self.screen, black, index_border_rect, width=1, border_radius=0)
                # draw index
                index_text = self.list_font.render(f"{display_index}", True, black)
                index_rect = index_text.get_rect()
                index_rect.center = index_border_rect.center
                self.screen.blit(index_text, index_rect)
                # increment display y
                display_y = display_y + l_height
            # update to next column
            if display_y >= (self.yres - l_height):
                xgird_pos = xgrid_pos + 3
                display_x = self.xgrid[xgrid_pos]
                display_y = l_height
            true_index = true_index + 1
        
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
