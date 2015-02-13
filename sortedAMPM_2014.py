
# coding: utf-8

#get_ipython().magic(u'reload_ext watermark')

#get_ipython().magic(u'watermark -a "Samantha Zeitlin" -d -u -p ipython,pandas,seaborn')

import argparse

import numpy as np
import pandasql
import pandas
from datetime import datetime, date, time
from dateutil.parser import parse
import pytz

import matplotlib.pyplot as plt
import matplotlib 
import seaborn as sns

#get_ipython().magic(u'matplotlib inline')

parser = argparse.ArgumentParser()
parser.add_argument('-i','--input', help='input csv file name', required=True)
#add argument here for whether there's an index column already or not
parser.add_argument('-o', '--output', help='file name for zoned, flagged, filtered csv', required=True)
#consider adding additional arguments here for the names of morning and evening suburb output files?

args=parser.parse_args()
myfile = args.input
zonedfile = args.output

#import into pandas
df = pandas.read_csv(myfile, index_col=0)


#for testing: put in some checks re: what you expect, i.e. df.head()
# for testing: check size df.shape


#convert datetimes to something useful
df['parsed']=[parse(x) for x in df['StartTime']]

#for testing: df['parsed'].head()

df['zoned'] = [x.astimezone(pytz.timezone('US/Pacific')) for x in df['parsed']]

#for testing: df['zoned'].head()

df['hour']=[x.hour for x in df['zoned']]

#for testing: df['hour'].head()
#for testing: df.head()

#for testing: df['hour'].std()

#sns.set_palette("deep", desat=0.6)
# sns.set_context(rc={"figure.figsize": (8,4)})
#
#
# df['hour'].hist() #note that these are not normal distributions, so not well suited for machine learning
# plt.xlabel('hour of the day(correct timezone)')
# plt.ylabel('frequency')


#convert distances to miles
df['Miles'] = df['DistanceMeters']/1609.34

#convert times to minutes (better for comparisons) and hours (better for speed calculations)
df['Minutes'] = df['TotalTimeSeconds']/60
df['Trip_hours'] = df['Minutes']/60

#convert speeds to miles per hour
df['average_mph'] = df['Miles']/df['Trip_hours']
df['maximum_mph'] = df['MaximumSpeed']*3600/1609.34

#tests for all of these conversions: df.head()

sorted_by_time_and_date = df.sort_index(by = ['hour', 'zoned'])

#check sorting: sorted_by_time_and_date.head()

#remove artifactual outliers (i.e. when bike computer still collecting data after train starts moving, or after getting a flat tire)

speed_filter_left = sorted_by_time_and_date[sorted_by_time_and_date['average_mph'] <= 40.0]
speed_filter_right=speed_filter_left[speed_filter_left['average_mph']>=5.0]

filtered=speed_filter_right.reset_index()

#sns.distplot(filtered['average_mph'])

# sns.set(style="ticks")
# sns.jointplot("hour", "average_mph", data=filtered)


#want to flag hours to use later as categorical colors on plots 
def leg_definer(hour):
    """Helper function to identify trip legs by hour, i.e.
    6 AM: first leg (to Caltrain) - morning_city
    7 AM: second leg (to Oracle) - morning_suburb
    4 PM (16): 3rd leg (return to Caltrain) - evening_suburb
    5 PM (17): 4th leg (return home) - evening_city
    other hour: other
    
    >>> leg_definer(6):
    'morning_city'
    
    (int) -> (str)
    """
    legref = {6:"morning_city", 7:"morning_suburb", 16:"evening_suburb", 17:"evening_city", 9:"other", 11:"other", 12:"other", 15:"other", 18:"evening_later"}
    return legref[hour]


# apply flags and create new columns for those
filtered['leg_flag']=[leg_definer(hour) for hour in filtered['hour']]

filtered['zoned'] = filtered['zoned'].apply(pandas.to_datetime)

filtered['month'] = [item.month for item in filtered['zoned']]

filtered['day'] = [item.day for item in filtered['zoned']]

filtered['weekday']=[item.weekday() for item in filtered['zoned']]

# g = sns.lmplot("day", "average_mph", filtered, hue="leg_flag", fit_reg=False)
# g.set(xticks=[0,5,10,15,20,25,30], ylim=(5,24))

# for testing: filtered.head()

# sns.set_context("talk")
# g=sns.lmplot("weekday", "average_mph", filtered, hue="leg_flag", x_jitter=0.15, fit_reg=False)
# g.set(xlim=(-1,6), ylim=(5,24))


# f, ax= plt.subplots()
# sns.violinplot(filtered['average_mph'], filtered['weekday'])



# write out
filtered.to_csv(zonedfile)



morning_suburb = filtered[filtered['leg_flag'] == 'morning_suburb']

# for testing: morning_suburb.weekday.value_counts()

#try this to be able to add titles
from matplotlib.font_manager import FontProperties
#from pylab import *

# f, ax= plt.subplots()
# g = sns.violinplot(morning_suburb['average_mph'], morning_suburb['weekday'])
# title('Morning Suburb')
# sns.despine()
# #g.set(ylim=(5,30))


evening_suburb=filtered[filtered['leg_flag']=='evening_suburb']


# for testing: evening_suburb.weekday.value_counts()

# write those out
evening_suburb.to_csv("evening_suburb_2014.csv", index_col=0)
morning_suburb.to_csv("morning_suburb_2014.csv", index_col=0)


# f, ax= plt.subplots()
# g = sns.violinplot(evening_suburb['average_mph'], evening_suburb['weekday'])
# g.set(ylim=(10,24))
# title('Evening Suburb')
# sns.despine()



# f, ax= plt.subplots()
# g = sns.violinplot(evening_suburb['average_mph'], evening_suburb['weekday'], color="Blues")#, alpha=0.7)
# g = sns.violinplot(morning_suburb['average_mph'], morning_suburb['weekday'], color="Yellow")# alpha=0.3)
# g.set(ylim=(10,24))
# title('Morning(yellow) vs. Evening(blue) Suburb')
# sns.despine()



