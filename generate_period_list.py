
# coding: utf-8


#a short script to generate the list of months
#months = pandas.PeriodIndex([pandas.Period('2013-01'), pandas.Period('2013-02')... pandas.Period('2013-12')])

def make_months(year):
    '''
    Function to generate list of months, to speed up period indexing in pandas time series data.
    year -> list of str (year-month)
    make_months('2013')
    ['2013-01', '2013-02'... '2013-12']
    '''

    twelfth = []

    for item in (range(1,13)):
        item = str(item)
        if len(item) < 2:
            item = '0' + item
        twelfth.append(item)

    months = []

    for item in twelfth:
        months.append(str(year) + '-' + item)    #convert this to join

return months




