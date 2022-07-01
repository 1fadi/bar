# Status bar
A script that monitors live **CPU usage, network connection (also connection type), volume level, VPN connection, counts installed packages, free RAM, battery level, checks USB drives**. 

Best use of this script is on a panel of a window manager on Linux based system.

## Requirements
#### Modules:
* psutil
* netifaces
* socket
* subprocess
* pyudev

## Notes
* this script works with no problems on most linux based operating systems.
* Some of these functions require you to change certain commands based on the distro you want to execute this script on.
