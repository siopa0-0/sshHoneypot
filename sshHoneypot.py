import socket
import threading
import select
import config
import paramiko

from commandHandler import processCommands
from logger import log_event

hostname = config.prompt()

#modify to where private key is located
key_path = config.KEY_PATH 

# === Fake SSH Server Interface ===
class sshServer(paramiko.ServerInterface):
    def check_channel_request(self, kind, chanid):
        # Only allow 'session' type channels (standard shell)
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
   
    def check_auth_password(self, username, password):
        print(f"[LOGIN] {username}:{password}")
        log_event(f"[LOGIN] {username}:{password}")
        # Accept ANY username/password
        return paramiko.AUTH_SUCCESSFUL 
    
    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        #Approves pseudo-terminal (PTY) request
        return True

    def check_channel_shell_request(self, channel):
        # Approves shell request
        return True 

# === Handle incoming client ===
def handleConnection(client_sock):
    buffer = ""  # Initialize the buffer to accumulate input
    try:
        transport = paramiko.Transport(client_sock)
        server_key = paramiko.RSAKey.from_private_key_file(key_path)
        transport.add_server_key(server_key)
        ssh = sshServer()
        transport.start_server(server=ssh)

        # Wait up to 20s for client to open a session
        channel = transport.accept(20)
        if channel is None:
            print("No channel.")
            return
        
        # Send a fake welcome message
        if config.SYSTEM == "Windows":
            channel.send(f"\033[2J\033[HMicrosoft Windows [Version 10.0.19045.3693]\n\r(c) Microsoft Corporation. All rights reserved.\n\n\r{hostname}".encode())
        else:
            channel.send(f"\033[2J\033[HWelcome to Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-84-generic x86_64)\n\n\r{hostname}".encode())
        while True:
            try:
                 # Wait for input for up to 60 seconds
                rlist, _, _ = select.select([channel], [], [], 180)
                if not rlist:
                    print("\n\r[!] Idle timeout: closing connection\n\r")
                    channel.send(b"\n\rIdle timeout. Bye!\n\r")
                    break

                # Receive command data from the client
                data = channel.recv(1024)
                if not data:
                    break

                i = 0
                while i < len(data):
                    byte = data[i]
                    
                    if byte == 127 or byte == 8:
                        if buffer:
                            buffer = buffer[:-1]
                            channel.send(b'\b \b')
                    elif byte == 9:
                        i += 1
                        continue      
                    elif byte == 27:
                        i += 2                  
                    else:
                        char = chr(byte)
                        buffer += char
                        channel.send(char.encode())
                    
                    i +=1

                buffer = buffer.replace('\r', '\n')

                if '\n' in buffer:
                    command, buffer = buffer.split('\n', 1)
                    command = command.strip()
                    print(f"[COMMAND] {command}") 
                    log_event(f"[COMMAND] {command}")
                    
                    if not command:
                        channel.send(f"\n\r{hostname}".encode())
                        continue

                    response, shouldClose = processCommands(command, hostname)
                    final_response = "\n\r" + response
                    channel.send(final_response.encode())
                    if shouldClose:
                        break

            except Exception as e:
                print(f"[!] Channel error: {e}")
                break
    except Exception as e:
        print(f"[!] Transport error: {e}")
    finally:
        # Always clean up the socket
        client_sock.close()
        print(f"[*] Connection closed.")
        log_event(f"Connection closed.\n")

# === Start the SSH Server ===
def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('', config.PORT))
    server_sock.listen(50)
    print(f"[*] SSH honeypot listening on port {config.PORT}")
    log_event(f"SSH honeypot listening on port {config.PORT}")

    while True:
        client_sock, client_addr = server_sock.accept()
        print(f"[+] Connection from {client_addr[0]}:{client_addr[1]}")
        log_event(f"Connection from {client_addr[0]}:{client_addr[1]}")
        t = threading.Thread(target=handleConnection, args=(client_sock,))
        t.start()

if __name__ ==  '__main__':
    main()


