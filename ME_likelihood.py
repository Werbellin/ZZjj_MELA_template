import os
import operator
import importlib

import sys
# this is a somewhat stupid trick to add the lhapdf python interface
sys.path.append('/usr/local/lib/python2.7/site-packages')
import lhapdf


from ROOT import TLorentzVector


def get_matrices(subprocess_dir, param_card = None) :
    print subprocess_dir
    print os.listdir(subprocess_dir)
    files = [f for f in os.listdir(subprocess_dir) if os.path.isdir(os.path.join(subprocess_dir, f))]
    #print 'files:', files

    matrices = {}

#    files = [f for f in files if f.find("udx_epemmupmumudx") > 2]
#    print files

    for f in files :
        matrices[f] = importlib.import_module("%s.%s.matrix2py"%(subprocess_dir.replace('/', '.'), f))

    for k, v in matrices.iteritems() :
        v.initialise('/Users/pigard/MG5_aMC_v2_3_3/zzjj_2e2mujj_qcd_fortran/Cards/param_card.dat')
#    print matrices
    return matrices

def invert_momenta(p):
        """ fortran/C-python do not order table in the same order"""
        new_p = []
        for i in range(len(p[0])): new_p.append([0]*len(p))
        for i, onep in enumerate(p):
            for j, x in enumerate(onep):
                new_p[j][i] = x
        return new_p

parton_dict = {'g' : 0, 'd' : 1, 'u' : 2, 's' : 3, 'c' : 4, 'b' : 5, 't' : 6}

def get_parton_flavor(subprocess) :
    incoming = subprocess[3:]
    incoming = incoming[:incoming.find('_')]
    #print incoming
    partons = []
    for i, c in enumerate(incoming) :
        if c == 'x' :
            partons[-1] = -1 * partons[-1]
            continue
        partons.append(parton_dict[c])

    return partons

def p4_to_MG_vector(p4) :
    return [p4.E(), p4.Px(), p4.Py(), p4.Pz()]


def get_incoming_partons(ZZjj_p4) :
    
    com_energy_half = ZZjj_p4.M() / 2.
    parton_1 = TLorentzVector()
    parton_1.SetPxPyPzE(0, 0, com_energy_half, com_energy_half)
    parton_2 = TLorentzVector()
    parton_2.SetPxPyPzE(0, 0, - com_energy_half, com_energy_half)

    boost = ZZjj_p4.BoostVector()

    parton_1.Boost(boost)
    parton_2.Boost(boost)

    return [p4_to_MG_vector(parton_1), p4_to_MG_vector(parton_2)]



class likelihood :
    def __init__(self, subprocess_dir, param_card = None, beam_energy = 6500, fac_scale = 2 * 91.2 + 200, PDF_name = "NNPDF30_lo_as_0130/0") : 
        self.matrices = get_matrices(subprocess_dir, param_card = None)
        self.beam_energy = beam_energy
        self.fac_scale = fac_scale
        self.pdf = lhapdf.mkPDF(PDF_name)
        self.partons = {}
        for k, v in self.matrices.iteritems() :
            self.partons[k] = get_parton_flavor(k)


    def get_likelihood(self, Z1, Z2, tagjet1, tagjet2) :

        ZZjj_p4 = (Z1[0] + Z1[1] + Z2[0] + Z2[1] + tagjet1 + tagjet2)
        incoming_partons = get_incoming_partons(ZZjj_p4) 

        p1 = [
                incoming_partons[0],
                incoming_partons[1], 
             ]

        p2 = [
                incoming_partons[1],
                incoming_partons[0], 
             ]

        Z1 = [
                p4_to_MG_vector(Z1[0]),
                p4_to_MG_vector(Z1[1]),
             ]
            
        Z2 = [
                p4_to_MG_vector(Z2[0]),
                p4_to_MG_vector(Z2[1]),
             ]

        perm_1 = [
                    p1 + Z1 + Z2 + [p4_to_MG_vector(tagjet1), p4_to_MG_vector(tagjet2)], 
                    p1 + Z1 + Z2 + [p4_to_MG_vector(tagjet2), p4_to_MG_vector(tagjet1)], 
                    p1 + Z2 + Z1 + [p4_to_MG_vector(tagjet2), p4_to_MG_vector(tagjet1)], 
                    p1 + Z2 + Z1 + [p4_to_MG_vector(tagjet1), p4_to_MG_vector(tagjet2)], 
 
                    p2 + Z1 + Z2 + [p4_to_MG_vector(tagjet1), p4_to_MG_vector(tagjet2)], 
                    p2 + Z1 + Z2 + [p4_to_MG_vector(tagjet2), p4_to_MG_vector(tagjet1)], 
                    p2 + Z2 + Z1 + [p4_to_MG_vector(tagjet2), p4_to_MG_vector(tagjet1)], 
                    p2 + Z2 + Z1 + [p4_to_MG_vector(tagjet1), p4_to_MG_vector(tagjet2)], 
                  ]
        #print 'perm1 '
        #for i, mom in enumerate(perm_1[0]) :
        #    print i, ' ', mom
        perm_2 = []
        for p in perm_1 :
            perm_2.append(invert_momenta(p))
        alpha_s = 0.13
        nhel = 0 # means sum over all helicity
        likelihood = 0

        me2 = 0.
        likelihood =0.

        squares = {}

        sums = [] 
        for i,p in enumerate(perm_2) :
            perm_sum = 0.
            #for i, mom in enumerate(p) :
            #    print i, ' ', mom
            x_1 = p[0][0] / self.beam_energy
            x_2 = p[0][1] / self.beam_energy
 
            for k, v in self.matrices.iteritems() :
                pdf_product = self.pdf.xfxQ2(self.partons[k][1], x_2, self.fac_scale) * self.pdf.xfxQ2(self.partons[k][0], x_1, self.fac_scale) / x_1 / x_2
                me2 = v.get_me(p, alpha_s, nhel)
                perm_sum += me2 * pdf_product
                likelihood += me2 * pdf_product
            sums.append(perm_sum)
#        max_me = max(squares.iteritems(), key=operator.itemgetter(1))[0]
#        print 'maximum ME2 for ', max_me, ' is ', squares[max_me] 
#            print 'me^2 sum: ', likelihood
        #print 'likelihood: ', likelihood
        #print sorted(squares.items(), key=operator.itemgetter(1)) 
        #return  squares[max_me] #likelihood
        #return max(sums)
        return  likelihood

    def test_likelihood(self, particles) :
        p4ded = [p4_to_MG_vector(part) for part in particles]
        inverted = [invert_momenta(p4ded)]
        alphas = 0.13
        nhel = 0 # means sum over all helicity
        likelihood = 0

        print 'LHE'
#        for p in p4ded :
#            print p

        me2 = 0
        sums = []
        for i,p in enumerate(inverted) :
            perm_sum = 0.
            for i, mom in enumerate(p) :
                print i, ' ', mom
 
            for k, v in self.matrices.iteritems() :

              
                #print v.__doc__
                x_1 = p[0][0] / self.beam_energy
                x_2 = p[0][1] / self.beam_energy
                #print x_1, ' ', x_2
                #print self.partons[k][1], ' ', self.partons[k][0]
                pdf_product =  self.pdf.xfxQ2(self.partons[k][1], x_2, self.fac_scale) * self.pdf.xfxQ2(self.partons[k][0], x_1, self.fac_scale) / x_1 / x_2# *
              #print 'process ', k
                me2 = v.get_me(p, alphas, nhel)
                #squares[str(i) + '_' + k] = me2
                perm_sum += me2 * pdf_product
                #print 'ME^2: ', me2
                #print 'PDF ', pdf_product
                #print 'PDGID 2', self.partons[k][1]
                likelihood += me2 * pdf_product
            sums.append(perm_sum)
        return max(sums)
 
