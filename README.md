# sshHoneypot
A simple Python-based SSH honeypot using Paramiko that simulates an interactive shell to deceive and monitor unauthorized SSH login attempts. Supports both Windows and Linux-like command emulation.

Features:

    Logs all credentials and commands used by attackers.
    Fake interactive shell (Windows or Linux style).
    Simulates common commands like cd, ls, echo, mkdir, cat, etc.
    Session timeout after inactivity.
    Easy to configure and extend.


Requirements:

    Python 3.8+
    paramiko library
    
    Install dependencies:
        pip install paramiko


Configuration:

    KEY_PATH = r"C:\path\to\your\private_key"
    PORT = 2222  # Port to listen on
    LOG_FILE_NAME = "secretsauce.log"


    Make sure the SSH private key exists at the path specified. You can generate one with:
      ssh-keygen -t rsa -f sshKey
    
Run the Honeypot:
  
    Start the SSH honeypot
      python main.py

      You should see output like:
        [*] SSH honeypot listening on port 2222

    Connect to It:

      From another machine or terminal:
        ssh -p 2222 anyuser@your_server_ip


Logs:

    All activity is logged in secretsauce.log, including:
      IP and port of the attacker
      Login credentials
      Commands executed

    Example log entry:
      [Sat May  1 14:22:03 2025] [LOGIN] admin:123456
      [Sat May  1 14:22:05 2025] [COMMAND] ls

    


















    
