import logging
import os


#LOGGER SECTION
#The directory where to save the log file
LOGGING_DIR = "DEBUG_LOG"
#The name of the log file
LOGGING_FILENAME = "DataTake_PyScript.log"
_LOGGING_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

fullLoggingDir = None


def _createLoggingDir():
    """
    Creates the logging directory if it doesn't exist.

    This function checks if the logging directory specified by `fullLoggingDir` exists. If it doesn't, the function creates the directory.

    Parameters:
        None

    Returns:
        None
    """
    if not os.path.exists(fullLoggingDir):
        os.makedirs(fullLoggingDir)

def _createLoggingFile():
    """
    Creates a logging file if it doesn't already exist.

    The function checks if the logging file exists at the specified path. If the file doesn't exist,
    it creates an empty file at that path.

    Parameters:
        None

    Returns:
        None
    """
    log_file_path = os.path.join(fullLoggingDir, LOGGING_FILENAME)
    if not os.path.exists(log_file_path):
        with open(log_file_path, "w") as file:
            file.write("")
            

def initialize_logging(FILE_FOLDER_NAME):
    """
    Initializes logging by creating the logging directory, the logging file, and configuring the logging format.

    Args:
        FILE_FOLDER_NAME (str): The name of the file folder where the logging directory will be created.

    Returns:
        logging.Logger: The logger object that can be used for logging.

    """
    global fullLoggingDir 
    fullLoggingDir = f"{FILE_FOLDER_NAME}/{LOGGING_DIR}"
    _createLoggingDir()
    _createLoggingFile()
    logging.basicConfig(filename=os.path.join(fullLoggingDir, LOGGING_FILENAME), format=_LOGGING_FORMAT)
    logger = logging.getLogger()
    return logger