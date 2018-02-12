# water
 - sizing water distribution systems - 

 This package helps designers size water distribution systems. It is based on 
 the energy equatation, and common fluid dynamics equations and assumptions.

 Modules:
 Tank:
 Create a tank of diameter and height. You can specify freeboard, deadstorage and elevation.
 Use to calculate storage requirements (Equalizing, Standby and Operating)

 Fittings:
 Create fittings to calculate minor losses. Specify kind, style, size and schedule (default 40)
 To calculate K value you need to specify a Reynolds number 

 Pumps:
 Create pump object. Uses mfg's pump curve data from csv file. Plots curve using polynomial regression
 TO DO:
 plot vfd speed curves
 plot system curve (constant pressure)
 create new curve --> creates csv file and saves it to pumps folder
 calculates run cost with efficiencies
