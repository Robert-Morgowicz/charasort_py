# chara class module; for individual chara objects and their representative image
import os
import pygame

class chara:
    def __init__(self,filename):
        # extract name from filename
        raw_name = os.path.basename(filename).split(".")[0]
        # decompose name into components and capitalize each
        spaced_name = raw_name.replace("_"," ")
        list_name = spaced_name.split(" ")
        cap_name = list(map(lambda x: x.capitalize(), list_name))
        # recombine string and store
        acc = ""
        for name_part in cap_name:
            acc = acc + " " + name_part
        self.name = acc
        self.image = pygame.image.load(filename)
        # NOTE: "tied" is not true for all charas in a tie.  For any tie, there is a representative chara
        # and a set of charas tied with the representative.  The representitive hase tied = false, and
        # holds the tie's placement relative to other charas.  All "tied" charas appear directly after their
        # representative
        self.tied = False

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"

    def print(self):
        print(str(self))