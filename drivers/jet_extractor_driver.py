from __future__ import absolute_import, unicode_literals
from pyLCIO.drivers.Driver import Driver
from ROOT import TH1D, TCanvas
from sixlcio.moves import input
from collections import OrderedDict


class JetExtractorDriver( Driver ):
    def __init__( self ):
        ''' Constructor '''
        Driver.__init__( self )
        
    
    def startOfData( self ):
        ''' Method called by the event loop at the beginning of the loop '''
        
        # Create ordered dictionary 
        self.v = OrderedDict()
    
    def processEvent( self, event ):
        ''' Method called by the event loop for each event '''


        jet_collection = event.getCollection("Durham6Jets")
        print(jet_collection)

        for jet in jet_collection:
            jet_lorentz_vec = jet.getLorentzVec()
            jet_energy = jet_lorentz_vec.Energy()
            jet_eta = jet_lorentz_vec.Eta()
            jet_phi = jet_lorentz_vec.Phi()

            # get particle from jet:
            particles = jet.getParticles()
            for particle in particles:
                particle_lorentz_vec = particle.getLorentzVec()
                particle_energy = particle_lorentz_vec.Energy()
                particle_eta = particle_lorentz_vec.Eta()
                particle_phi = particle_lorentz_vec.Phi()

        
        
    def endOfData( self ):
        ''' Method called by the event loop at the end of the loop '''
        
        # Create a canvas for each histogram and draw them
        
        
        userInput = input('Press any key to continue')