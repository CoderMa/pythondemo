import socket
import threading

# 设置服务端地址和端口号
SERVER_ADDRESS = "localhost"
SERVER_PORT = 8001

# 监听的队列大小
LISTEN_QUEUE_SIZE = 5

# 消息欢迎消息
WELCOME_MESSAGE = "Welcome to server!"

# 为每个客户端建立相应的socket连接
def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    client_socket.send(WELCOME_MESSAGE.encode())

    while True:
        try:
            data = client_socket.recv(1024)
            if data:
                print(f"Received message from {client_address}: {data.decode()}")
                client_socket.send(data)
            else:
                # 关闭客户端连接
                client_socket.close()
                print(f"Connection closed by {client_address}")
                break
        except Exception as e:
            print(f"Error encountered while receiving data from {client_address}: {e}")
            client_socket.close()
            break

# 监听多个socket
def listen(address, connections):
    # 创建socket连接
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(address)
    server_socket.listen(LISTEN_QUEUE_SIZE)

    print(f"Listening on {address[0]}:{address[1]}")
    while True:
        # 等待客户端连接
        client_socket, client_address = server_socket.accept()
        print(f"Accepted new connection from {client_address}")

        # 为客户端启动线程
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.daemon = True
        thread.start()

        # 将客户端的socket连接保存
        connections.append(client_socket)

# 启动监听
connections = []
threads = []
for port in range(SERVER_PORT, SERVER_PORT + 3):
    address = (SERVER_ADDRESS, port)
    thread = threading.Thread(target=listen, args=(address, connections))
    threads.append(thread)
    thread.start()

# 等待所有线程结束
for thread in threads:
    thread.join()

# 关闭所有连接
for connection in connections:
    connection.close()

