# water distribution design package in Python 

from Water.tanks import Tank
from Water.fittings import Fitting
from Water.pumps import Pump
from Water.pipe import Pipe
import Water.tools as tools

__all__ = ['Tank', 'Fitting', 'Pump', 'Pipe', 'tools']


## turn fittings class into subclass of Pipe, then you can inherently add fittings to sections
## in a standard format like you did in ftw_injection