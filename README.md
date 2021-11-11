# water
 - water is a python package tailored for water system engineering - 

 This package helps engineers with common engineering tasks when designing and
 working with municipal water systems. Units are in US industry standard.

 Modules:
 Tank:
 Create a tank of diameter and height and shape. You can specify freeboard, deadstorage and elevation partitions.
 Use to calculate storage requirements (Equalizing, Standby and Operating)

 Pumps:
 Create pump object. Uses mfg's pump curve data saved in a sqlite db with the ability to add to the db. Curves can be plotted with or without efficiency curve, with applied affinity laws and with multiple parallel pumps. 

 Pipe:  
 Create pipe objects with length and diameter. Apply a flow to get head loss. Fittings can be added to the pipe object to get minor losses.

 Genset:
 Create a generator object and apply resistive and inductive loads to get aid in genset size.

 Tools:
 collection of functions used throughout the Classes and also can be used as needed separately. 
