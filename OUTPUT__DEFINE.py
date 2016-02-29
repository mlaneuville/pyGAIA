#!/usr/bin/python
#
# class Output
#		Field getField
#
# Author: M. Laneuville -- laneuville@ipgp.fr
# Last update: 31/05/2012

from TOOLS__DEFINE import *			# contains a list of tools
from GRID__DEFINE import *			# definition of the Grid object
from FIELD__DEFINE import *			# definition of the Field object

class	Output:

    def __init__(self,file,init=0):

        if not init:
            print "Loading "+file

        f_in = open(file,'rb')
        tmp = f_in.read(6)				# GP_OUT
        tmp = read_int(f_in)			# size of the grid filename
        
        tmp = f_in.read(tmp)			# grid filename, has to be parsed to get rid of the path
        self.gridname = tmp.rsplit('/')[-1]
        
        tmp = read_db(f_in)
        self.time = tmp
        
        self.iter = file.rsplit('_',1)[-1]
        self.filename = file
        
        if init==1:
           	g = Grid(self.gridname,init=1)
        if init!=0:
            return
        
        g = Grid(self.gridname)

        # starts reading the data
        self.fieldCount = 0
        self.fields = []
        self.fieldNames = []
        id = f_in.read(1)
        while id and (id != 'I'):
            field = []
            n_elem = read_int(f_in)
            # vpe = values per elements (1 for scalar field, 3 for vector field)
            # but doesn't change the way we store the data at the moment
            vpe = int(float(n_elem) / g.nCells)
            print "\treading "+id+" with VPE = "+str(vpe)
            for i in range(n_elem):
            	field.append(read_db(f_in))
            
            self.fields.append(field)
            self.fieldNames.append(id) 
            self.fieldCount += 1
            
            id = f_in.read(1)
        
        print 
        f_in.close()

    def getField(self, id):
        for i,name in enumerate(self.fieldNames):
            if id == name:
                id = i
                break
        return Field(id, self.fields[i])
