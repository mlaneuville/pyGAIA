#!/usr/bin/python

from SIMULATION__DEFINE import *
from OUTPUT__DEFINE import *
from GRID__DEFINE import *

import matplotlib.pyplot as plt

#from data import *
import mpl_toolkits.mplot3d.axes3d as p3
import sys
import numpy as np
import os
import yaml

# TODO: this is very dangerous
np.seterr(all='ignore')

if len(sys.argv) != 2:
	print "not enought arguments"
	print "usage: "+str(sys.argv[0])+" <run_folder>"
	sys.exit(0)

folder = sys.argv[1]

os.chdir(base_folder)

try:
    stream = file(folder+"/parameters.yaml")
except IOError:
    print "Cannot find parameters file in  "+folder
    sys.exit()

data = yaml.load(stream)

moon_radius = data["moon_radius"]
core_radius = data["core_radius"]
mantle_diffusivity = data["mantle_diffusivity"]
temperature_scale = data["temperature_scale"]
temperature_offset = data["temperature_offset"]

s = Simulation(folder)
g = Grid(s.grid)

#o = s.getAtOutput(1)
#f = o.getField('T')
#r, t = g.getProfile(f.data, 90, 180)
#plt.plot(r, t)
#plt.show()

time_evo = []
core_evo = []
tcmb_evo = []

for i in range(1, s.nOutputs+1):
    o = s.getAtOutput(i)
    f = o.getField('T')
    vel = o.getField('v')
    sol = o.getField('s')
    evo = o.getField('E')

    vx = np.array(vel.data)[0::3]
    vy = np.array(vel.data)[1::3]

    X, Y, T = g.getSlice(f.data, 2)
    X, Y, S = g.getSlice(sol.data, 2)
    
    X, Y, U = g.getSlice(vx, 2)
    X, Y, V = g.getSlice(vy, 2)
    
    Z = T*temperature_scale + temperature_offset
    M = T - S
    
    meltzone = T > S
    M[T > S] = 1.
    M[T < S] = np.ma.masked
    
    fig, ax = plt.subplots(figsize=(8,8))

    levels = np.linspace(250, 2000, 50)
    CS = plt.contourf(X, Y, Z, levels)
    CS2 = plt.contourf(X, Y, M, colors='white')
    
    #cbar = plt.colorbar(CS2, use_gridspec=True)
    #cbar.ax.set_ylabel('Temperature [-]')
    
    core = plt.Circle((0,0), 0.234, color='k')
    surf = plt.Circle((0,0), 1.234, color='k', fill=False)
    
    fig.gca().add_artist(core)
    fig.gca().add_artist(surf)
    
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.axis('off')
    
    speed = np.sqrt(U*U + V*V)
    if speed.max():
        lw = 2*speed/speed.max()
        ax.streamplot(X, Y, U, V, color='k', linewidth=lw, arrowstyle='-')
    
    D = moon_radius - core_radius
    kappa = mantle_diffusivity
    Ga = 1e9*365.25*24*3600
    time = o.time*D**2/kappa/Ga

    plt.text(0., 1., "Time: %3.2f Ga" % time, transform=ax.transAxes)
    plt.savefig("vis/T-slice-%03d.png" % (i-1), transparent=True)

    time_evo.append(time)
    core_evo.append(evo.data[0]*core_radius/1e3)
    tcmb_evo.append(f.data[0]*temperature_scale + temperature_offset)

    plt.figure()
    plt.plot(time_evo, core_evo, 'k', lw=2)
    plt.xlabel("Time [Ga]")
    plt.ylabel("Core size [km]")
    plt.grid()
    plt.savefig("vis/core-size-evolution.png", transparent=True)

    plt.figure()
    plt.plot(time_evo, tcmb_evo, 'k', lw=2)
    plt.xlabel("Time [Ga]")
    plt.ylabel("Core Temperature [K]")
    plt.grid()
    plt.savefig("vis/core-temperature-evolution.png", transparent=True)

#fig = plt.figure()
#ax = p3.Axes3D(fig)
#
#idx = np.nonzero(pow(np.array(g.x),2)+pow(np.array(g.y),2)+pow(np.array(g.z),2)<pow(g.innerRadius,2))
#ax.scatter(np.array(g.x)[idx[0]],np.array(g.y)[idx[0]],np.array(g.z)[idx[0]],c='k') 
#
#TT = np.array(f.data)
#SS = np.array(sol.data)
#idx = np.nonzero(TT-SS > 0)
#ax.scatter(np.array(g.x)[idx[0]],np.array(g.y)[idx[0]],np.array(g.z)[idx[0]]) 
#
#ax.set_zlim3d(-1,1)
#ax.set_ylim3d(-1,1)
#ax.set_xlim3d(-1,1)
#plt.savefig("meltzone.png")
