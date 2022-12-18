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
global redo_buffer
global game_window

def query_compare(chara1 : chara, chara2 : chara, history, redo_buffer, battle_no):
    # if there's history, allow the undo
    # if there's redo_buffer allow the redo

    # draw the battle screen
    global game_window
    game_window.draw_battle()
    battle_no = battle_no + 1
    # return one_won, winner
    return True, chara1

def sort(charas : list) -> list:
    # TODO: tracking history
    global history
    global redo_buffer
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
    history = [(list_of_lists, next_of_lists, [])]
    redo_buffer = []
    # track number of battles
    battle_no = 1
    # until we have a full sorted list
    while len(list_of_lists[0]) < startlen:
        # base case: if we reach the end of the list of lists, it's time for another round
        if ind1 == len(list_of_lists) or ind2 == len(list_of_lists):
            list_of_lists = next_of_lists
            next_of_lists = []
        # name source lists and initialize dest list
        charas1 = list_of_lists[ind1]
        charas2 = list_of_lists[ind2]
        next_charas = [] 
        # while neither list is empty
        while charas1 and charas2:
            # base case, if one list empties, append the rest of the other
            if not charas1:
                next_charas.append(charas2)
                charas2 = []
            elif not charas2:
                next_charas.append(charas1)
                charas1 = []
            # if either first chara is tied to a prior chara, put it into the next list
            # and continue until there are no tied charas
            elif charas1[0].tied:
                next_charas.append(charas1[0])
                charas1.pop(0)
            elif charas2[0].tied:
                next_charas.append(charas2[0])
                charas2.pop(0)
            else: 
                one_won, winner = query_compare(charas1[0], charas2[0], history, redo_buffer, battle_no)
                next_charas.append(winner)
                if one_won:
                    charas1.pop(0)
                else:
                    charas2.pop(0)
        # append and increment indecies        
        next_of_lists.append(next_charas)
        ind1 = ind1 + 2
        ind2 = ind2 + 2
    
    return next_of_lists[0]

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
    if args.debug:
        debug = True
    if args.seed:
        random.seed(args.seed)
    if args.resolution:
        [xres, yres] = args.resolution.splittext("x")
    else:
        xres = 1280
        yres = 720
    global game_window
    game_window = window.window(xres, yres)
    game_window.draw_loading(args.datapath)
    # load images and construct charas in list of charas
    charas = loader.load_from_datapath(args.datapath)
    game_window.draw_start(charas, args.datapath)
    # sort the list of charas
    sorted_charas = sort(charas)
    # display results screen
    display_result(sorted_charas)


if __name__ == "__main__":
    main()


