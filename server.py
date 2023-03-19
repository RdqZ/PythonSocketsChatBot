import socket
import select

HEADER_LENGTH = 10  # Define o tamanho do cabeçalho das mensagens
IP = "127.0.0.1"  # Define o endereço IP do servidor
PORT = 1337  # Define a porta do servidor

# Cria um socket de servidor e define opções de reutilização de endereço
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Vincula o socket do servidor ao endereço IP e à porta definidos
server_socket.bind((IP, PORT))
server_socket.listen()  # Coloca o servidor em modo de escuta

sockets_list = [server_socket]  # Lista de sockets conectados ao servidor
clients = {}  # Dicionário para armazenar informações sobre os clientes conectados

def receive_message(client_socket):
    """
    Função para receber mensagens de um cliente.
    """
    try:
        message_header = client_socket.recv(HEADER_LENGTH)  # Recebe o cabeçalho da mensagem
        if not len(message_header):  # Se não houver cabeçalho, retorna False
            return False
        message_length = int(message_header.decode('utf-8').strip())  # Obtém o comprimento da mensagem a partir do cabeçalho
        return {"header": message_header, "data": client_socket.recv(message_length)}  # Retorna um dicionário com informações sobre a mensagem recebida
    except:
        return False

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)  # Usa a função select para obter sockets prontos para leitura e exceções

    for notified_socket in read_sockets:  
        if notified_socket == server_socket: 
            client_socket, client_address = server_socket.accept() 
            user = receive_message(client_socket)  
            if user is False:  
                continue  
            sockets_list.append(client_socket) 
            clients[client_socket]
