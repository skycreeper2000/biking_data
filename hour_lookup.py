__author__ = 'szeitlin'

#compare to dictionary for sorting
categories = {}

def centering(both, mid, name):
    '''
    :param both: list. (Output of the delta_range function.)
    mid = middle of the range, name: the key for the dictionary
    :return: a dictionary

    >>> centering([-1,1], 7, 'morning')
    {'morning': [6, 8, 7]}
    '''
    #apply the delta_range to get the range around the middle
    centered = [mid+x for x in both] + [mid]
    entry = dict([[name,centered],])
    return entry

def dict_grower(entry, categories):
    '''
    :param named: Takes the output of multiple runs of centering() and combines them
    :return: a bigger dict

    >>> dict_grower({'morning':[6,8,7]}, {'afternoon':[12,13,14,15,16,17,18]})
    {'afternoon': [12, 13, 14, 15, 16, 17, 18], 'morning': [6, 8, 7]}
    '''

    categories.update(entry)

    return categories


def hour_lookup(hours, categories):
    '''
    (list of ints) -> (two lists of ints)

    Takes a list of ints, compares them to a dictionary ("categories"), and then writes them to
    dictionary of lists ("sorted").

    :param: hours is a list of ints
    :param: categories is a dictionary

    >>> hour_lookup([6,7,12,15,18], categories)
    {'morning':[6, 7], 'afternoon':[12, 15, 18]}
    '''
    sorted = {}

    #this sort of works but it's too hard to refer back to these without knowing what they'll be
    # for name in categories.keys():
    #     #make a new dict with that name
    #     temp1 = str(name) + "_list"
    #     temp2 = []
    #     sorted.update({temp1:temp2})
    #     print sorted

    #try something like:        ast.literal_eval("%s = <expression" % string)

    #iterate until all the hours are assigned to the sorted dict
    for num in hours:
        for timeofday, hour in categories.items():
            if num in hour:
            #append it to the list with the appropriate name
                if timeofday not in sorted:
                    sorted.update({timeofday:[num]})
                else:
                    sorted[timeofday].append(num)
    #print sorted

    return sorted

# import doctest
# doctest.testmod()

#note that doctests are tricky for dicts, and are sensitive to any errors in spacing! yuck.

hour_lookup([6,7,12,15,18], {'afternoon': [12, 13, 14, 15, 16, 17, 18], 'morning': [6, 8, 7]})
