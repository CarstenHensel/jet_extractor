from __future__ import absolute_import, unicode_literals
from __future__ import print_function
import sys
import os
from pyLCIO.io.EventLoop import EventLoop
from pyLCIO.drivers.EventMarkerDriver import EventMarkerDriver
from drivers.jet_extractor_driver import JetExtractorDriver

def usage():
    print('Usage:\n  python %s <fileName>' % (os.path.split(sys.argv[0])[1]))
    

def loop( fileName ):
    '''Set up an event loop to read the input file and add a driver to
       extract jet information.'''
    
    # Create the event loop
    eventLoop = EventLoop()
    
    # Set the input file. The actual reader is determined from the file ending (stdhep or slcio)
    eventLoop.addFile( fileName )
    
    # Add a driver to print the progress
    markerDriver = EventMarkerDriver()
    markerDriver.setInterval( 1 )
    markerDriver.setShowRunNumber( False )
    eventLoop.add( markerDriver )
    
    # Add the driver that extract the jet information
    jet_extractor_driver = JetExtractorDriver()
    eventLoop.add( jet_extractor_driver )
    
    # Skip some events if desired
    eventLoop.skipEvents( 0 )
    
    # Execute the event loop
    #CH eventLoop.loop( -1 )
    eventLoop.loop( 10)


if __name__ == "__main__":
    if len( sys.argv ) < 2:
        usage()
        sys.exit( 0 )
        
    # Read the file name from the command line input
    file_name = sys.argv[1]
    loop( file_name )
