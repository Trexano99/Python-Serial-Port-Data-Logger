# Python Serial Port Data Logger

This project contains a Python script for logging data from a serial port and writes them to a local file. It can be used to log data directly on csv files or similar to be used for other purpose .<br>
It also includes a logging system that records debug information to a separate log file. <br>
The script is designed to work with devices like the ESP32, but can be adapted to work with any device that communicates over a serial port.

The project has been developed for a Windows environment, but can be easily adapted to work on other operating systems.

It is also include the file `ExecProgram_Windows.bat` that will check if Python and pip are installed and install the necessary Python packages (like pySerial) if they are not already installed.

For any help or questions, feel free to contact me without any hesitation.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8 or higher
- pip
- pySerial

pySerial is automatically installed by the `ExecProgram_Windows.bat` script if it is not already installed on your machine.

### Installing

1. Clone the repository to your local machine.
2. Run the `ExecProgram_Windows.bat`.

## Usage

1. Run the `ExecProgram_Windows.bat` file to start the script.
2. The script will prompt you to select a COM port. The selected port will be saved in a config file, so you won't have to select it again the next time you run the script.
3. The script will start reading data from the selected COM port and writing it to a file in the `GeneratedFiles/DataCollected` directory. The file will be named `DataCollected_MMSS.csv`, where `MM` is the current minute and `SS` is the current second.
4. The script will also record debug information to a log file in the `GeneratedFiles/DEBUG_LOG` directory.

Every parameter can be customized directly inside the SerialPortDataLogger.py or inside the LoggingSuite.py in the first section of the code.


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details