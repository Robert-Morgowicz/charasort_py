# module for loading images from a directory and turning them into a list of chara objects
import os
import sys

import chara

#charalist = list[chara]

def load_from_datapath(datapath : str) -> list:
    ret = []
    for file in os.listdir(datapath):
        ret.append(chara.chara(file))
    return ret
