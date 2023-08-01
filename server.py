#!/usr/bin/python3
import socket
import time
import os
import subprocess
import signal
import asyncio

# Diccionario que contiene la información de los comandos y sus explicaciones y comandos a ejecutar
command_info = {
    "ls": {
        "explicacion": "Listar archivos y directorios en el directorio actual.",
        "comando": "ls"
    },
    "pwd": {
        "explicacion": "Mostrar el directorio de trabajo actual.",
        "comando": "pwd"
    },
    "cd": {
        "explicacion": "Cambiar el directorio de trabajo.",
        "comando": "cd"
    },
    "mkdir": {
        "explicacion": "Crear un directorio.",
        "comando": "mkdir"
    },
    "rmdir": {
        "explicacion": "Eliminar un directorio vacío.",
        "comando": "rmdir"
    },
    "rm": {
        "explicacion": "Eliminar un archivo o directorio.",
        "comando": "rm"
    },
    "touch": {
        "explicacion": "Crear un archivo vacío.",
        "comando": "touch"
    },
    "cat": {
        "explicacion": "Mostrar el contenido de un archivo.",
        "comando": "cat"
    },
    "chmod": {
        "explicacion": "Cambiar los permisos de un archivo o directorio.",
        "comando": "chmod"
    }
    # Agrega más comandos y explicaciones aquí
}

async def handle_client(client_conn, client_addr):
    loop = asyncio.get_event_loop()

    while True:
        msg = (await loop.sock_recv(client_conn, 255)).decode()  # Recibe el mensaje del cliente
        print(msg)
        
        msg_split = msg.split(" ") # Divide el mensaje en palabras separadas por espacios en blanco
        print('\nAddress: %s - Port: %d' % (client_addr[0], client_addr[1]))
        print('Recibido: %s' % msg)

        cmd = msg_split[0]  # Elimina espacios en blanco al inicio y final del comando

        if cmd in command_info: # Si el comando es conocido, ejecuta el comando y envía la respuesta al cliente
            info = command_info[cmd] # Obtiene la información del comando
            explanation = info["explicacion"] # Obtiene la explicación del comando
            if len(msg_split) > 1:
                for i in range(2, len(msg_split)):
                    msg_split[1] += " " + msg_split[i]
                command_to_execute = str(info["comando"]) + " " + str(msg_split[1])
            else:
                command_to_execute = str(info["comando"])

            try:
                process = subprocess.Popen(command_to_execute, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                output, error = process.communicate()
                if error:
                    response = f"Comando: {cmd}\nExplicación: {explanation}\nError al ejecutar el comando: {cmd}\n{error}\n"
                else:
                    response = f"Comando: {cmd}\nExplicación: {explanation}\nSalida:\n{output}\n"
            except Exception as e:
                response = f"Error al ejecutar el comando: {cmd}\n{str(e)}\n"
        else:
            response = f"Comando desconocido: {cmd}\n"
        
        await loop.sock_sendall(client_conn, response.encode())  # Envia la respuesta al cliente

        await asyncio.sleep(1)  # Espera 1 segundo antes de seguir al siguiente ciclo

    client_conn.close()
    print('client disconnect')

async def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = ""
    port = 9001
    server_socket.bind((host, port))
    server_socket.listen(5)
    server_socket.setblocking(False)

    loop = asyncio.get_event_loop()

    while True:
        conn, addr = await loop.sock_accept(server_socket)  # Espera la conexión de un cliente
        loop.create_task(handle_client(conn, addr))  # Crea un nuevo hilo para manejar el cliente

asyncio.run(run_server())