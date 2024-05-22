import socket
import subprocess

HOST = '127.0.0.1' # Standard loopback interface address (localhost)
PORT = 65432 # Port to listen on (non-privileged ports are > 1023)

# Creates socket object using context manager (helps to manage resources and deallocate after block ends)

# AF_INET --> Internet address family for IPv4 
# SOCK_STREAM --> Socket type for TCP 

def dataToCommand(data):
    command = data.decode("utf-8")
    return command

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  
    s.bind((HOST, PORT)) # Method used to link socket to network interface and port 
    s.listen() # Enables server to accept connections .. Now listening 
    conn, addr = s.accept() # Accepts a connection... 
    # Conn --> New socket object to send/receive data 
    # Addr --> Address on other side of connection 

    # S --> Listening socket //// Conn --> Communicating socket
    try:
        with conn:
            print(f"Connected to {addr}")
            while True:
                data = conn.recv(1024) # Read data from client (max of 1024 bits to be sent at a time)
                if data.find(b'exit') != -1:
                    print("\nExiting server...")
                    break
                if not data: 
                    print("Client unavailable...")
                    break
                
                command = dataToCommand(data)
                print("THE COMMAND: ", command)

                p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                for x in p.stdout.readlines():
                    print(x)
                retval = p.wait()

                conn.sendall(data) # Echo data back to client

                # Whenever an empty byte object is returned by conn.recv, 
                #the client has closed the connection and loop is terminated.
    except: 
        print("Client unavailable...")