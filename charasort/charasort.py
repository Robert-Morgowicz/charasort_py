# main program module.  Contains main method and the sorting algorithm
# default libraries
import os
import random
import time
import argparse
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

def query_compare(charas1, 
                  charas2, 
                  list_of_lists,
                  next_of_lists,
                  next_charas,):
    global game_window
    global history
    global history_len
    global redo_buffer
    global battle_no
    global debug
    # if there's history, allow the undo
    allow_undo = (history != [])
    # if there's a redo_buffer allow the redo
    allow_redo = (redo_buffer != [])
    # record current state as history
    if debug:
        print(f"battle #{battle_no}")
        print(list_of_lists)
        print(next_of_lists)
        print(next_charas)
    history.append((list_of_lists, next_of_lists, next_charas))
    if len(history) > history_len:
        history.pop(0)
    # draw the battle screen
    action = game_window.battle(charas1[0], charas2[0], allow_undo, allow_redo, battle_no)
    match action:
        case window.Action.LEFT_WIN:
            battle_no = battle_no + 1
            next_charas.append(charas1[0])
            charas1.pop(0)
            # invalidate redo
        case window.Action.RIGHT_WIN:
            battle_no = battle_no + 1
            next_charas.append(charas2[0])
            charas2.pop(0)
            # invalidate redo
        case window.Action.TIE:
            battle_no = battle_no + 1
            charas2[0].tied = True
            next_charas.append(charas1[0])
            charas1.pop(0)
            # invalidate redo
        case window.Action.UNDO:
            battle_no = battle_no - 1
        case window.Action.REDO:
            battle_no = battle_no + 1
            list_of_lists, next_of_lists, next_charas = redo_buffer[0]
            redo_buffer.pop(0)
    return

def sort(charas : list) -> list:
    # TODO: tracking history
    global battle_no
    global debug
    # starting length for loop control
    startlen = len(charas)
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
                next_of_lists.append(list_of_lists[ind1])
            if debug:
                print("base case")
            list_of_lists = next_of_lists
            ind1 = 0
            ind2 = 1
            next_of_lists = []
            continue
        # name source lists and initialize dest list
        charas1 = list_of_lists[ind1]
        charas2 = list_of_lists[ind2]
        next_charas = [] 
        # while neither list is empty
        while charas1 or charas2:
            # base case, if one list empties, append the rest of the other
            if not charas1:
                next_charas = next_charas + charas2
                charas2.clear()
            elif not charas2:
                next_charas = next_charas + charas1
                charas1.clear()
            # if either first chara is tied to a prior chara, put it into the next list
            # and continue until there are no tied charas
            elif charas1[0].tied:
                next_charas.append(charas1[0])
                charas1.pop(0)
            elif charas2[0].tied:
                next_charas.append(charas2[0])
                charas2.pop(0)
            else: 
                query_compare(charas1, 
                              charas2, 
                                  list_of_lists,
                                  next_of_lists,
                                  next_charas)
        # append and increment indecies        
        next_of_lists.append(next_charas)
        #if debug:
        #    print("next:")
        #    print(next_of_lists)
        #   print(list_of_lists)
        ind1 = ind1 + 2
        ind2 = ind2 + 2
    
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


