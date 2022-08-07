#!/usr/bin/env python
from barscript import *

# Set network devices
Interfaces = ["wlp4s0", "enp0s31f6"]

def main():
    
    sep = "|"  # set separator
    
    while 1: 
        print(
            "\r",
            display_datetime(),
            sep, "RAM: {}".format(free_ram()),
            sep, "CPU: {}%".format(cpu()),
            #sep, "Packages: {}".format(count_pkg()),
            sep, "VPN: {}".format(vpn_connection()),
            sep, "VOL: {}".format(check_vol()),
            sep, connection(Interfaces), 
            sep, bat(),
            flush=True,
            end="  "
        )
        sleep(0.3)
    
    
if __name__ == "__main__":
    main()