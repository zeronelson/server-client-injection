import socket

HOST = '127.0.0.1' # The server's IP address
PORT = 65432 # The port used by the server 

exit = True

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT)) # Connects to server

        while (exit):

            s.sendall(b"We made it") # Sends message to server
            data = s.recv(1024) # Reads server reply 
            print(f"Received {data!r} ")
            answer = input("Enter command: ")
            s.sendall(bytes(answer, encoding="ascii")) # Sends message to server
            data = s.recv(1024)
            print(f"Received {data!r} ")


            if (data.find(b'exit') != -1):
                exit = False
                print("Exiting client...")
        

except Exception as e: 
    print("\nServer unavailable...")
    print("THE REASON: ", e)

#print(f"Received {data!r} ")


