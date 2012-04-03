"""This module defines the root discovery class, and provides a way
to load all the available discovery modules.
"""

from threading import Thread

class Discoverer(Thread):
    """The discovery class itself.

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

    def __init__(self, output):
        """Construct a new Discoverer
        output: a queue where the output will be pushed."""
        Thread.__init__(self)
        self.output = output

    def run(self):
        """The main loop of the discoverer.
        Do your thing in here, loop forever and pass things
        to the output queue.
        """
        pass

