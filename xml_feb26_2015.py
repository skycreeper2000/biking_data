__author__ = 'szeitlin'

from lxml import objectify

def extract_nodes(root):

    StartTime = []
    TotalTimeSeconds = []
    DistanceMeters = []
    MaximumSpeed = []
    Calories = []

    AvgSpeedList = []

    Pos_count, Alt_count = 0,0
    posTime = []
    Lat = []
    Long = []
    altTime = []
    alt = []

    for a,act in enumerate(root.Activities.Activity):

        for lap in root.Activities.Activity[a].Lap:
            StartTime.append(lap.values()[0])
            TotalTimeSeconds.append(float(lap.TotalTimeSeconds.text))
            DistanceMeters.append(float(lap.DistanceMeters.text))
            MaximumSpeed.append(float(lap.MaximumSpeed.text))
            Calories.append(float(lap.Calories.text))

            kids= lap.Extensions.getchildren()
            avgspeed = kids[1].AvgSpeed.pyval #have to do pyval to get rid of nested brackets from xml
            AvgSpeedList.append(avgspeed)

            try:
                for j, lapnum in enumerate(lap):
                    if lap[j].Track is not None:
                        try:
                            if lap[j].Track.Trackpoint is not None:

                                for k, trackpt in enumerate(lap[j].Track.Trackpoint):
                                    try:
                                        if lap[j].Track.Trackpoint[k].Position is not None:
                                            Pos_count+=1
                                            posTime.append(lap[j].Track.Trackpoint[k].Time)
                                            Lat.append(lap[j].Track.Trackpoint[k].Position.LatitudeDegrees.pyval)
                                            Long.append(lap[j].Track.Trackpoint[k].Position.LongitudeDegrees.pyval)
                                    except AttributeError:
                                        continue
                                    try:
                                        if lap[j].Track.Trackpoint[k].AltitudeMeters.text is not None:
                                            Alt_count+=1
                                            altTime.append(lap[j].Track.Trackpoint[k].Time)
                                            alt.append(lap[j].Track.Trackpoint[k].AltitudeMeters.text)
                                    except AttributeError:
                                        continue
                        except AttributeError:
                            continue

            except AttributeError:
                continue

    all_the_lists = [StartTime, TotalTimeSeconds, DistanceMeters, MaximumSpeed, Calories, AvgSpeedList, posTime, Lat, Long, altTime, alt]

    return all_the_lists

path = "2014.tcx"
parsed = objectify.parse(open(path))
root = parsed.getroot()
all_the_lists = extract_nodes(root)

print map(len, all_the_lists)
