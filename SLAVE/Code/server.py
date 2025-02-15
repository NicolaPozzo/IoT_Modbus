import asyncio
import argparse
import time
from pymodbus.server import StartAsyncTcpServer, StartAsyncSerialServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext


# Configuring the slave's datastore with initial values for different types of Modbus data
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0]*100),  # Digital Inputs (DI)
    co=ModbusSequentialDataBlock(0, [0]*100),  # Coils (CO)
    hr=ModbusSequentialDataBlock(0, [0]*100),  # Holding Registers (HR)
    ir=ModbusSequentialDataBlock(0, [0]*100)   # Input Registers (IR)
)
context = ModbusServerContext(slaves={1: store}, single=False)

# Function to start the Modbus TCP server on port 5020
async def run_server_tcp():
    print("[✅] Starting the Modbus TCP server on port 5020...")
    await StartAsyncTcpServer(context, address=("0.0.0.0", 5020))  # Listen on all interfaces

# Function to start the Modbus RTU (serial) server on the specified port
async def run_server_serial(port):
    print(f"[✅] Starting the Modbus RTU server on port {port}...")
    await StartAsyncSerialServer(
        context, 
        port=port,  # Serial port (e.g., /dev/ttyUSB0 on Linux, COM3 on Windows)
        baudrate=9600,  # Baud rate for serial communication
        bytesize=8,  # Number of data bits
        parity="N",  # No parity
        stopbits=1,  # Number of stop bits
        framer="rtu"  # RTU frame format
    )

# Command-line argument parser to let the user select between TCP or Serial mode
parser = argparse.ArgumentParser(description="Start a Modbus TCP or RTU server.")
parser.add_argument("--mode", choices=["tcp", "serial"], default="tcp", required=True, help="Execution mode: tcp or serial")
parser.add_argument("--port", type=str, default="/dev/ttyUSB0", help="Serial port for Modbus RTU (e.g., COM3 on Windows)")

# Parse the arguments from the command line
args = parser.parse_args()

# Start the server based on the user's choice (TCP or Serial)
# !! The serial mode not WORKING !! 
if args.mode == "tcp":
    asyncio.run(run_server_tcp())  # Run the TCP server
elif args.mode == "serial":
    asyncio.run(run_server_serial(args.port))  # Run the Serial RTU server

