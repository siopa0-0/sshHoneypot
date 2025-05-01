import os
import platform
import config

system = platform.system()

def handle_cd(command, hostname):
    arguments = command[3:]

    if not arguments:
        if system == "Windows":
            return f"{os.getcwd()}\n\n\r{config.prompt(os.getcwd())}", False
        else:
            os.chdir("/")
            return f"\n\r{config.prompt(os.getcwd())}", False
    else:    
        try:
            os.chdir(arguments)
            return f"\n\r{config.prompt(os.getcwd())}", False
        except FileNotFoundError:
            if system == "Windows":
                return f"The system cannot find the path specified.\n\n\r{config.prompt(os.getcwd())}", False
            else:
                return f"cd: no such file or directory: {arguments}.\n\n\r{config.prompt(os.getcwd())}", False
        
def handle_close(command, hostname):
    return "", True

def handle_echo(command, hostname):
    arguments = command[5:]
    return arguments + f"\n\n\r{config.prompt(os.getcwd())}", False

def handle_mkdir(command, hostname):
    arguments = command[6:]
    dir_names = arguments.split()
    if not arguments:
        if system == "Windows":
            return f"The syntax of the command is incorrect.\n\n\r{config.prompt(os.getcwd())}", False
        else:
            return f"mkdir: missing operand\n\n\r{config.prompt(os.getcwd())}", False
            
    for dir_name in dir_names:
        try:
            os.makedirs(dir_name, exist_ok=True)
        except Exception as e:
            return f"Error: {e}\n\n\r{config.prompt(os.getcwd())}", False
    return f"\n\r{config.prompt(os.getcwd())}", False

def handle_pwd(command, hostname):
    return f"{os.getcwd()}\n\n\r{config.prompt(os.getcwd())}", False

def handle_ls(command, hostname):
    if system == "Windows":
        arguments = command[4:]
    else:
        arguments = command[3:]

    path = arguments if arguments else os.getcwd()
    try:
        files = os.listdir(path)
        return "\n\r".join(files) + f"\n\n\r{config.prompt(os.getcwd())}", False
    except FileNotFoundError:
        if system == "Windows":
            return f"Cannot access '{path}': Directory or File Not Found\n\n\r{config.prompt(os.getcwd())}", False
        else:
            return f"ls: cannot access '{path}': No such file or directory\n\n\r{config.prompt(os.getcwd())}", False

def handle_rmdir(command, hostname):
    arguments = command[6:]
    dir_names = arguments.split()
    if system == "Windows":
        if not arguments:
            return f"The syntax of the command is incorrect.\n\n\r{config.prompt(os.getcwd())}", False
        if not os.path.isdir(arguments):
            return f"The system cannot find the file specified.\n\n\r{config.prompt(os.getcwd())}", False
            
    else:
        if not arguments:
            return f"rmdir: missing operand\n\n\r{config.prompt(os.getcwd())}", False
        if not os.path.isdir(arguments):
            return f"rmdir: {arguments}: No such file or directory\n\n\r{config.prompt(os.getcwd())}", False
    
    for dir_name in dir_names:
        try:
            os.rmdir(dir_name)
        except Exception as e:
            return f"Error: {e}\n\n\r{config.prompt(os.getcwd())}", False
    return f"\n\r{config.prompt(os.getcwd())}", False
    
def handle_open(command, hostname):
    if system == "Windows":
        arguments = command[5:]
        if not arguments:
            return f"The syntax of the command is incorrect.\n\n\r{config.prompt(os.getcwd())}", False
        if not os.path.isfile(arguments):
            return f"The system cannot find the file specified.\n\n\r{config.prompt(os.getcwd())}", False
    else:
        arguments = command[4:]
        if not arguments:
            return f"cat: missing operand\n\n\r{config.prompt(os.getcwd())}", False
        if not os.path.isfile(arguments):
            return f"cat: {arguments}: No such file or directory\n\n\r{config.prompt(os.getcwd())}", False

    try:
        with open(arguments, 'r') as f:
            content = f.read()
            content = content.replace("\n", "\n\r")
        return f"{content}\n\n\r{config.prompt(os.getcwd())}", False
    except Exception as e:
        return f"error reading file: {e}\n\n\r", False
        


windowsCommands = {
    "cd": handle_cd,
    "dir": handle_ls,
    "echo": handle_echo,
    "exit": handle_close,
    "mkdir": handle_mkdir,
    "rmdir": handle_rmdir,
    "type": handle_open,
    }

linuxCommands = {
    "cat": handle_open,
    "cd": handle_cd,
    "echo": handle_echo,
    "exit": handle_close,
    "logout": handle_close,
    "ls": handle_ls,
    "mkdir": handle_mkdir,
    "pwd": handle_pwd,
    "rmdir": handle_rmdir,
}

commands = windowsCommands if system == "Windows" else linuxCommands

# === Process the Commands ===
def processCommands(command, hostname):
    split_command = command.lower().split()
    base_command = split_command[0]
    if base_command in commands:
        return commands[base_command](command, hostname)

    # Handle unknown commands
    else:
        if system == "Windows":
            return f"'{base_command}' is not recognized as an internal or external command, operable program or batch file.\n\n\r{hostname}", False
        else:
            return f"bash: {base_command}: command not found\n\n\r{hostname}", False
