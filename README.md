<p align="center">
<img width="200" height="200" src="https://hasemar.github.io/water/documentation/html/_static/water_small.png">
</p>
<p style="text-align: center;">A python package for water system engineers</p>

This package is intended to help engineers with common engineering tasks when designing and
working with municipal water systems. Units are in US industry standard.

See the documentation for this package at: https://hasemar.github.io/water

## Installing / Getting started

**Requirements**  
Most classes and functions just use the standard built-in libraries for Python 3.5+. However, the Pumps class uses the following and are required in order to use it.
 
* numpy 
* matplotlib

Once you have forked the repository you can add the directory to your PYTHONPATH.  
Go into `.profile` in your home directory (or create one if you do not have one), and add the following:  

```bash
#set PYTHONPATH to recognize water package in github directory
if [ -d "/home/<user>/<directory_name>/water" ] ; then
    export PYTHONPATH=$PYTHONPATH:/home/<user>/<directory_name>/water
fi 
```
Be sure to change the path name to where ever you have the repo saved.  

If using on Windows, you can add the repository path to the environment variable PYTHONPATH. 

## Contributions

If you would like to help in the development of this package contributions are welcome!  
Please see the [contributing](contributions.md) guidlines!

**A bit of background** 

I am a water systems engineer that was looking for an easier way to do my day to day calculations. I am not a professional programmer by any means. If you have any suggestions on how to improve the code, make this more useful and more robust, I'm all ears!

Here are some things I am working on (slowly):  
I am currently pulling fitting and pipe data from a dictionary above the Pipe class. I am pretty sure that is not kosher, but it was a way to get it working. I would like to move the pipe and fittings data into a sqlite database. I have done this with the Pumps class and you will see some methods in the Pipes class relating to db handling that are currently not in use. As I worry through this transition it is becoming apparent that I should have a db handling class so I am not repeating code in my Pipe and Pump class. 

Currently units are in US *water industry standard* units. This package may be more useful if units could be specified.

I would like to create a water quality class that would perform concentration, filter bed area, contact time, and other water quality related calculations.

## Features

Check out the [examples and tutorials](https://hasemar.github.io/water/documentation/html/tutorial.html) page of the documentation for a better description. 

These are the different modules in this package:     

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
## Links  
- Project homepage: https://hasemar.github.io/water/
- Repository: https://github.com/hasemar/water/
- Issue tracker: https://github.com/hasemar/water/issues
  - In case of sensitive bugs like security vulnerabilities, please contact
    hasemar@gmail.com directly instead of using issue tracker. We value your effort
    to improve the security and privacy of this project!
## Licensing

"The code in this project is licensed under MIT license."