from pymodbus.client import ModbusTcpClient

# Connessione al server Modbus
client = ModbusTcpClient('192.168.36.129', port=5020)  # Sostituisci 'IP_DEL_SERVER' con l'IP del server

# Connessione al server Modbus
client.connect()

# Funzione di reconnaissance: invia una richiesta con function code 17 (Read Device Identification)
result = client.read_device_information()

# Stampa il risultato per vedere le informazioni del dispositivo
print(result)

# Chiude la connessione
client.close()
