
# coding: utf-8

# In[1]:

get_ipython().magic(u'reload_ext watermark')


# In[3]:

get_ipython().magic(u'watermark -a "Samantha Zeitlin" -d -u -p ipython,pandas,seaborn')


# In[1]:

import numpy as np
import pandasql
import pandas
from datetime import datetime, date, time
from dateutil.parser import parse
import pytz
from delta_range import delta_range
from hour_lookup import centering, dict_grower, hour_lookup

import matplotlib.pyplot as plt
import matplotlib 
import seaborn as sns

get_ipython().magic(u'matplotlib inline')


# In[2]:

df = pandas.read_csv("sorted_by_date_2014.csv", index_col=0)


# In[3]:

df.head()


# In[4]:

df.shape


# In[5]:

type(df['StartTime'][0])


# In[8]:

#ideas: could just take times, ignore days (not sure how many will be identical, probably not many)
#could convert times back & use a bag-of-words approach to count occurrences(for that could maybe do hours +/-1)
df['parsed']=[parse(x) for x in df['StartTime']]


# In[9]:

df['parsed'].head()


# In[10]:

df['zoned'] = [x.astimezone(pytz.timezone('US/Pacific')) for x in df['parsed']]


# In[11]:

df['zoned'].head()


# In[12]:

df['hour']=[x.hour for x in df['zoned']]


# In[13]:

df['hour'].head()


# In[14]:

df.head()


# In[18]:

#want to know the variation of hours to know how to set the delta_range for what to include, probably easiest to plot & look  
df['hour'].std()


# In[19]:

import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import numpy as np

sns.set_palette("deep", desat=0.6)
sns.set_context(rc={"figure.figsize": (8,4)})

get_ipython().magic(u'matplotlib inline')


# In[20]:

df['hour'].hist() #note that these are not normal distributions, so not well suited for machine learning 
plt.xlabel('hour of the day(correct timezone)')
plt.ylabel('frequency')


# In[21]:

morning_range = delta_range(2)
print morning_range


# In[22]:

afternoon_range = delta_range(6)
print afternoon_range


# In[23]:

first = centering(morning_range, 7, 'morning')


# In[24]:

categories = {}
second = centering(afternoon_range, 15, 'afternoon')


# In[25]:

dict_grower(first, categories)
dict_grower(second, categories)


# In[26]:

hour = df['hour'].tolist()


# In[27]:

daytimes = hour_lookup(hour, categories )
print(daytimes),


# In[15]:

#convert distances to miles 
df['Miles'] = df['DistanceMeters']/1609.34

#convert times to minutes (better for comparisons) and hours (better for speed calculations)
df['Minutes'] = df['TotalTimeSeconds']/60
df['Trip_hours'] = df['Minutes']/60

#convert speeds to miles per hour
df['average_mph'] = df['Miles']/df['Trip_hours']
df['maximum_mph'] = df['MaximumSpeed']*3600/1609.34


# In[16]:

df.head()


# In[17]:

#actually just want to add a column with a flag for daytime category, and sort by that. Or, could sort by hours... 
sorted_by_hours= df.sort_index(by='hour')


# In[31]:

sorted_by_hours.head()


# In[18]:

sorted_by_time_and_date = df.sort_index(by = ['hour', 'zoned'])


# In[33]:

sorted_by_time_and_date.head()


# In[19]:

speed_filter_left = sorted_by_time_and_date[sorted_by_time_and_date['average_mph'] <= 40.0]


# In[20]:

speed_filter_right=speed_filter_left[speed_filter_left['average_mph']>=5.0]


# In[21]:

filtered=speed_filter_right.reset_index()


# In[37]:

sns.distplot(filtered['average_mph'])


# In[38]:

sns.set(style="ticks")
sns.jointplot("hour", "average_mph", data=filtered)


# In[22]:

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


# In[23]:

filtered['leg_flag']=[leg_definer(hour) for hour in filtered['hour']]


# In[24]:

filtered['zoned'] = filtered['zoned'].apply(pandas.to_datetime)


# In[25]:

filtered['month'] = [item.month for item in filtered['zoned']]


# In[26]:

filtered['day'] = [item.day for item in filtered['zoned']]


# In[27]:

g = sns.lmplot("day", "average_mph", filtered, hue="leg_flag", fit_reg=False)
g.set(xticks=[0,5,10,15,20,25,30], ylim=(5,24))


# In[28]:

#really want to group by month and plot that way, or by day of the week, and compare those
filtered['weekday']=[item.weekday() for item in filtered['zoned']]


# In[46]:

filtered.head()


# In[40]:

sns.set_context("talk")
g=sns.lmplot("weekday", "average_mph", filtered, hue="leg_flag", x_jitter=0.15, fit_reg=False)
g.set(xlim=(-1,6), ylim=(5,24))


# In[41]:

f, ax= plt.subplots()
sns.violinplot(filtered['average_mph'], filtered['weekday'])


# In[31]:

filtered.to_csv("zoned_flagged_filtered_2014.csv")


# In[42]:

morning_suburb= filtered[filtered['leg_flag']=='morning_suburb']


# In[43]:

morning_suburb.weekday.value_counts()


# In[44]:

#try this to be able to add titles
from matplotlib.font_manager import FontProperties
from pylab import *


# In[45]:

f, ax= plt.subplots()
g = sns.violinplot(morning_suburb['average_mph'], morning_suburb['weekday'])
title('Morning Suburb')
sns.despine()
#g.set(ylim=(5,30))


# In[46]:

evening_suburb=filtered[filtered['leg_flag']=='evening_suburb']


# In[47]:

evening_suburb.weekday.value_counts()


# In[48]:

evening_suburb.head()


# In[49]:

evening_suburb.to_csv("evening_suburb_2014.csv", index_col=0)
morning_suburb.to_csv("morning_suburb_2014.csv", index_col=0)


# In[51]:

f, ax= plt.subplots()
g = sns.violinplot(evening_suburb['average_mph'], evening_suburb['weekday'])
g.set(ylim=(10,24))
title('Evening Suburb')
sns.despine()


# In[52]:

f, ax= plt.subplots()
g = sns.violinplot(evening_suburb['average_mph'], evening_suburb['weekday'], color="Blues")#, alpha=0.7)
g = sns.violinplot(morning_suburb['average_mph'], morning_suburb['weekday'], color="Yellow")# alpha=0.3)
g.set(ylim=(10,24))
title('Morning(yellow) vs. Evening(blue) Suburb')
sns.despine()


# In[75]:

filtered.set_index(['StartTime'], inplace=True)


# In[98]:

filtered.head()


# In[77]:


days = filtered.resample('B')


# In[6]:

get_ipython().magic(u'install_ext https://raw.githubusercontent.com/szeitlin/watermark/master/watermark.py')


# In[52]:

#previous year (matplotlib)
fig, axes=plt.subplots(nrows=2, ncols=3)

set_time['Calories'].plot(kind='bar', ax=axes[0,0]); axes[0,0].set_title('Calories')
set_time['maximum_mph'].plot(kind='bar', ax=axes[0,1]); axes[0,1].set_title('max speed(mph)')
set_time['average_mph'].plot(kind='bar', ax=axes[0,2]); axes[0,2].set_title('avg speed(mph)')
set_time['Miles'].plot(kind='bar', ax=axes[1,0]); axes[1,0].set_title('Miles')
set_time['Minutes'].plot(kind='bar', ax=axes[1,1]); axes[1,1].set_title('Minutes')
plt.tight_layout() #required to keep x-axis labels & titles from overlapping


# In[ ]:

#not sure what group by is doing here- is that the average, the max, some random number-? 

