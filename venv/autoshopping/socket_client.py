import socket
import time
import traceback

import select

# 设置服务端地址列表
SERVER_ADDRESSES = [("localhost", 8001), ("localhost", 8002), ("localhost", 8003)]


def set_socket(server_address):
    sockets = []
    for server_addr in server_address:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.setblocking(True)
        sockets.append(client_socket)
    return sockets


def start_client(server_address):
    sockets = set_socket(server_address)
    # 连接服务端
    for index, client_socket in enumerate(sockets):
        server_address = SERVER_ADDRESSES[index]
        try:
            client_socket.connect(server_address)
        except Exception as e:
            print(f"Connect to {server_address} failed: {e}")
    start_listen(sockets)


def start_listen(sockets):
    # 使用select监听服务端
    while True:
        try:
            # 仅监听已连接的socket，获取到了数据则接收数据
            readable, writeable, errors = select.select(sockets, [], sockets)

            for _socket in readable:
                try:
                    data = _socket.recv(1024)
                    if data:
                        print(f"Received message from {_socket.getpeername()}: {data.decode()}")
                    else:
                        # 当对端关闭连接时，对应的可读socket也会被认为是可写的
                        # 并且其recv方法将返回空字节流
                        sockets.remove(_socket)
                except Exception as e:
                    print(f"Error encountered while receiving data: {e}")
                    sockets.remove(_socket)
            for _socket in errors:
                print(f"Error encountered on {socket.getpeername()}")
                sockets.remove(_socket)
        except Exception as e:
            traceback.print_exc()
            print(e.args)
            time.sleep(1)
            start_client(SERVER_ADDRESSES)
            break


if __name__ == '__main__':
    # 创建socket连接
    start_client(SERVER_ADDRESSES)

