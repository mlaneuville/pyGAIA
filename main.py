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

# TODO: this is very dangerous
np.seterr(all='ignore')

if len(sys.argv) != 2:
	print "not enought arguments"
	print "usage: "+str(sys.argv[0])+" <run_folder>"
	sys.exit(0)

folder = sys.argv[1]

os.chdir(base_folder)

s = Simulation(folder)
g = Grid(s.grid)

#o = s.getAtOutput(1)
#f = o.getField('T')
#r, t = g.getProfile(f.data, 90, 180)
#plt.plot(r, t)
#plt.show()

for i in range(1, s.nOutputs+1):
    o = s.getAtOutput(i)
    f = o.getField('T')
    vel = o.getField('v')
    sol = o.getField('s')
    
    vx = np.array(vel.data)[0::3]
    vy = np.array(vel.data)[1::3]

    X, Y, T = g.getSlice(f.data, 2)
    X, Y, S = g.getSlice(sol.data, 2)
    
    X, Y, U = g.getSlice(vx, 2)
    X, Y, V = g.getSlice(vy, 2)
    
    Z = T
    M = T - S
    
    meltzone = T > S
    M[T > S] = 1.
    M[T < S] = np.ma.masked
    
    fig, ax = plt.subplots(figsize=(8,8))

    levels = np.linspace(0, 1.1, 50)
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
    
    D = 1410e3
    kappa = 1e-6
    Ga = 1e9*365.25*24*3600

    plt.text(0., 1., "Time: %3.2f Ga" % (o.time*D**2/kappa/Ga), transform=ax.transAxes)
    plt.savefig("vis/T-slice-%03d.png" % (i-1), transparent=True)

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
