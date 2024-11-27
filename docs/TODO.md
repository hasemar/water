Need to turn the chem pump sizing into a Class in the Water package

There are a few things that need fixing in the Pipe Class, review.
Also add more things to the pipe class (maybe utilize the sqlite db)
Add AC pipe to parameter data
Add search parameters to available pumps method in pump class - (just look at target flow and target head and list pumps within a certain tolerance from those values)
Fix pipe fittings naming - should match db??
Create a way to see fitting choices.  DB???
Round to whatever base you need - good for MDD design val
def myround(x, base=25):
    return int(base * round(float(x)/base))

It would be awesome to create a python toolbox for ArcPro that integrates the Water package. That way you could pull pumps, tanks and pipes from the GIS to load the parameters for calculations.

Need to add hydrant flow calc in python class (tools?)

Engineering Calc templates - more structured design process that enables all engineers to use the same platform

Create a template folder for water things
