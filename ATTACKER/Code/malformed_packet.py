from scapy.all import *
from scapy.layers.inet import TCP, IP
from scapy.layers.l2 import Ether

# Set the source and target IP addresses and port number for Modbus communication
source_ip = "192.168.36.130"
target_ip = "192.168.36.129"  # IP of the Modbus device (Master or Slave)
target_port = 5020  # Modbus TCP port

def send_malformed_modbus():
    """ Sends a malformed Modbus TCP packet containing two messages in one TCP segment """

    # Define two Modbus messages in hexadecimal format:
    modbus_msg_1 = bytes.fromhex("00 01 00 00 00 06 01 03 00 00 00 02")  # Read Holding Registers
    modbus_msg_2 = bytes.fromhex("00 02 00 00 00 06 01 06 00 01 00 05")  # Write Single Register

    # Create a single IP/TCP packet with both messages concatenated (malformed)
    packet = IP(dst=target_ip) / TCP(dport=target_port, flags="PA") / (modbus_msg_1 + modbus_msg_2)
    
    print("SEND malformed packet")
    send(packet, verbose=1)  # Send the malformed packet to the target device

def send_fragmented_modbus():
    """ Sends a fragmented Modbus TCP request, splitting it into two TCP segments """

    # Define a normal Modbus message (Read Holding Registers)
    modbus_msg = bytes.fromhex("00 01 00 00 00 06 01 03 00 00 00 02")

    # Split the message into two parts (fragments)
    fragment1 = modbus_msg[:5]  # First part of the message (first 5 bytes)
    fragment2 = modbus_msg[5:]  # Second part of the message (remaining bytes)

    # Send the first TCP packet with the first fragment
    packet1 = IP(src=source_ip, dst=target_ip) / TCP(dport=target_port, flags="PA") / fragment1
    send(packet1, verbose=1)

    # Send the second TCP packet with the remaining fragment
    packet2 = IP(src=source_ip, dst=target_ip) / TCP(dport=target_port, flags="PA") / fragment2
    send(packet2, verbose=1)
    
    print("SEND fragmented packet")

# Uncomment to send fragmented Modbus packet
# send_fragmented_modbus()

# Send malformed Modbus packet
send_malformed_modbus()

