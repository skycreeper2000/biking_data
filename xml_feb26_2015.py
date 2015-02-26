__author__ = 'szeitlin'

from lxml import objectify

def extract_nodes(root):

    #initialize counters
    Pos_count, Alt_count = 0

    for a,act in enumerate(root.Activities.Activity):

        for lap in root.Activities.Activity[a].Lap:

            try:
                for j, lapnum in enumerate(lap):
                    if lap[j].Track is not None:
                        track_count+=1

            except AttributeError:
                continue
            try:
                if lap[j].Track.Trackpoint is not None:
                    for k, trackpt in enumerate(lap[j].Track.Trackpoint):
                        try:
                            if lap[j].Track.Trackpoint[k].Position is not None:
                                Pos_count+=1
                                posTime = lap[j].Track.Trackpoint[k].Time
                                Lat = lap[j].Track.Trackpoint[k].Position.LatitudeDegrees.pyval
                                Long = lap[j].Track.Trackpoint[k].Position.LongitudeDegrees.pyval
                        except AttributeError:
                            continue
                        try:
                            if lap[j].Track.Trackpoint[k].AltitudeMeters.text is not None:
                                Alt_count+=1
                                altTime = lap[j].Track.Trackpoint[k].Time
                                alt = lap[j].Track.Trackpoint[k].AltitudeMeters.text
                        except AttributeError:
                            continue


            except AttributeError:
                continue




path = "2014.tcx"
parsed = objectify.parse(open(path))
root = parsed.getroot()
extract_nodes(root)