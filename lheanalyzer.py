#!/usr/bin/env python

import re

from commons import Particle

class LHEFileFormatError(Exception):
    def __init__(self, filename,line):
        self.line = line
        self.filename = filename
    def __str__(self):
        return repr("Error in LHE File "+self.filename+" in line "+str(self.line))
       
class Event:
    def __init__(self,initstr):
        """Constuctor call with line from lhe file"""
        ls=initstr.split()
        self.nParticles,self.processId,self.weight,self.scale,self.QEDCoupling,self.QCDCoupling=int(ls[0]),int(ls[1]),float(ls[2]),float(ls[3]),float(ls[4]),float(ls[5])
        self.particles=[]
    def addParticle(self,particle):
        """adds a particle to the event"""
        self.particles.append(particle)

class Process:
    def __init__(self,initstr):
        ls=initstr.split()
        self.crossSection,self.crossSectionUncertainty,self.maxWeight,self.id=float(ls[0]),float(ls[1]),float(ls[2]),int(ls[3])
        

class LHEFile:
    def __init__(self, filename):
        self.filename=filename
        self.fp = open(filename,"r")
        self.lineCounter=0
        for line in self.fp:
            self.lineCounter+=1
            if line.strip()=="<init>": break
    def __iter__(self):
        return self
    def next(self):
        for line in self.fp:
            self.lineCounter+=1
            if line[0]!="#":
                return line
                break
        self.fp.close()
                
class LHEAnalysis:
    """Iterator for looping over a sequence backwards."""
    def __init__(self, filename):
        self.lhefile=LHEFile(filename)

	line=self.lhefile.next()
	ls = line.split()
	try:
            self.beamId ,self.beamEnergy,self.PDFAuthor,self.PDFSet,self.weightSwitch,self.nProcesses=[int(ls[0]),int(ls[1])],[float(ls[2]),float(ls[3])],[int(ls[4]),int(ls[5])],[int(ls[6]),int(ls[7])],int(ls[8]),int(ls[9])
        except (ValueError, IndexError):
            raise LHEFileFormatError(self.lhefile.filename,self.lhefile.lineCounter)
	self.processes=[]
	for i in range(self.nProcesses):
            line=self.lhefile.next()
            try:
                self.processes.append(Process(line))
            except (ValueError, IndexError):
                raise LHEFileFormatError(self.lhefile.filename,self.lhefile.lineCounter)
      
    def __iter__(self):
        return self
    def next(self):
        beginevent=False
        for line in self.lhefile:
            if line==None:
                raise StopIteration
                return
            if re.match("<event[a-zA-Z0-9_ ='-]*>", line): 
                beginevent=True
                break
        if beginevent is False:
            raise StopIteration
        initline=self.lhefile.next()
        event=Event(initline)
        for line in self.lhefile:
            if line.strip()=="</event>" or line.strip()=="<mgrwt>":
                break
            try:
                particle = Particle(line)
            except (ValueError, IndexError):
                raise LHEFileFormatError(self.lhefile.filename,self.lhefile.lineCounter)
            event.addParticle(particle)
        #for line in self.lhefile:
        #    if re.match("<rscale>", line) :
        #        #print line
        #        temp =line.split()[2] 
        #        #print 'scale?: ', line.split()[2]
        #        temp = temp[0:temp.find('</')] 
        #        #print temp
        #        rscale = float(temp)
        #        event.rscale = rscale 
        #    else :
        #        break
        return event
    totalCrossSection = property(lambda self: sum(p.crossSection for p in self.processes))
