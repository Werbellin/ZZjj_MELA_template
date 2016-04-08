#!/usr/bin/env python

import re
import ROOT

import math

def delta_phi(part1, part2) :
    pt_sort = by_pt([part1, part2])
    phi1 = pt_sort[0].phi
    phi2 = pt_sort[1].phi

    dphi = phi1 - phi2
    dphi = math.acos(math.cos(dphi))
    return (dphi)

#    if dphi > math.pi :
#        dphi = abs(2 * math.pi - dphi)
#
#    return dphi

def by_pt(aList) :
    return sorted(aList, key=lambda particle: particle.pt, reverse = True)

def removeFromList(list_a, list_b) :
    output = []
    for b in list_b :
        if b not in list_a :
            output.append(b)
    return output

class Particle:
    """Describes a single particle"""

    def __init__(self, properties, const1 = None, const2 = None, isJet = False, index = -1) :
        """Constructor where properties = (PDGID, px, py, pz, energy, mass) """
        
        # for constructor from LHE
        if isinstance(properties, basestring) :
        
            
            ls = properties.split()
            self.pdgId,self.status,self.mother, self.color,self.momentum,self.lifetime,self.spin=int(ls[0]),int(ls[1]),[int(ls[2]),int(ls[3])],[int(ls[4]),int(ls[5])],[float(ls[6]),float(ls[7]),float(ls[8]),float(ls[9]),float(ls[10])],float(ls[11]),float(ls[12])

        # and from flat NTUPLE
        if isinstance(properties[1], ROOT.TLorentzVector) :
            #print 'Lorentz! :)'
            self.pdgId = properties[0]
            self.index = index
            p4 = properties[1]
            #if not isJet :
            self.momentum = (p4.Px(), p4.Py(), p4.Pz(), p4.E(), p4.M())

            self.const1 = const1
            self.const2 = const2


        #print 'failed'

#        else :
#            self.pdgId = properties[0]
#            self.index = index
#            if not isJet :
#                self.momentum = (properties[1], properties[2], properties[3], properties[4], properties[5])
#            else :
#               tvec = ROOT.TLorentzVector()
#               tvec.SetPtEtaPhiE(properties[1], properties[2], properties[3], properties[4])
#               self.momentum = (tvec.Px(), tvec.Py(), tvec.Pz(), properties[4],  properties[5])
#            self.const1 = const1
#            self.const2 = const2


    def getTLorentzVector(self):
        """Returns the ROOT TLorentzVector of the particle"""
        return ROOT.TLorentzVector(self.momentum[0],self.momentum[1],self.momentum[2],self.momentum[3])
    px = property(lambda self: self.momentum[0])
    py = property(lambda self: self.momentum[1])
    pz = property(lambda self: self.momentum[2])
    e = property(lambda self: self.momentum[3])

    energy = property(lambda self: self.momentum[3])
    mass = property(lambda self: self.momentum[4])
    pt = property(lambda self: (self.px**2+self.py**2)**0.5)
    tLorentzVector = property(getTLorentzVector)
    p4 = tLorentzVector
    eta = property(lambda self: self.tLorentzVector.Eta())
    phi = property(lambda self: self.tLorentzVector.Phi())
    rap = property(lambda self: self.tLorentzVector.Rapidity())


    def __add__(self, other) :
        if isinstance(other, ROOT.TLorentzVector) :
            print 'is lvec'
            return self.getTLorentzVector() + other
        else :
            return self.getTLorentzVector() + other.getTLorentzVector()

    def __radd__(self, other) :
        if isinstance(other, ROOT.TLorentzVector) :
            print 'is lvec2'
            return self.getTLorentzVector() + other
        else :
            return self.getTLorentzVector() + other.getTLorentzVector()


class LorentzVector:
    def __init__(self,momentum):
        self.px=momentum[0]
        self.py=momentum[1]
        self.pz=momentum[2]
        self.energy=momentum[3]
    def add(self,p):
        self.energy+=p.energy
        self.px+=p.px
        self.py+=p.py
        self.pz+=p.pz
    def invariantMass(self):
        return (self.energy**2-self.px**2-self.py**2-self.pz**2)**0.5
        
   
def dR_p4(p1, p2) :
    return ((p1.Eta()-p2.Eta())**2 + (p1.Phi() - p2.Phi())**2 )**0.5

def dR(p1, p2) :
    return ((p1.p4.Eta()-p2.p4.Eta())**2 + (p1.p4.Phi() - p2.p4.Phi())**2 )**0.5


def invariantMass(p0,*particles):
    l0=LorentzVector(p0.momentum)
    for p in particles:
        l0.add(LorentzVector(p.momentum))
    return l0.invariantMass()
def transverseMass(p0,p1):
    import ROOT
    from math import cos
    l0=p0.tLorentzVector
    l1=p1.tLorentzVector
    return (l0.Et()**2+l1.Et()**2-2*l0.Et()*l1.Et()*cos(l0.DeltaPhi(l1)))**0.5
