import os
import getpass
import platform
import socket

KEY_PATH = r"C:\Users\gayle\Desktop\Python\sshKey"
LOG_FILE_NAME = "secretsauce.log"
PORT = 2222
SYSTEM = platform.system()

# Dynamically build the full path to the log file
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, LOG_FILE_NAME)

def prompt(cwd=None):
    user = getpass.getuser()
    host = socket.gethostname()
    cwd1 = cwd or os.getcwd()
    if SYSTEM == "Windows":
        return f"{cwd1}> "
    else:
        return f"{user}@{host}:{cwd1}~$ "
    