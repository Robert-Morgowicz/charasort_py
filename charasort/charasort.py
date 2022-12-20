# main program module.  Contains main method and the sorting algorithm
# default libraries
import os
import random
import time
import argparse
import math
# 3rd party libraries
import pygame
# this project libraries
import chara
import loader
import window

global debug
global history
global history_len
global redo_buffer
global game_window
global battle_no
# must be global for undo functionality
global list_of_lists
global next_of_lists
global next_charas

class history_entry():
    def __init__(self, user, src_list, dest_list, action, ind1, ind2, tied=None):
        self.user = user
        self.src_list = src_list
        self.dest_list = dest_list
        self.action = action
        self.ind1 = ind1
        self.ind2 = ind2
        self.tied = tied

    def redo(self):
        match self.action:
            case window.Action.RIGHT_WIN:
                # move the element back
                self.dest_list.append(self.src_list[0])
                self.src_list.pop(0)
            case window.Action.LEFT_WIN:
                # move the element back
                self.dest_list.append(self.src_list[0])
                self.src_list.pop(0)
            case window.Action.TIE:
                # as above but unset tie
                self.dest_list.append(self.src_list[0])
                self.src_list.pop(0)
                self.tied.tied = True
            case window.Action.REDO:
                pass
            case window.Action.UNDO:
                pass
            case window.Action.AUTO:
                # move the element back
                self.dest_list.append(self.src_list[0])
                self.src_list.pop(0)
            case window.Action.APPEND:
                self.dest_list.append(self.src_list)
                self.ind1 = self.ind1 + 2
                self.ind2 = self.ind2 + 2
                global next_charas
                next_charas = []
            case window.Action.APPEND_PASS:
                self.dest_list.append(self.src_list[ind1].copy())
                self.src_list[ind1].clear()
            case window.Action.NEW_ROUND:
                global list_of_lists
                global next_of_lists
                list_of_lists = next_of_lists
                next_of_lists = []
                self.ind1 = 0
                self.ind2 = 2
        return self.ind1, self.ind2

    def inverse(self):
        match self.action:
            case window.Action.RIGHT_WIN:
                # move the element back
                self.src_list.insert(0, self.dest_list[-1])
                self.dest_list.pop(-1)
            case window.Action.LEFT_WIN:
                # move the element back
                self.src_list.insert(0, self.dest_list[-1])
                self.dest_list.pop(-1)
            case window.Action.TIE:
                # as above but unset tie
                self.src_list.insert(0, self.dest_list[-1])
                self.dest_list.pop(-1)
                self.tied.tied = False
            case window.Action.REDO:
                pass
            case window.Action.UNDO:
                pass
            case window.Action.AUTO:
                # move the element back
                self.src_list.insert(0, self.dest_list[-1])
                self.dest_list.pop(-1)
            case window.Action.APPEND:
                self.src_list = self.dest_list[-1]
                self.dest_list.pop(-1)
                global next_charas
                next_charas = self.src_list
            case window.Action.APPEND_PASS:
                self.src_list[self.ind1] = self.dest_list[-1]
                self.dest_list.pop(-1)
            case window.Action.NEW_ROUND:
                global list_of_lists
                global next_of_lists
                list_of_lists = self.src_list
                next_of_lists = self.dest_list
                
        return self.ind1, self.ind2

    def __repr__(self):
        return f"User:{self.user}, Action:{self.action}"


            

def set_state():
    pass

def query_compare(ind1, ind2, expect_no):
    global game_window
    global history
    global history_len
    global redo_buffer
    global battle_no
    global debug
    global list_of_lists
    global next_of_lists
    global next_charas
    # if there's history, allow the undo
    allow_undo = (history != [])
    # if there's a redo_buffer allow the redo
    allow_redo = (redo_buffer != [])
    # record current state as history
    if debug:
        print(f"battle #{battle_no}")
        print("list of lists")
        print(list_of_lists)
        print("next_of_lists")
        print(next_of_lists)
        print("next_charas")
        print(next_charas)
        print("history")
        print(history)
        print("redo_buffer")
        print(redo_buffer)
    #if len(history) > history_len:
    #    history.pop(0)
    charas1 = list_of_lists[ind1]
    charas2 = list_of_lists[ind2]
    if not charas1:
        next_charas.append(charas2[0])
        charas2.pop(0)
        action = window.Action.AUTO
        history.append(history_entry(False, charas2, next_charas, window.Action.AUTO, ind1, ind2))
    elif not charas2:
        next_charas.append(charas1[0])
        charas1.pop(0)
        action = window.Action.AUTO
        history.append(history_entry(False, charas1, next_charas, window.Action.AUTO, ind1, ind2))
    # if either first chara is tied to a prior chara, put it into the next list
    # and continue until there are no tied charas
    elif charas1[0].tied:
        next_charas.append(charas1[0])
        charas1.pop(0)
        action = window.Action.AUTO
        history.append(history_entry(False, charas1, next_charas, window.Action.AUTO, ind1, ind2))
    elif charas2[0].tied:
        next_charas.append(charas2[0])
        charas2.pop(0)
        action = window.Action.AUTO
        history.append(history_entry(False, charas2, next_charas, window.Action.AUTO, ind1, ind2))
    else: 
        # draw the battle screen
        action = game_window.battle(charas1[0], charas2[0], allow_undo, allow_redo, battle_no, expect_no)
    match action:
        case window.Action.LEFT_WIN:
            battle_no = battle_no + 1
            next_charas.append(charas1[0])
            charas1.pop(0)
            history.append(history_entry(True, charas1, next_charas, window.Action.LEFT_WIN, ind1, ind2))
            # invalidate redo
        case window.Action.RIGHT_WIN:
            battle_no = battle_no + 1
            next_charas.append(charas2[0])
            charas2.pop(0)
            history.append(history_entry(True, charas2, next_charas, window.Action.RIGHT_WIN, ind1, ind2))
            # invalidate redo
        case window.Action.TIE:
            battle_no = battle_no + 1
            charas2[0].tied = True
            next_charas.append(charas1[0])
            charas1.pop(0)
            history.append(history_entry(True, charas1, next_charas, window.Action.TIE, ind1, ind2, tied=charas2[0]))
            # invalidate redo
        case window.Action.UNDO:
            if debug:
                print("BEGIN UNDO")
            redo_adds = []
            history.reverse()
            history_elt = history[0]
            while not history_elt.user:
                if debug:
                    print(history_elt)
                history_elt.inverse()
                history.pop(0)
                history_elt = history[0]
            if debug:
                print(history_elt)
            ind1, ind2 = history_elt.inverse()
            redo_buffer.append(history_elt)
            history.pop(0)
            history.reverse()
            battle_no = battle_no - 1
            if debug:
                print("END UNDO")
        case window.Action.REDO:
            if debug:
                print("BEGIN REDO")
            redo_elt = redo_buffer[0]
            if debug:
                print(redo_elt)
            redo_elt.redo()
            history.append(redo_elt)
            redo_buffer.pop(0)
            battle_no = battle_no + 1
            if debug:
                print("END REDO")
        case window.Action.AUTO:
            pass
    return ind1, ind2

def sort(charas : list) -> list:
    # TODO: tracking history
    global battle_no
    global history
    global debug
    global list_of_lists
    global next_of_lists
    global next_charas
    # starting length for loop control
    startlen = len(charas)
    # expeced number of battles is n * log n
    expect_no = startlen * int(math.log(startlen))
    if debug:
        print(expect_no)
    # shuffle list
    random.shuffle(charas)
    # turn list into a list of singleton lists
    list_of_lists = list(map(lambda x: [x], charas))
    # initialize loop control variables and next iteration list of lists
    ind1 = 0
    ind2 = 1
    next_of_lists = []
    # track number of battles
    battle_no = 1
    # until we have a full sorted list
    while len(list_of_lists[0]) < startlen:
        # base case: if we reach the end of the list of lists, it's time for another round
        if ind2 >= len(list_of_lists):
            # there was still one more odd-numbered list that must be carried forward to next round
            if not ind1 >= len(list_of_lists):
                next_of_lists.append(list_of_lists[ind1].copy())
                list_of_lists[ind1].clear()
                history.append(history_entry(False, list_of_lists, next_of_lists, window.Action.APPEND_PASS, ind1, ind2))
            if debug:
                print("base case")
            history.append(history_entry(False, list_of_lists, next_of_lists, window.Action.NEW_ROUND, ind1, ind2))
            list_of_lists = next_of_lists
            ind1 = 0
            ind2 = 1
            next_of_lists = []
            continue
        # name source lists and initialize dest list
        #charas1 = list_of_lists[ind1]
        #charas2 = list_of_lists[ind2]
        next_charas = [] 
        # while neither list is empty
        while list_of_lists[ind1] or list_of_lists[ind2]:
            ind1, ind2 = query_compare(ind1, ind2, expect_no)     
        
        next_of_lists.append(next_charas)
        ind1 = ind1 + 2
        ind2 = ind2 + 2
        history.append(history_entry(False, next_charas, next_of_lists, window.Action.APPEND, ind1, ind2))
    
    return list_of_lists[0]

def display_result(charas):
    pass

def main():
    # main function
    # set up argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true",
                        help="enables debug mode")
    parser.add_argument("--datapath", type=str,
                        help="the path to a directory with images to use in the sort")
    parser.add_argument("--seed", type=str,
                        help="random seed for list randomization")
    parser.add_argument("--history", type=int,
                        help="number of steps to keep as history for undo (default=1) input -1 for full history")
    parser.add_argument("--resolution", type=str,
                        help="target resolution for game window of form NNNNxMMMM")
    # parse arguments
    args = parser.parse_args()
    # enable debug mode
    global debug
    global history
    global history_len
    global redo_buffer
    history = []
    redo_buffer = []
    if args.debug:
        debug = True
    else:
        debug = False
    if args.seed:
        random.seed(args.seed)
    if args.history:
        history_len = args.history
    else:
        history_len = 1
    if args.resolution:
        [xres, yres] = args.resolution.splittext("x")
    else:
        xres = 1280
        yres = 720
    global game_window
    game_window = window.window(xres, yres)
    game_window.loading(args.datapath)
    # load images and construct charas in list of charas
    charas = loader.load_from_datapath(args.datapath)
    game_window.start(charas, args.datapath)
    # sort the list of charas
    sorted_charas = sort(charas)
    # display results screen
    display_result(sorted_charas)


if __name__ == "__main__":
    main()


