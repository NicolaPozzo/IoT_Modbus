from pymodbus.client import ModbusTcpClient

def main():
    ip = "192.168.36.129"  # Modbus server IP address (target device)
    port = 5020  # Modbus server port (default TCP port for Modbus)
    
    # Create a Modbus TCP client instance
    client = ModbusTcpClient(ip, port=port)
    
    # Attempt to connect to the Modbus server
    if not client.connect():
        print("Connection Failed")  # If the connection fails, print an error message
        return
    
    # Start a loop to interact with the user for Modbus operations
    while True:
        print("\nSelect an operation:")
        print("1 - Write a coil")
        print("2 - Read coils")
        print("3 - Write a register")
        print("4 - Read a register")
        print("5 - Exit")
        
        # Get user input for selecting the operation
        choice = input("Enter the operation number: ")
        
        if choice == "1":
            # Write a coil value
            address = int(input("Coil address: "))  # Ask for the coil address
            value = input("Value (True/False): ").lower() == "true"  # Ask for the coil value (True or False)
            client.write_coil(address, value)  # Write the value to the specified coil address
            print(f"Coil {address} written with value {value}")
        
        elif choice == "2":
            # Read multiple coils
            address = int(input("Starting address: "))  # Starting address of coils
            count = int(input("Number of coils to read: "))  # Number of coils to read
            result = client.read_coils(address, count=count)  # Read the coils from the server
            if result.isError():
                print("Error reading coils")  # If there's an error, print a message
            else:
                print(f"Coil values: {result.bits}")  # Display the values of the coils
        
        elif choice == "3":
            # Write a register value
            address = int(input("Register address: "))  # Ask for the register address
            value = int(input("Value to write: "))  # Ask for the value to write to the register
            client.write_register(address, value)  # Write the value to the specified register address
            print(f"Register {address} written with value {value}")
        
        elif choice == "4":
            # Read a holding register value
            address = int(input("Register address: "))  # Ask for the register address
            result = client.read_holding_registers(address, count=1)  # Read the holding register
            if result.isError():
                print("Error reading register")  # If there's an error, print a message
            else:
                print(f"Value of register {address}: {result.registers[0]}")  # Display the value of the register
        
        elif choice == "5":
            # Exit the loop and close the connection
            print("Closing connection...")
            break  # Break out of the loop to close the connection
        
        else:
            # If an invalid choice is entered, prompt the user to try again
            print("Invalid choice. Please try again.")
    
    client.close()  # Close the connection to the Modbus server

if __name__ == "__main__":
    main()  # Call the main function when the script is run

