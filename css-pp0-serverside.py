#!/usr/bin/env python3.7
# Artifact repository for PP0 - for more information see
# https://github.com/yossioren/pp0

# DNS server that replies with NXDOMAIN to all queries (but logs the time!!)
# Source: https://github.com/paulc/dnslib/blob/master/dnslib/server.py
# Source: https://gist.github.com/pklaus/b5a7876d4d2cf7271873
# https://gist.github.com/andreif/6069838
# To get this attack to work you need to point an NS record somewhere in the DNS hierarchy at a 
# computer running this script  
import argparse
import dnslib.server
import time

class NanoTimeDNSLogger(dnslib.server.DNSLogger):
    def log_prefix(self,handler):
        if self.prefix:
            return "%d %s [%s:%s] " % (time.time_ns(), time.strftime("%Y-%m-%d %X"),
                               handler.__class__.__name__,
                               handler.server.resolver.__class__.__name__)
        else:
            return ""

    def log_reply(self,handler,reply):
        # do nothing
        pass


# main app
# Find out which port to bind to
parser = argparse.ArgumentParser(description='Start a DNS implemented in Python. Usually DNSs use UDP on port 53.')
parser.add_argument('--port', default=5053, type=int, help='The port to listen on.')
args = parser.parse_args()

print("Starting nameserver...")

# bind to that port and start the server
# base resolver - responds to anything with NXDOMAIN
# todo: log
server = dnslib.server.DNSServer(dnslib.server.BaseResolver(), port = args.port, logger=NanoTimeDNSLogger())
server.start()

