#!/usr/bin/python
#
# class Simulation
#		Output getAtOutput(int)
#		void outputInfo()
#
# Author: M. Laneuville -- laneuville@ipgp.fr
# Last update: 31/05/2012

from OUTPUT__DEFINE import *		# defines the Output object
import os												# needed for chdir
import fnmatch									# needed for filter
import operator									# itemgetter

class Simulation:

    def __init__(self, dir):

        print "Loading directory "+dir
        print
        # be careful if you have files with "PX_OUT" in their names and that are not outputs
        files = fnmatch.filter(os.listdir(dir),'PX_OUT*')
        self.nOutputs = len(files)
        # we are now in the run's folder
        os.chdir(dir)
        
        self.outputs = []
        for f in files:
            # init parameter allows us to create a minimal Output object, just to read time & iter
            o = Output(f, init=len(self.outputs)+1)
            self.outputs.append([o.time, int(o.iter), o.filename])
        
        self.grid = o.gridname
        self.outputs.sort(key=operator.itemgetter(0))
        
        self.OutputInfo()

    def getAtOutput(self, iter):
        # iter is the iter-th output here, not the iteration number at the end of the file
        # in my case it goes from 0 to 90
        return Output(self.outputs[iter-1][2])

    def OutputInfo(self):
        print "Simulation covers "
        print "\t"+str(self.nOutputs)+" output files"
        print "\t"+str(self.outputs[-1][1])+" iterations"
        print "\tmax sim time of "+str(self.outputs[-1][0])
        print
