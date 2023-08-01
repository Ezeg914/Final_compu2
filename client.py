#!/usr/bin/python3
import socket

def main():
    host = '127.0.0.1'  # IP del servidor (localhost)
    port = 9001 # Puerto del servidor

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# Crea un socket de tipo TCP/IP (IPv4)
    client_socket.connect((host, port))  # Conexión al servidor

    try:
        while True:
            command = input("\nIngrese un comando de Linux ('exit' para salir): ")
            
            
            if len(command) == 0:
                print("No se ingresó ningún comando.")
                continue
            # Envía el comando al servidor
            client_socket.send(command.encode())
            
            # Recibe la respuesta del servidor
            response = client_socket.recv(4096).decode()
    

            print("\nRespuesta del servidor:")
            print(response)

            if command.lower() == 'exit':
                break

    finally:
        client_socket.close()  # Cierra la conexión al servidor

if __name__ == '__main__':
    main()