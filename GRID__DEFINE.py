#!/usr/bin/python
#
# class Grid
#		(r,profile) getProfile(field,theta,phi)
#		(x,y,field) getSlice(field,axis)
#		void outputInfo()
#
# Author: M. Laneuville -- laneuville@ipgp.fr
# Last update: 31/05/2012

from TOOLS__DEFINE import *		# contains tools to read binary files
from data import *						# global variables for pyGAIA
#from pylab import *						# linspace, griddata
#from math import *						# acos & cie
from math import sqrt
import numpy as np
from numpy import arccos
from numpy import arctan2
from matplotlib.mlab import griddata

class	Grid:

	def __init__(self,filename,init=0):

		f_in = open(grid_folder+filename,'rb')
		tmp = f_in.read(12)
		self.isASCII = (tmp[9]=='A')
		self.is2D = (tmp[3]=='2')

		self.innerRadius = read_db(f_in)
		self.outerRadius = read_db(f_in)
		self.resolution = read_db(f_in)
		self.nShells = read_int(f_in)
		self.nCells = 0

		self.x = []
		self.y = []
		self.z = []
		for i in range(self.nShells):
			n_elem = read_int(f_in)
			self.nCells = self.nCells + n_elem
			for j in range(n_elem):
				self.x.append(read_db(f_in))
				self.y.append(read_db(f_in))
				self.z.append(read_db(f_in))

		f_in.close()

		if init:
			print "Loading "+filename
			self.outputInfo()

	def getProfile(self,data,theta,phi):
		print theta,phi
		cellsPerShell = self.nCells/self.nShells	
		profile = []
		radius = []
		for j in range(self.nShells):
			r = []
			th = []
			ph = []
			d = []
			for i in range(cellsPerShell):
				id = j*cellsPerShell+i
				r.append(sqrt( pow(self.x[id],2) + pow(self.y[id],2) + pow(self.z[id],2) ))
				th.append(arccos( self.z[id]/r[i] ))
				ph.append(arctan2( self.y[id], self.x[id] ))
				d.append(data[id])
			th_regrid = np.linspace(0,np.pi,180)
			ph_regrid = np.linspace(-np.pi, np.pi,360)
			Z = griddata(th,ph,d,th_regrid,ph_regrid, interp='linear')
			profile.append(Z[phi,theta])
			radius.append(r[-1])
		return radius, profile




	def getSlice(self,data,axis,res=600):

		if axis==0:
			xi = np.linspace(min(self.y),max(self.y),res)
			yi = np.linspace(min(self.z),max(self.z),res)
			index = np.nonzero(abs(np.array(self.x)) < 1e-2)
			x = np.array(self.y)[index[0]]
			y = np.array(self.z)[index[0]]
		if axis==1:
			xi = np.linspace(min(self.z),max(self.z),res)
			yi = np.linspace(min(self.x),max(self.x),res)
			index = np.nonzero(abs(np.array(self.y)) < 1e-8)
			x = np.array(self.z)[index[0]]
			y = np.array(self.x)[index[0]]
		if axis==2:
			xi = np.linspace(min(self.x),max(self.x),res)
			yi = np.linspace(min(self.y),max(self.y),res)
			index = np.nonzero(abs(np.array(self.z)) < 1e-8)
			x = np.array(self.x)[index[0]]
			y = np.array(self.y)[index[0]]

		d = np.array(data)[index[0]]
		Z = griddata(x,y,d,xi,yi, interp='linear')

		X, Y = np.meshgrid(xi,yi)
		#idx = nonzero( pow(array(X),2)+pow(array(Y),2) < pow(self.innerRadius,2))
		#Z[idx[0]]=0.0

		return X,Y,Z

	def outputInfo(self):
		print "\tisASCII = "+str(self.isASCII)
		print "\tis2D = "+str(self.is2D)
		print "\tinnerRadius = "+str(self.innerRadius)
		print "\touterRadius = "+str(self.outerRadius)
		print "\tresolution = "+str(self.resolution)
		print "\tnShells = "+str(self.nShells)
		print
