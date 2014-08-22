__author__ = 'szeitlin'

#compare to dictionary for sorting

def centering(both, mid, name):
    '''
    :param both: list. output of the delta_range function.
    mid = middle of the range, name: the key for the dictionary
    :return: a dictionary

    >>> centering([-1,1], 7, 'morning')
    {'morning': [6, 8, 7]}
    '''
    #apply the delta_range to get the range around the middle
    centered = [mid+x for x in both] + [mid]
    entry = dict([[name,centered],])
    return entry

def dict_grower(entry):
    '''
    :param named: Takes the output of multiple runs of centering() and combines them
    :return: a bigger dict

    >>> dict_grower('morning':[6,7,8], 'afternoon':[12,13,14,15,16,17,18])
    {morning:[6,7,8], afternoon:[12,13,14,15,16,17,18]
    '''
    categories = {}

    categories.update(entry)

    return categories


# def hour_lookup():
#     '''
#     (list of ints) -> (two lists of ints)
#
#     Takes a list of ints, compares them to a dictionary, and then writes them to
#     two lists.
#
#     >>> hour_lookup([6,7,12,15,18])
#     morning = [6, 7]
#     afternoon = [12, 15, 18]
#     '''
#     pass

import doctest
doctest.testmod()
