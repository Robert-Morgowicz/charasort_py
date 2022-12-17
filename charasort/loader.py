# module for loading images from a directory and turning them into a list of chara objects
import os
import sys

import chara

def load_from_datapath(datapath : str) -> list[chara]:
    ret = []
    for file in os.listdir(datapath):
        filename = os.basename(file)
        ret.append(chara(filename))
