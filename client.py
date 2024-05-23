import socket
import logging

HOST = '127.0.0.1' # The server's IP address
PORT = 65432 # The port used by the server 
EXIT = False
STAY = True

logging.basicConfig(filename='client-log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

while (STAY):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT)) # Connects to server
            s.settimeout(2)

            while (not EXIT):
                answer = input("\nEnter command: ")

                if (answer.lower() == 'exit'):
                    logging.info(f"Received command to exit")
                    print("\nExiting client...")
                    EXIT = True
                    STAY = False
                    break

                if ";" in answer:
                    commandList = answer.split(";")
                    byteCommandList = bytearray()
                    for string in commandList:
                        byteCommandList.extend(string.encode("utf-8"))
                        byteCommandList.append(3)
                    s.sendall(byteCommandList)
                    logging.info(f"Command sent: {byteCommandList}")
                else:
                    s.sendall(bytes(answer, encoding="ascii")) # Sends message to server
                    logging.info(f"Command sent: {answer}")

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
        STAY = False



