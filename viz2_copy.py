
# coding: utf-8

# In[1]:

#more/better plots
import pandas
import numpy as np
df = pandas.read_csv("parsed_2013.csv", index_col=0)


# In[2]:

#convert distances to miles 
df['Miles'] = df['DistanceMeters']/1609.34

#convert times to minutes (better for comparisons) and hours (better for speed calculations)
df['Minutes'] = df['TotalTimeSeconds']/60
df['Hours'] = df['Minutes']/60

#convert speeds to miles per hour
df['average_mph'] = df['Miles']/df['Hours']
df['maximum_mph'] = df['MaximumSpeed']*1200/1609.34

#round off to 2 decimal places
df = np.round(df, 2)


# In[3]:

import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')


# In[4]:

#%pylab #optional - makes the plot appear in a separate window 


# In[4]:

fig1 = plt.figure()
plt.rcParams['figure.figsize'] = 18, 8 #default is too small! 
df.index = [pandas.to_datetime(x) for x in df.index] 
df.to_csv("updated_2013.csv")
monthly = df.set_index(df.index).resample('M', how=len)


# In[5]:

monthly.plot(kind='area')


# In[6]:

from mpltools import style
style.use('ggplot')


# In[9]:

print style.available


# In[11]:

#try making a colormap
from mpltools import color
tencolor = color.LinearColormap('tencolor', [(0.02, 0.2, 0.4, 1), (0.4, 0.0, 0.1, 1), (0.02, 0.4, 0.02, 1) ,(0.8, 0, 0,1), (0, 0.8, 0, 1), (0, 0, 0.8, 1), (0.4, 0.4, 0, 1), (0, 0.4, 0.4, 1), (0.4, 0, 0.4, 1), (0.3, 0,0,1)])
monthly.plot(kind='area', cmap=tencolor)


# In[ ]:



