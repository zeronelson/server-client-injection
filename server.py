import socket
import subprocess
import os 
import logging

HOST = '127.0.0.1' # Standard loopback interface address (localhost)
PORT = 65432 # Port to listen on (non-privileged ports are > 1023)
EXIT = False
STAY = True
multiCommand = False

# Creates socket object using context manager (helps to manage resources and deallocate after block ends)
# AF_INET --> Internet address family for IPv4 
# SOCK_STREAM --> Socket type for TCP 
# Conn --> New socket object to send/receive data 
# Addr --> Address on other side of connection 
# Conn --> New socket object to send/receive data 
# S --> Listening socket //// Conn --> Communicating socket   

# Set up logging
logging.basicConfig(filename='server-log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
while (STAY):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  
        s.bind((HOST, PORT)) # Method used to link socket to network interface and port 
        s.listen() # Enables server to accept connections... Server is listening 
        conn, addr = s.accept() # Accepts a connection...
        logging.info(f"Connected by {addr}")
        
        try:
            with conn:
                print(f"\nConnected to {addr}")

                while (not EXIT):
                    data = conn.recv(1024) # Read data from client (max of 1024 bits)
                    command = data.decode("utf-8")
                    
                    

                    if (command.lower() == 'exit'):
                        logging.info(f"Received command from {addr}: {command}")
                        print("\nExiting server...")
                        EXIT = True
                        STAY = False
                        break
                    
                    if ('\x03' in command):
                        command = command.split('\x03')
                        command.remove('')
                        multiCommand = True

                    if not data: 
                        print("\nClient unavailable...")
                        EXIT = True
                        STAY = False
                        break

                    logging.info(f"Received command from {addr}: {command}")

                    if (multiCommand):
                        for string in command:
                            try:
                                p = subprocess.Popen(string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                                stdout, stderr = p.communicate(timeout=2)
                                conn.sendall(bytes(stdout, encoding="ascii"))
                                os.kill(p.pid,1)
                            except Exception as e:
                                logging.info("Exception: ", e)
                                print("Exception: ", e)
                                pass
                        multiCommand = False
                    else:
                        try:
                            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                            stdout, stderr = p.communicate(timeout=2)
                            logging.info(f"Output from {command}: {stdout}")
                            conn.sendall(bytes(stdout, encoding="ascii"))
                            os.kill(p.pid,1)
                        except Exception as e:
                            logging.info("Exception: ", e)
                            print("Exception: ", e)
                            pass

        except Exception as e:
            logging.info("Exception: ", e)
            print("\nException: ", e)
            STAY = False
            