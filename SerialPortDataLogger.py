
import os
import sys
import glob
import serial
from serial.tools import list_ports
from datetime import datetime
import LoggingSuite


#FILE MAIN FOLDER
FILE_FOLDER_NAME = "GeneratedFiles"

#Constants
#The config file name where to save the com port selected
CONFIGSERIAL_FILE_NAME = f"{FILE_FOLDER_NAME}/ConfigDataTake_PyScript.conf"


#The folder where to save the data collected from serial port
FOLDERDATA_NAME = f"{FILE_FOLDER_NAME}/DataCollected"
#The name of the file to be generated in wich put data
DATA_FILE_NAME =  f"DataCollected_{datetime.now().strftime('%M%S')}.csv"
_COMPLETEFOLDERDATA_NAME = f"{FOLDERDATA_NAME}/{DATA_FILE_NAME}"


#If True, the script wait to read from the com port until is writed the string RESET_READ_LINE.
#This is done to avoid to read data from the com port before the device is ready or 
#read data from the com port before the device is reset or 
#becuase there are other data before the data to be readed
WAIT_FOR_RESET_STRING = True
#The string received from the com port to start reading the data
RESET_READ_LINE = "PyScript_StartReading"


#If True, the data readed from the com port are printed in the console
SHOW_READ_DATA_FROM_COM = False


def portSelection():
    """
    Selects a COM port from the available ports.

    Returns:
        str: The selected COM port.

    Raises:
        ValueError: If the selected port is out of range.
    """
    logger.info("Port selection.") 
    #Get all ports available
    all_ports = _getAllSerialPorts()
    
    logger.debug(f"PORTS AVAILABLE: {all_ports}") 
    
    #Check if there is any port available. If no exit
    if all_ports == []:
        print("No port available. Connect a device and try again.")
        exit()
    
    print("Choose the number of com port you want to use:")
    for i,port in enumerate(all_ports):
        print(f"{i}: {port}\n")

    port = int(input("Insert the number of the port you want to use: "))

    if port < 0 or port >= len(all_ports):
        print("Error in selecting the port. Please try again.")
        logger.error(f"Selected port: {port}. Port cannot be less than zero or grater than {len(all_ports)-1}")
        exit()
    
    logger.debug(f"PORT SELECTED: {all_ports[port]}")
    return all_ports[port]

def _getAllSerialPorts():
    """
    Returns a list of available serial ports on the system.

    Returns:
        list: A list of available serial ports.

    Raises:
        EnvironmentError: If the platform is not supported.
    """
    
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def createSerialConnection(comPort, baudrate, timeout=1):
    """
    Creates a serial connection with the specified COM port and baudrate.

    Args:
        comPort (str): The COM port to connect to.
        baudrate (int): The baudrate for the serial connection.
        timeout (float, optional): The timeout value for read operations (default is 1 second).

    Returns:
        serial.Serial: The created serial connection object.

    Raises:
        serial.SerialException: If there is an error in creating the serial connection.
    """
    logger.info("Creating the serial connection.") 
    ser = None
    try:
        ser = serial.Serial(
            port=comPort,
            baudrate=baudrate,
            timeout=timeout)
    except serial.SerialException as e:
        logger.error(f"Error in creating the serial connection: {e}")
        print(f"\n\nError in creating the serial connection.\nCHECK THE PORT IS NOT IN USED FROM OTHER PROGRAMS OR TERMINALS.\n\n")
        exit()
    return ser

def createConfigFile():
    """
    Creates a config file with the selected COM port.

    This function prompts the user to select a COM port and creates a config file
    with the selected port information. This avoid the user to select the port 
    each time the script is executed.

    Args:
        None

    Returns:
        None
    """
    logger.info("Creating the config file.") 

    portSelected = portSelection()
    with open(CONFIGSERIAL_FILE_NAME, "w") as file:
        file.write("COM_PORT: "+portSelected)
    
    logger.info("Config file created.")

def isPortConnected(actualUsingPort):
    """
    Checks if a given port is connected.

    Parameters:
    actualUsingPort (str): The port to check.

    Returns:
    bool: True if the port is connected, False otherwise.
    """
    myports = [p.device for p in list(list_ports.comports())]
    if actualUsingPort in myports:
        return True
    return False



#Initialize the logger
logger = LoggingSuite.initialize_logging(FILE_FOLDER_NAME)

if __name__ =="__main__":
    
    portSelected = -1

    #Check if the config file exists. If not create it.
    if not os.path.isfile(CONFIGSERIAL_FILE_NAME):
        createConfigFile()
        print("Created config file")

    #Read the port need to be used
    with open(CONFIGSERIAL_FILE_NAME, "r") as file:
        portSelected = file.read().split(":")[1].strip()
        print("Ready to read from port: "+portSelected)

    #Check if the port selected is correct. Else exit
    if portSelected == None or portSelected == "":
        print("Error in reading the port selected")
        exit()

    ser = createSerialConnection(portSelected, 115200)

    #Wait for the command to start reading the data. See the constants WAIT_FOR_RESET_STRING
    if WAIT_FOR_RESET_STRING:
        logger.info("Waiting for the reset command to start reading the data.") 
        print("\n\nWaiting for the reset command to start reading the data. \nIf necessary turn on device or reset it.\n")
        while(ser.readline().decode('utf-8').strip() != RESET_READ_LINE):
            pass
        logger.info("Received the command to start reading the data. Creating data file.") 
        print(f"Received the command to start reading the data.")

    print(f"Data are collected in: {_COMPLETEFOLDERDATA_NAME}\n")

    #Prepare the file to save the data

    #Create folder to save data if not exists
    if not os.path.exists(FOLDERDATA_NAME):
        os.makedirs(FOLDERDATA_NAME)
    
    
    print("Start reading data. The serial get stuck until you press CTRL+C or close the terminal or disconnect the port.\n")
    #Create file to save the data
    with open(_COMPLETEFOLDERDATA_NAME, "w") as file:    
        readedData = ""
        while isPortConnected(portSelected):
            #Read the data and save it in the file
            readedLine = ser.readline().decode('utf-8').strip()

            #If readed line is empty, the timeout is over
            if readedLine == "":
                #If there is data to save, save it
                if readedData != "":
                    file.write(readedData)
                    print("Updated Data file.\n")
                    readedData = ""
            
            #Else there are new data, append it to the readedData
            else:
                #If there is no readed data, say that is reading new data
                if readedData=="":
                    print("\nReading new data.")
                if SHOW_READ_DATA_FROM_COM:
                    print(f"SerialCom: {readedLine}")
                readedData += readedLine+"\n"
            
    print("Data reading stopped.")