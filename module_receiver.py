# -*- coding: utf-8 -*-

###########################################################
# This module receives results from the speechrecognition module and prints to console
#
# Syntax:
#    python scriptname --pip <ip> --pport <port>
#
#    --pip <ip>: specify the ip of your robot (without specification it will use the NAO_IP defined below
#
# Author: Johannes Bramauer, Vienna University of Technology
# Created: May 30, 2018
# License: MIT
###########################################################

# NAO_PORT = 65445 # Virtual Machine
NAO_PORT = 9559 # Robot


# NAO_IP = "127.0.0.1" # Virtual Machine
NAO_IP = "nao.local" # Pepper


from optparse import OptionParser
import naoqi
import time
import sys
from naoqi import ALProxy


class ReceiverTestModule(naoqi.ALModule):
    """
    Use this object to get call back from the ALMemory of the naoqi world.
    Your callback needs to be a method with two parameter (variable name, value).
    """

    def __init__( self, strModuleName, strNaoIp ):
        try:
            naoqi.ALModule.__init__(self, strModuleName )
            self.BIND_PYTHON( self.getName(),"callback" )
            self.strNaoIp = strNaoIp

        except BaseException, err:
            print( "ERR: abcdk.naoqitools.ReceiverModule: loading error: %s" % str(err) )

    # __init__ - end
    def __del__( self ):
        print( "INF: abcdk.naoqitools.ReceiverModule.__del__: cleaning everything" )
        self.stop()

    def start( self ):
        memory = naoqi.ALProxy("ALMemory", NAO_IP, NAO_PORT)
        memory.subscribeToEvent("SpeechRecognition", self.getName(), "processRemote")
        print( "INF: ReceiverModule: started!" )


    def stop( self ):
        print( "INF: ReceiverModule: stopping..." )
        memory = naoqi.ALProxy("ALMemory", NAO_IP, NAO_PORT)
        memory.unsubscribe(self.getName())

        print( "INF: ReceiverModule: stopped!" )

    def version( self ):
        return "0.1"

    def processRemote(self, signalName, message):
        # Do something with the received speech recognition result
        print(message)


def main():
    """ Main entry point

    """
    parser = OptionParser()
    parser.add_option("--pip",
        help="Parent broker port. The IP address or your robot",
        dest="pip")
    parser.add_option("--pport",
        help="Parent broker port. The port NAOqi is listening to",
        dest="pport",
        type="int")
    parser.set_defaults(
        pip=NAO_IP,
        pport=NAO_PORT)

    (opts, args_) = parser.parse_args()
    pip   = opts.pip
    pport = opts.pport

    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = naoqi.ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       pip,         # parent broker IP
       pport)       # parent broker port

    try:
        p = ALProxy("ReceiverTestModule")
        p.exit()  # kill previous instance
    except:
        pass
    # Reinstantiate module

    # Warning: ReceiverModule must be a global variable
    # The name given to the constructor must be the name of the
    # variable
    global ReceiverTestModule
    ReceiverTestModule = ReceiverTestModule("ReceiverTestModule", pip)
    ReceiverTestModule.start()

    SpeechRecognition = ALProxy("SpeechRecognition")
    SpeechRecognition.start()
    #SpeechRecognition.setLanguage("de-de")
    SpeechRecognition.calibrate()
    SpeechRecognition.enableAutoDetection()

    #SpeechRecognition.startRecording(20) # use this to start recording for 20 seconds (intended to use without auto-detection)

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        myBroker.shutdown()
        sys.exit(0)



if __name__ == "__main__":
    main()