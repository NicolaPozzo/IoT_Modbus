from pymodbus.client import ModbusTcpClient

# Configure the Modbus TCP client (change IP and port if necessary)
IP_SLAVE = "192.168.36.129"  # Target device address (Slave)
PORT = 5020  # Default Modbus TCP port

# Connect to the device
client = ModbusTcpClient(IP_SLAVE, port=PORT)
client.connect()

# Send a broadcast command (Write Single Register at address 40001 with value 1234)
UNIT_ID_BROADCAST = 0  # Broadcast address in Modbus
REGISTER_ADDRESS = 0  # Register address to modify
VALUE_TO_WRITE = 1234  # Value to write

print(f"[⚡] Sending Modbus TCP broadcast message to {IP_SLAVE} (port {PORT})...")
response = client.write_register(REGISTER_ADDRESS, VALUE_TO_WRITE, slave=UNIT_ID_BROADCAST)

# Broadcast messages do not generate a response, so response will be None
if response is None:
    print("[✅] Broadcast message successfully sent! No response from slaves.")
else:
    print("[❌] Something went wrong!")

# Close the connection
client.close()

