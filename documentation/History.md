The history is a buffer of sorts which stores state information between steps of the sort

There are one of two ways to implement history: either

1. Store the full state of the lists

2. store transaction information for each action

at each step, store the elt moved, it's src list, and its dest list, the greater indecies

when undoing, walk back through the history, doing inverse operations and resetting the greater indecies until your reach the first non-auto action
