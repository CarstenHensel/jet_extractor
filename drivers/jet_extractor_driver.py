from __future__ import absolute_import, unicode_literals
from pyLCIO.drivers.Driver import Driver
from ROOT import TH1D, TCanvas
from sixlcio.moves import input
from collections import OrderedDict
import json
from dataclasses import dataclass
from math import log, sqrt

@dataclass
class ParticleContainer():
    delta_eta  : float
    delta_phi  : float
    log_pt     : float
    log_e      : float
    log_rel_pt : float 
    log_rel_e  : float 
    delta_R    : float
        
    def get_dict(self):
        d = {}
        d["delta_eta"]  = self.delta_eta  
        d["delta_phi"]  = self.delta_phi 
        d["log_pt"]     = self.log_pt
        d["log_e"]      = self.log_e
        d["log_rel_pt"] = self.log_rel_pt
        d["log_rel_e"]  = self.log_rel_e
        d["delta_R"]    = self.delta_R
        return d

@dataclass
class JetContainer():
    eta    : float
    phi    : float
    energy : float
    pt     : float



class JetExtractorDriver( Driver ):
    def __init__( self ):
        ''' Constructor '''
        Driver.__init__( self )

    
    def startOfData( self ):
        ''' Method called by the event loop at the beginning of the loop '''
        
        # Create ordered dictionary 
        self.v = OrderedDict()

        p = ParticleContainer(1, 2, 3, 4, 5, 6, 7)
       
        with open('data.json', 'w') as f:
            json.dump(p.get_dict(), f)
    
    def processEvent( self, event ):
        ''' Method called by the event loop for each event '''
        n = 0
        event_number = event.getEventNumber()

        print(event.getCollectionNames())
        #MCParticles
        mcparticles = event.getCollection("MCParticles")
        print(self.find_initial_state(mcparticles))

        self.print_mc_tree(mcparticles)

        out_put = {"jet content": {"ID":-1, "delta_eta":[], "delta_phi":[], "log pT":[], \
                                  "log E":[], "log rel pT":[], "log rel E":[], "Delta R": -1}}

        jet_collection = event.getCollection("Durham2Jets")
        print(jet_collection, jet_collection.size())
        
        n_jet = 0
        output_jets = []
        for j in jet_collection:
            n_jet += 1
            
            #print(help(j))
            #print(j.id(), j.getType())

            lorentz_vec = j.getLorentzVec()
            energy = lorentz_vec.Energy()
            eta = lorentz_vec.Eta()
            phi = lorentz_vec.Phi()
            pt = lorentz_vec.Pt()
            jet = JetContainer(eta, phi, energy, pt)

            output_jets.append(jet)

            # get particle from jet:
            particles = j.getParticles()
            n_particles = 0

            output_particles = []
            for p in particles:
                n_particles += 1
                p_lorentz_vec = p.getLorentzVec()
                particle_energy = p_lorentz_vec.Energy()
                particle_eta = p_lorentz_vec.Eta()
                particle_phi = p_lorentz_vec.Phi()
                particle_pt = p_lorentz_vec.Pt()

                delta_eta = eta - particle_eta
                delta_phi = phi - particle_phi
                log_pt = log(particle_pt)
                log_e = log(particle_energy)
                log_rel_pt = log(particle_pt / pt)
                log_rel_e = log(particle_energy / energy)
                delta_r = sqrt(delta_eta**2 + delta_phi**2)
                particle = ParticleContainer(delta_eta, delta_phi, log_pt, log_e, log_rel_pt, log_rel_e, delta_r)
                output_particles.append(particle)
        
    def endOfData( self ):
        ''' Method called by the event loop at the end of the loop '''
        
        # Create a canvas for each histogram and draw them
        
        
        userInput = input('Press any key to continue')


    def find_initial_state(self, mcparticles):
        initial_state = []
        for particle in mcparticles:
            if particle.getParents():
                continue
            else:
                initial_state.append(particle)
        return initial_state


    def find_quarks(self, mcparticles):
        quark_ids = [1, 2, 3, 4, 5, 6]
        quarks = []
        for mcp in mcparticles:
            if mcp.getPDG() in quark_ids:
                daughters = mcp.getDaughters()
                if daughters:
                    final_quark = False
                    for d in daughters:
                        if d.getPDG() not in quark_ids:
                            print(mcp.getPDG(), d.getPDG(), mcp.getEnergy())
                            self.get_parents(mcp)
                            final_quark = True
                    if final_quark:
                        quarks.append(mcp)
        return quarks

    def get_parents(self, mcp):
        parents = []
        parent_ids = []
        helper = mcp
        while helper.getParents():
            for p in helper.getParents():
                parents.append(p)
                parent_ids.append(p.getPDG())
                helper = parents[-1]
        print(parent_ids)
        

    def print_mc_tree(self, mcparticles):
        for mcp in mcparticles:
            print(mcp.id(), mcp.getPDG())
            string = ""
            daughters = mcp.getDaughters()
            for d in daughters:
                string += " " + str(d.id()) + " " + str(d.getPDG()) + "     "
            print(string)