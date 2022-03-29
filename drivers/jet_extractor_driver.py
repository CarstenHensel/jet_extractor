from __future__ import absolute_import, unicode_literals
from pyLCIO.drivers.Driver import Driver
from ROOT import TLorentzVector
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
        
    def get_record(self):
        d = {}
        d["delta_eta"]  = self.delta_eta  
        d["delta_phi"]  = self.delta_phi 
        d["log_pt"]     = self.log_pt
        d["log_e"]      = self.log_e
        d["log_rel_pt"] = self.log_rel_pt
        d["log_rel_e"]  = self.log_rel_e
        d["delta_R"]    = self.delta_R
        return d


class JetContainer():
    def __init__(self, lcio_jet):
        self.jet = lcio_jet 
        self.pdgid = -1
        self.particles = None

    def get_record(self):
        d = {}
        dp = {}
        lorentz_vec = self.jet.getLorentzVec()
        d["eta"]       = lorentz_vec.Eta()
        d["phi"]       = lorentz_vec.Phi()
        d["energy"]    = lorentz_vec.Energy()
        d["pt"]        = lorentz_vec.Pt()
        d["pdgid"]     = self.pdgid
        d["npart"]     = len(self.particles)

        indices = range(len(self.particles))
        for index, p in zip(indices, self.particles):
            key = "particle " + str(index)
            dp[key] = p.get_record()
        d["particles"] = dp
        return d

    def add_particles(self, particles):
        self.particles = particles

    def add_pdgid(self, pdgid):
        self.pdgid = pdgid

class EventContainer():
    def __init__(self, event_number, jets):
        self.event_number = event_number
        self.jets = jets

    def get_record(self):
        d = {}
        dp = {}
        d["event"] = self.event_number
        d["njets"] = len(self.jets)
        
        indices = range(len(self.jets))
        for index, j in zip(indices, self.jets):
            key = "jet " + str(index)
            dp[key] = j.get_record()
        d["jets"] = dp
        return d

class JetExtractorDriver( Driver ):
    def __init__( self ):
        ''' Constructor '''
        Driver.__init__( self )

    
    def startOfData( self ):
        ''' Method called by the event loop at the beginning of the loop '''
        
        self.jet_records = []
       
    
    def processEvent( self, event ):
        ''' Method called by the event loop for each event '''
        n = 0
        

        #print(event.getCollectionNames())
        
        mcparticles = event.getCollection("MCParticles")
        quarks = self.find_quarks(mcparticles)

        


        jet_collection = event.getCollection("Durham2Jets")
        print(jet_collection, jet_collection.size())
        
        n_jet = 0
        output_jets = []
        for lcio_jet in jet_collection:
            n_jet += 1

            jet_lorentz_vec = lcio_jet.getLorentzVec()
            jet_eta = jet_lorentz_vec.Eta()
            jet_phi = jet_lorentz_vec.Phi()
            jet_pt = jet_lorentz_vec.Pt()
            jet_energy = jet_lorentz_vec.Energy()

            jet = JetContainer(lcio_jet)

            output_jets.append(jet)

            # get particle from jet:
            lcio_particles = lcio_jet.getParticles()
            n_particles = 0

            output_particles = []
            for p in lcio_particles:
                n_particles += 1
                p_lorentz_vec = p.getLorentzVec()
                particle_energy = p_lorentz_vec.Energy()
                particle_eta = p_lorentz_vec.Eta()
                particle_phi = p_lorentz_vec.Phi()
                particle_pt = p_lorentz_vec.Pt()

                delta_eta = jet_eta - particle_eta
                delta_phi = jet_phi - particle_phi
                log_pt = log(particle_pt)
                log_e = log(particle_energy)
                log_rel_pt = log(particle_pt / jet_pt)
                log_rel_e = log(particle_energy / jet_energy)
                delta_r = sqrt(delta_eta**2 + delta_phi**2)
                particle = ParticleContainer(delta_eta, delta_phi, log_pt, log_e, log_rel_pt, log_rel_e, delta_r)
                output_particles.append(particle)
            jet.add_particles(output_particles)
            output_jets.append(jet)
            
        event_container = EventContainer(event.getEventNumber(), output_jets)
        self.jet_records.append(event_container.get_record()) 
        
        
    def endOfData( self ):
        ''' Method called by the event loop at the end of the loop '''
        with open('data.json', 'w') as f:
              json.dump(self.jet_records, f, indent=4)
        userInput = input('Press any key to continue')



    def find_quarks(self, mcparticles):
        quark_ids = [1, 2, 3, 4, 5, 6]
        string_id = 92
        quarks = []
        for mcp in mcparticles:
            if mcp.getPDG() == string_id:
                for parent in mcp.getParents():
                    quarks.append(parent)
        return quarks

        
    def jet_matching(self, jets, quarks):
        for j in jets:
            jet_vec = TLorentzVector()


    def print_mc_tree(self, mcparticles):
        for mcp in mcparticles:
            print(mcp.id(), mcp.getPDG())
            string = ""
            daughters = mcp.getDaughters()
            for d in daughters:
                string += " " + str(d.id()) + " " + str(d.getPDG()) + "     "
            print(string)
            print(" ")