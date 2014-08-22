__author__ = 'szeitlin'

#helper script to designate allowed range for grouping

def delta_range(delta):
    '''
        Takes a delta and applies it to generate a reference list for grouping items.

    (int) --> list of ints (except zero)

        >>> delta_range(2)
        [-1, 1]
        >>> delta_range(10)
        [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]
        >>> delta_range(6)
        [-3, -2, -1, 1, 2, 3]

    '''
    half = delta//2
    right = [x for x in range(1, half+1)]
    left = [-x for x in range(1, half+1)]
    left.reverse()
    both = left + right
    return both

import doctest
doctest.testmod()
