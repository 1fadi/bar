#!/usr/bin/env python

import socket
import netifaces
from os import popen
import subprocess
import psutil
import time
from colorama import Fore
from colorama import Style


# Network
def ping():  # checks if there is a connection
    try:
        socket.setdefaulttimeout(1)
        socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = "1.1.1.1"
        port = 80
        server_addr = (host, port)
        socket_obj.connect(server_addr)
    except OSError as Err:
        return False
    else:
        socket_obj.close()
        return True


# Set network devices
Ethernet_device = "enp2s0"
Wifi_device = "wlp3s0"


def interface(eth=Ethernet_device, wifi=Wifi_device):  # returns the type of connection
    gateways = netifaces.gateways()
    if gateways["default"][2][1] == eth:
        return "Ethernet"
    elif gateways["default"][2][1] == wifi:
        return "Wifi"
    else:
        return None


def connection():  # combines the previous two functions
    if ping() is True:
        if interface() == "Ethernet":
            return "Ethernet: CONNECTED"
        elif interface() == "Wifi":
            return "Wi-fi: CONNECTED"
    elif ping() is False or interface() is None:
        return "NO CONNECTION !"


# VPN
def vpn_connection():
    r = popen("ip a | grep tun0 | grep inet | wc -l").readline()
    if r == 1:
        return "on"
    else:
        return "off"


def cpu():
    return psutil.cpu_percent(interval=0.5)


# VOLUME
def check_vol():
    cmd = "amixer get Master | awk -F'[][]' 'END{ print $2}'"
    process = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
    return process.stdout.strip().decode("ascii")


# count installed packages
def count_pkg(default_cmd="pacman -Q"):  # pacman for arch, apt for debian based system etc.
    return str(len(popen(default_cmd).readlines()))


if __name__ == "__main__":
    print("|", " CPU: {}%".format(cpu()), "|", "Packages: {}".format(count_pkg()), "|", "VPN: {}".format(vpn_connection()), "|", "VOL: {}".format(check_vol()), "|", connection(), "|", flush=True, end="")
    time.sleep(0.3)

