#!/usr/bin/env python
import socket
import netifaces
from os import popen
import subprocess
import psutil
from pyudev import Context
from time import sleep
from datetime import datetime


# Network
def connection(interfaces: list):
    """
    Internet connection status
    """
    
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
    
    
    def find_interface(interfaces=interfaces):
        """returns the type of connection"""
        gateways = netifaces.gateways()
        return list(filter(lambda x: (x == gateways["default"][2][1]), interfaces))[0]
    
    if ping() is True:
        if find_interface()[:1] == "e":
            return "Ethernet"
        elif find_interface()[:1] == "w":
            return "Wi-fi"
    else:
        return "NO CONNECTION"


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
    percent = str(battery.percent).rpartition(".")[0]
    if plugged:
        return f"Bat: {percent}%"
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
    OS = [psutil.LINUX, psutil.OPENBSD, psutil.FREEBSD, psutil.NETBSD, psutil.BSD]
    if any(OS):  # checks if OS is supported, windows doesn't have a package manager by default
        return str(len(popen(default_cmd).readlines()))
    else:
        pass


'''# USB drives.
def find_usb(exclude_system_disks=disks):
    """return how many usb drives are plugged in.
    this function looks up for available disks and excludes
    hdd and ssd drives."""
    context = Context()
    usb_devices = []
    for device in context.list_devices(subsystem="block"):
        if device.device_type == "disk":
            if device.device_node not in exclude_system_disks:
                usb_devices.append(device.device_node)
    if not usb_devices:
        return ""
    else:
        return "USB: " + str(len(usb_devices))'''


# date and time
def display_datetime():
    # now = datetime.now()
    now = datetime.utcnow()
    current_time = now.strftime("%I:%M %p")  # 12 h cycle mode
    current_date = now.date()
    return f"{current_date} {current_time}"
