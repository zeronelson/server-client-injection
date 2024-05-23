import socket
import subprocess

HOST = '127.0.0.1' # Standard loopback interface address (localhost)
PORT = 65432 # Port to listen on (non-privileged ports are > 1023)
exit = False
STAY = True

# Creates socket object using context manager (helps to manage resources and deallocate after block ends)
# AF_INET --> Internet address family for IPv4 
# SOCK_STREAM --> Socket type for TCP 
# Conn --> New socket object to send/receive data 
# Addr --> Address on other side of connection 
# Conn --> New socket object to send/receive data 
# S --> Listening socket //// Conn --> Communicating socket   

while (STAY):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  
        s.bind((HOST, PORT)) # Method used to link socket to network interface and port 
        s.listen() # Enables server to accept connections... Server is listening 
        conn, addr = s.accept() # Accepts a connection...
        
        try:
            with conn:
                print(f"\nConnected to {addr}")
                #conn.settimeout(2.0) 

                while (not exit):
                    data = conn.recv(1024) # Read data from client (max of 1024 bits to be sent at a time)

                    if data.find(b'exit') != -1:
                        print("\nExiting server...")
                        exit = True
                        break
                    if not data: 
                        print("\nClient unavailable...")
                        exit = True
                        break
                    
                    command = data.decode("utf-8")

                    print("\nTHE COMMAND: ", command) # TODO -> Does not work for 'date' location

                    try:
                        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                        for x in p.stdout.readlines():
                            print(x)
                            conn.sendall(x)
                        retval = p.wait()
                    except Exception as e:
                        if ('timed out' in str(e)):
                            print("\nTimed out2")
                            pass
                        print("\nInvalid command")
                        print("\nTHE REASON: ", e)
                    
                    #conn.sendall(data) # Echo data back to client

        except Exception as e: 
            if ('timed out' in str(e)):
                print("\nTimed out1")
                
            STAY = False
            print("\nClient unavailable...")
            print("\nTHE REASON: ", e)