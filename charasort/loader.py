# module for loading images from a directory and turning them into a list of chara objects
import os
import sys

import chara

#charalist = list[chara]

def load_from_datapath(datapath : str) -> list:
    ret = []
    for path, dirs, files in os.walk(datapath):
        for file in files:
            fullpath = os.path.join(path, file)
            ret.append(chara.chara(fullpath))
    return ret
