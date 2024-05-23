import socket

HOST = '127.0.0.1' # The server's IP address
PORT = 65432 # The port used by the server 
EXIT = False
STAY = True

while (STAY):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT)) # Connects to server
            s.settimeout(2.0)

            while (not EXIT):

                #s.sendall(b"Connected...") # Sends message to server
                #data = s.recv(1024) # Reads server reply 
                #print(f"Received {data!r} ")
                answer = input("\nEnter command: ")
                s.sendall(bytes(answer, encoding="ascii")) # Sends message to server

                data = s.recv(1024)
                decodedData = data.decode("utf-8")
                while (len(decodedData) > 0):
                    try:
                        if (decodedData != answer):
                            print("\n", decodedData)
                        data = s.recv(1024) # Don't want this to block indefinitely
                        decodedData = data.decode("utf-8")
                    except Exception as e:
                        if ('timed out' in str(e)):
                            break
                   
                if (answer.find('exit') != -1):
                    print("\nExiting client...")
                    EXIT = True
                    STAY = False
                    break
                    
    except Exception as e: 
        if ('timed out' in str(e)):
            print("\nTimed out")
            continue

        if ('[WinError 10061]' in str(e)): # Catch if server is not running
            print("\nServer unavailable...")

        print("Exiting from line 48")
        STAY = False



