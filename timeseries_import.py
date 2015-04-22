__author__ = 'szeitlin'

import pandas

def data_cleanup(list_of_lists):
    """
    Prepare a dataframe from a list of lists.

    :param list_of_lists:
    :return: pandas dataframe
    """

    seriously = map(pandas.Series, list_of_lists)

    #round is a pandas method

    sigfigs = map(round(4), seriously)

    df = pandas.concat(sigfigs, axis=1)

    return df


