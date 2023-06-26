
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re

from ansible.module_utils.six import string_types
from ansible.errors import AnsibleFilterError

class FilterModule(object):

    def filters(self):
        return {
            "cisco_interface_range": cisco_interface_range,
        }
    
def cisco_interface_range(iface_range):
    iface_ranges = iface_range.split(",")
    ifaces = list()
    for iface_range in iface_ranges:
        match = re.match(r"""(?P<interface>[A-Za-z]+) # Interface name
                        (?P<module>([0-9]/){1,2}) # Module
                        (?P<ports>([0-9])+(-[0-9]+)?)""",iface_range, re.X)
        if not match:
            raise AnsibleFilterError('unable to parse interface')
        #interface = match.group('interface')
        interface = _cisco_interface_name(match.group('interface'))
        module = match.group('module')
        ports = match.group('ports')
        
        tokens = ports.split('-')

        if len(tokens) == 1:
            iface = "{}{}{}".format(interface, module, ports)
            ifaces.append(iface)
        
        elif len(tokens) == 2:
            start, end = tokens
            for i in range(int(start), int(end) + 1):
                iface = "{}{}{}".format(interface, module, i)
                ifaces.append(iface)
                i += 1

    return ifaces

def _cisco_interface_name(short_name):
    full_names = [
        "TwentyFiveGigabitEthernet",
        "HundredGigabitEthernet",
        "GigabitEthernet",
    ]
    #fixme: Make some try, exception code if no match found.
    for name in full_names:
        if name.lower().startswith(short_name):
            return name