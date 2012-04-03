"""The root network discovery class.
This module provides the "Discoverer" base class, a background task
which discovers machines and the services they're running, pushing
the output to a queue.
It also provides functions which can load and start all the available 
discoverers.
"""

import os

from glob      import glob
from time      import sleep
from threading import Thread

class Discoverer(Thread):
    """The base network discovery class.
    Instances of these run forever in the background, finding new nodes,
    networks and services, passing them to an output queue.

    Attributes:

    isIntrusive      
        True if the actions taken by this class could be described as 
        unwelcome or abusive. For example a Discoverer who uses nmap
        to scan the network and its hosts MUST have this value set to
        True, because it's potentially naughty and shouldn't be done
        without the user's permission.

    isPassive
        True if this class doesn't actually interact with the network
        or hosts on the network to discover nodes or services. For
        example, reading data from /proc/net is completely passive,
        while finding machines via broadcast ping is not.
    """

    isIntrusive = False
    isPassive   = False

    def __init__(self, output, loopTime=60):
        """Construct a new Discoverer
        output: a queue where the output will be pushed.
        loopTime: the amount of time to sleep for between loops."""
        Thread.__init__(self)
        self.output   = output
        self.loopTime = loopTime

    def run(self):
        """Runs this detector forever in a loop.
        You can override this method if your discoverer already loops
        forever.
        """
        while True:
            self.runOnce()
            sleep(self.loopTime)

    def runOnce(self):
        """Runs one loop of your discoverer.
        Override this method and do self.output.put(dict)
        """
        pass

def getAllDiscoverers():
    """Gets all available discoverer classes.
    Each Discoverer exists as a file named Dicoverer_*.py in this 
    script's directory. This function creates each one and returns
    a list of their classes, which can be used to construct objects.
    """
    ret = []
    basepath = os.path.dirname(os.path.realpath(__file__))

    for name in glob('{base}/Discoverer_*.py'.format(base=basepath)):
        modname = os.path.splitext(os.path.split(name)[1])[0]
        module  = __import__('{mod}'.format(mod=modname))
        ret.append(getattr(module, modname))

    return ret

    
