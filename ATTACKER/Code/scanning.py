from scapy.all import *
from pymodbus.client import ModbusTcpClient

network_prefix = "192.168.36."

# Loop through all possible IP addresses in the subnet (1-254)
for i in range(1, 255):
    ip = f"{network_prefix}{i}"
    client = ModbusTcpClient(ip, port=5020)

    try:
        if client.connect():
            print(f"[+] Modbus device found at address {ip}")
            result = client.read_coils(address=0, count=10)
            if result.isError():
                print(f"[-] {ip} : Registers not readable")
            else:
                print(f"[+] {ip} : Registers read successfully")
                print(result.bits)
            client.close()
    except:
        pass  # Ignore exceptions and continue scanning

