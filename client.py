from socket import *
import sys

HOST = '127.0.0.1'
PORT = 6799
BUFFER_SIZE = 4096

def create_socket():
    client_socket = socket(AF_INET, SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
    except Exception as e:
        print(f"Erro ao conectar ao servidor: {e}")
        sys.exit(1)
    return client_socket

def request_file(client_socket):
    while True:
        filename = input("Digite o nome do arquivo a ser solicitado (ou 'exit' para sair): ")
        if filename.lower() == 'exit':
            client_socket.send("CLOSE".encode())
            break
        if not filename.strip():
            print("Por favor, insira um nome de arquivo válido.")
            continue

        request = f"GET /{filename} HTTP/1.1\r\n"
        client_socket.send(request.encode())
        
        response = client_socket.recv(BUFFER_SIZE).decode()
        print(response)

def main():
    client_socket = create_socket()
    request_file(client_socket)
    client_socket.close()

if __name__ == "__main__":
    main()
