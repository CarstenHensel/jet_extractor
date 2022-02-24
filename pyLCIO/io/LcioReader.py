'''
Created on Dec 4, 2012

@author: <a href="mailto:christian.grefe@cern.ch">Christian Grefe</a>
'''

from __future__ import absolute_import, unicode_literals
import os

from pyLCIO import IOIMPL, IO
from pyLCIO.io.Reader import Reader
#from ROOT import vector
from ROOT import std

class LcioReader( Reader ):
    ''' Class to hold an LCReader object '''
    
    def __init__( self, fileName=None ):
        ''' Constructor allowing initialization with an LCIO file '''
        
        # Create a new LCReader
        reader = IOIMPL.LCFactory.getInstance().createLCReader( IO.LCReader.directAccess )
        Reader.__init__(self, reader, fileName)
    
    def getNumberOfRuns( self ):
        ''' Get the number of runs in the current file '''
        return self.reader.getNumberOfRuns()
    
    def __read__( self ):
        ''' Get the next event from the stream '''
        return self.reader.readNextEvent()
    
    def __open__( self, fileName ):
        if self.isOpen:
            self.__close__()
        self.reader.open( fileName )
        self.isOpen = True
            
    def setReadCollectionNames(  self, colNames ):
        #wrapper example for an autogenerated method that takes a string vector
        v = std.vector(std.string)()
        for col in colNames:
            v.push_back(col)
        self.reader.setReadCollectionNames( v )
