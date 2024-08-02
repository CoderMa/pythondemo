import random

import select
import socket


def __startProxyServer(s, dest):
    # wait for the server to come up before sending it a packet.
    cmd = b'UP'
    inputSockets = [s]
    twait = random.random()  # will give a random number between 0 and 1.
    # if twait < 0.2: twait = 0.2

    for i in range(30):

        # keep sending this until we have a response.  We don't know how long it
        # will take for the __helloProxyServer() to come up with its network IO
        # working.  We wait here until it does.

        inputready, outputready, exceptready = select.select(inputSockets, [], [], twait)

        if (len(inputready) == 0):
            print("Sending UP to proxy server: %s" % cmd)
            s.sendto(cmd, dest)
            twait = 0.1
        else:
            b, src = s.recvfrom(20000)
            print("Recieved response from proxy server: %s: %s" % (src, b))
            return b


def createsocket():
    dest = ('127.0.0.1', 3910)
    cmdSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cmdSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    cmdSock.bind(dest)
    # start proxy server
    buf = __startProxyServer(cmdSock, dest)

    if cmdSock:
        cmdSock.close()


createsocket()

if __name__ == '__main__':
    createsocket()
