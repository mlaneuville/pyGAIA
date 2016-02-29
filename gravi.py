#!/usr/bin/local/python

from SIMULATION__DEFINE import *
from OUTPUT__DEFINE import *
from GRID__DEFINE import *

import sys
import os
import data
import spharm_tools
import numpy as np

# load r, theta, phi, temperature, velocity_r, viscosity
folder = sys.argv[1]
os.chdir(data.base_folder)
s = Simulation(folder)
g = Grid(s.grid)

o = s.getAtOutput(91)

T = o.getField('T')
v = o.getField('v')
visc = o.getField('V')

r = [sqrt(g.x[i]**2 + g.y[i]**2 + g.z[i]**2) for i in range(len(g.x))]
th = [arccos(g.z[i]/r[i]) for i in range(len(g.x))]
ph = [arctan2(g.y[i], g.x[i]) for i in range(len(g.x))]

# -----------------------------
#   topography at CMB
# -----------------------------

# compute tau_rr at CMB
tau_rr = visc[nonzero(r == min(r))]*v[nonzero(r== min(r))]
# expand tau_rr as SH

# -----------------------------
#   topography at surface
# -----------------------------

# compute tau_rr at surface
# expand tau_rr as SH
