
import collections 
import pandas
from lxml import etree as ET #this was missing from 'python for data analysis' example
from lxml import objectify

print pandas.__version__

path = "2013_xml.tcx"
parsed = objectify.parse(open(path))
root = parsed.getroot()

#kids = root.Activities.Activity.Lap.Extensions.getchildren()
#root.Activities.Activity.Lap.descendantpaths()
#upper_field = ['Id','Lap']
#middle_field = ['TotalTimeSeconds', 'DistanceMeters', 'MaximumSpeed', 'Calories']
#extensions = ['AvgSpeed']

timestamps = []

count = 0 #count laps
TotalTimeSeconds = [] 
DistanceMeters = []
MaximumSpeed = []
Calories = []
AvgSpeedList = []

for activity in root.Activities.Activity:
    timestamps.append(activity.Id) #this comes out to fewer - not one per lap (?) 
    for lap in activity.Lap:
        #print dir(lap)    #to get all the elements
        #print lap.getchildren()
        #print lap.Extensions
        #print child.tag
        #print timestamps
        count +=1                
        TotalTimeSeconds.append(lap.TotalTimeSeconds.text)
        DistanceMeters.append(lap.DistanceMeters.text)
        MaximumSpeed.append(lap.MaximumSpeed.text)
        Calories.append(lap.Calories.text)
        
        kids= lap.Extensions.getchildren()
        avgspeed = kids[1].AvgSpeed
        print avgspeed
        AvgSpeedList.append(avgspeed)
	#AvgSpeedList.append(kids[1].AvgSpeed)

print count
print type(AvgSpeedList), type (MaximumSpeed)

#print len(timestamps), len(TotalTimeSeconds), len(DistanceMeters), len(MaximumSpeed), len(Calories), len(AvgSpeedList)

TotalTimeSeconds = pandas.Series(TotalTimeSeconds)
DistanceMeters = pandas.Series(DistanceMeters)
MaximumSpeed = pandas.Series(MaximumSpeed)
Calories = pandas.Series(Calories)
AverageSpeed = pandas.Series(AvgSpeedList)

print AverageSpeed

df = pandas.concat([TotalTimeSeconds, DistanceMeters, MaximumSpeed, Calories, AverageSpeed], axis=1)

#df.head()

#df.shape

df.columns = ['TotalTimeSeconds', 'DistanceMeters', 'MaximumSpeed', 'Calories', 'AverageSpeed']

df.describe()

#get rid of those extra brackets in AverageSpeed column - don't quite understand where they're coming from (?)


#get rid of extra decimal places


#df.to_csv("parsed_2013.csv")




