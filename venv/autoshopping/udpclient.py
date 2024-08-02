import socket
import binascii

# 指定服务器地址和端口号，务必根据实际情况修改
HOST = '127.0.0.1'
PORT = 50018
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 绑定本机50019端口
s.bind(('', 50019))

request = bytearray([0x31, 0x32, 0x33, 0x34])
s.sendto(request, (HOST, PORT))
response, server_address = s.recvfrom(1024)
print('received', binascii.hexlify(response), "from", server_address)
