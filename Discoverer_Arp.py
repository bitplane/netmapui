"""Discovers machines using ARP.
"""

import os

from Discoverer import Discoverer

# dependency check
if not os.path.exists('/proc/net/arp'):
    raise ImportError('Discoverer_Arp requires /proc/net/arp access')

class Discoverer_Arp(Discoverer):
    """ARP Discoverer.
    This passive discoverer queries the system's Address Resolution 
    Protocol cache for devices on the local ethernet network, and 
    passes them back to the caller's queue."""

    isIntrusive = False
    isPassive   = True

    def validate(self):
        """Raise an exception if dependencies aren't met.
        This discoverer requires /proc/net/arp.
        """

    def runOnce(self):
        """Adds machines from the ARP cache to the caller's queue.
        """
        input = open('/proc/net/arp')
        # ignore the first line (header)
        input.next()
        for line in input:
            tokens = line[:-1].split()

            # convert hex strings to numbers
            tokens[1] = int(tokens[1], 16)
            tokens[2] = int(tokens[2], 16)

            # skip non-ethernet and incomplete hosts
            if tokens[1] != 1 or not tokens[2] & 2:
                continue

            out = {'devices':
                      [{'ipv4': {'address'  : tokens[0]},
                        'eth' : {'address'  : tokens[3],
                                 'interface': tokens[5]}}],
                   'interfaces': [{'name':tokens[5]}] }

            self.output.put(out)

        input.close()

