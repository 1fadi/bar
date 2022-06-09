#!/usr/bin/env python
""" A script for live monitoring CPU usage, network conn, volume, VPN conn, installed packages, etc..
Use on a panel of a window manager on Linux based system.
**Install using pip3: psutil, netifaces, sockets, subprocess**
Some of these functions require you to change certain commands based on the distro you want to execute this script on.
"""

import socket
import netifaces
from os import popen
import subprocess
import psutil
import pyudev
from time import sleep


# Network
def ping():
    """checks if there is a connection"""
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


def interface(eth=Ethernet_device, wifi=Wifi_device):
    """returns the type of connection"""
    gateways = netifaces.gateways()
    if gateways["default"][2][1] == eth:
        return "Ethernet"
    elif gateways["default"][2][1] == wifi:
        return "Wifi"
    else:
        return None


def connection():
    """combines the previous two functions"""
    if ping() is True:
        if interface() == "Ethernet":
            return "Ethernet: CONNECTED"
        elif interface() == "Wifi":
            return "Wi-fi: CONNECTED"
    elif ping() is False or interface() is None:
        return "NO CONNECTION !"


# VPN
def vpn_connection():
    """checks the connection of VPN"""
    r = popen("ip a | grep tun0 | grep inet | wc -l").readline()
    if r == 1:
        return "on"
    else:
        return "off"


# CPU
def cpu():
    """return CPU usage in percent."""
    return psutil.cpu_percent(interval=0.5)


# RAM
def free_ram():
    """calculates the available ram"""
    total = psutil.virtual_memory().total/1024/1024
    free = psutil.virtual_memory().available/1024/1024
    return f"{int(free)}/{int(total)}"


# BATTERY
def bat():
    """return battery level in percent and check if its charging"""
    battery = psutil.sensors_battery()
    try:
        plugged = battery.power_plugged
    except AttributeError as err:
        return "No battery found!"
    percent = str(battery.percent)
    if plugged:
        return f"Bat: {percent}% Charging.."
    else:
        return f"Bat: {percent}%"

    
# VOLUME
def check_vol():
    """return volume level in percent.
    be sure to have alsamixer and pulseaudio installed on your system."""
    cmd = "amixer get Master | awk -F'[][]' 'END{ print $2}'"
    process = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
    return process.stdout.strip().decode("ascii")


# count installed packages
def count_pkg(default_cmd="pacman -Q"):
    """return number of all installed packages on the system.
    default_cmd: pacman for arch, apt for debian based system etc."""
    return str(len(popen(default_cmd).readlines()))


# Set hdd and ssd disks
disks = ["/dev/sda", "/dev/sdb"]


# USB drives.
def find_usb(exclude_system_disks=disks):
    """return how many usb drives are plugged in.
    this function looks up for available disks and excludes
    hdd and ssd drives."""
    context = pyudev.Context()
    usb_devices = []
    for device in context.list_devices(subsystem="block"):
        if device.device_type == "disk":
            if device.device_node not in exclude_system_disks:
                usb_devices.append(device.device_node)
    return "USB: "+ str(len(usb_devices))


#### main ####
def main():
    while True: 
        print(
            "\r",
            "RAM: {}".format(free_ram()),
            "|", "CPU: {}%".format(cpu()),
            "|", "Packages: {}".format(count_pkg()),
            "|", "VPN: {}".format(vpn_connection()),
            "|", "VOL: {}".format(check_vol()),
            "|", connection(), 
            "|", find_usb(),
            "|",# bat(),
            flush=True,
            end=""
        )
        sleep(0.3)
    
    
if __name__ == "__main__":
    main()

