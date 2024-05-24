import socket
import logging

# IDEA: On client, request to open up a file, which must be sent by server to client. 
#Then client reads and performs operations to another file, which could then be sent back to server
HOST = '127.0.0.1' # The server's IP address
PORT = 65432 # The port used by the server 

# Loop flags
exit = False

logging.basicConfig(filename='client-log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

while (not exit):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT)) # Connects to server
            s.settimeout(2)

            while True:
                answer = input("\nEnter command: ")
                answer = answer.strip()
                
                # Perform some type of input validation (ex. 'exit]' is no valid input)
                # BUT HOW?
                # Can have dictionary of all possible inputs (TOO LIMITING AND THERES SO MANY)
                # User can recheck input or just don't set timeout in case the command is unsuccessful so the script won't abort
                # 
                if (answer.lower() == 'exit'):
                    logging.info(f"Successfully exiting after user command '{answer}'")
                    print("\nExiting client...")
                    exit = True
                    break

                if ";" in answer:
                    commandList = answer.split(";")
                    byteCommandArray = bytearray()
                    for string in commandList:
                        byteCommandArray.extend(string.encode("utf-8"))
                        byteCommandArray.append(3)
                    s.sendall(byteCommandArray)
                    logging.info(f"Command sent to server: {byteCommandArray}")
                else:
                    s.sendall(bytes(answer, encoding="ascii")) # Sends message to server
                    logging.info(f"Command sent to server: {answer}")

                data = s.recv(1024)
                decodedData = data.decode("utf-8")
                while (len(decodedData) > 0):
                    try:
                        if (decodedData != answer):
                            print(decodedData)
                        data = s.recv(1024) 
                        decodedData = data.decode("utf-8")
                    except Exception as e:
                            logging.info(f"Exception: {e}")
                            #if ('timed out' in str(e)): # Catch if socket timed out
                            break           
    except Exception as e: 
        #if ('timed out' in str(e)): # Catch if socket timed out
        #if ('[WinError 10061]' in str(e)): # Catch if server is not running
        print("\nServer unavailable...")
        print("\nException: ", e)
        logging.info(f"Exception: {e}")

        # How to handle timeout from bad input/command?
        continue
        #exit = False



