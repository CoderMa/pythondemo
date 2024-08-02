import socket
import multiprocessing
import time


def main():
    """控制整个服务器流程的函数"""
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 端口复用
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    # 绑定地址
    tcp_server_socket.bind(("", 8080))
    tcp_server_socket.listen(128)

    while True:
        client_socket, addr = tcp_server_socket.accept()
        # 调用处理浏览器请求的函数
        # handler_client_request(client_socket)
        sub_process = multiprocessing.Process(target=handler_client_request, args=(client_socket,))
        sub_process.start()


def handler_client_request(client_socket):
    """和浏览器交互"""
    recv_data = client_socket.recv(100000)

    if len(recv_data) == 0:
        print("客户端关闭")
        return

    recv_data = recv_data.decode()
    print(recv_data)

    path_list = recv_data.split(" ")
    request_path = path_list[1]

    # 设置主页
    if request_path == "/":
        request_path = "/index.html"

    # 异常捕获（防止出现异常的时候服务器直接崩溃）
    try:
        # 打开资源文件
        # file_path = "D:\\workspace\\pythonlearning\\venv\\yoyotest\\report\\result.html"
        f = open("./resources" + request_path, 'rb')
        file_data = f.read()
        f.close()
    except Exception as e:
        # 文件不存在
        print(e)
        response_line = "HTTP/1.1 404 NOT FOUND\r\n"
        response_header = "server: py1.0\r\n"
        response_body = "404 NOT FOUND..."
        response_data = response_line + response_header + "\r\n" + response_body
        client_socket.send(response_data.encode())
        client_socket.close()
    else:

        # 响应行
        response_line = "HTTP/1.1 200 OK\r\n"
        response_header = "server: py1.0\r\n"
        # response_body = "124"
        response_body = file_data
        # response_data = response_line + response_header + "\r\n" + response_body
        response_data = (response_line + response_header + "\r\n").encode() + response_body

        # 发送数据
        client_socket.send(response_data)
        # time.sleep(1000)
        client_socket.close()


if __name__ == '__main__':
    main()
