import socket
import netifaces


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


def interface():  # returns the type of connection
    gateways = netifaces.gateways()
    if gateways["default"][2][1] == Ethernet_device:
        return "Ethernet"
    elif gateways["default"][2][1] == Wifi_device:
        return "Wifi"
    else:
        return None


def connection():  # combines the previous two functions
    if ping() is True:
        if interface() is "Ethernet":
            return "Ethernet: CONNECTED"
        elif interface() is "Wifi":
            return "Wi-fi: CONNECTED"
    elif ping() is False or interface() is None:
        return "NO CONNECTION !"


if __name__ == "__main__":
    print(connection(), flush=True, end="")