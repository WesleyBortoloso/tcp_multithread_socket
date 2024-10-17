from socket import *
import threading
import os

HOST = '127.0.0.1'
PORT = 6799
ADDRESS = (HOST, PORT)

def connect_client(connectionSocket, addr):
    print(f"Nova conexão: {addr}")
    connected = True

    while connected:
        try:
            message = connectionSocket.recv(1024).decode()
            if not message:
                break
            connected = verify_connection(message)

            if connected:
                find_file(message, connectionSocket)

        except Exception as e:
            print(f"Erro: {e}")
            break

    close_connection(connectionSocket)

def verify_connection(message):
    return message != "CLOSE"

def find_file(message, connectionSocket):
    filename = message.split()[1][1:]
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                outputdata = f.read()

            connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
            connectionSocket.send("Content-Type: text/html\r\n".encode())
            connectionSocket.send("\r\n".encode())

            connectionSocket.send(outputdata.encode())
        else:
            connectionSocket.send("HTTP/1.1 404 Not Found\n".encode())

    except IOError:
        connectionSocket.send("500 Internal Server Error\n".encode())

def close_connection(connectionSocket): 
    connectionSocket.close()
    print(f"Uma conexão foi fechada {threading.active_count() - 1}")

def start_server():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(ADDRESS)
    serverSocket.listen()
    print('Pronto para servir...')
    return serverSocket

def main():
    serverSocket = start_server()

    while True:
        connectionSocket, addr = serverSocket.accept()
        thread = threading.Thread(target=connect_client, args=(connectionSocket, addr))
        thread.start()
        print(f"Conexões ativas {threading.active_count() - 1}")

if __name__ == "__main__":
    main()
