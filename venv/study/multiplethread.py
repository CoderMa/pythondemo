import threading
import time
import os


def singer(count):
    print(os.getpid())
    print(os.getppid())
    for i in range(count):
        print("singer %d" % i)
        time.sleep(1)


def dancer(num):
    print(os.getpid())
    print(os.getppid())
    for i in range(num):
        print("dancer %d" % i)
        time.sleep(1)


if __name__ == '__main__':
    my_singer = threading.Thread(target=singer, args=(5,))
    my_dancer = threading.Thread(target=dancer, kwargs={'num': 5})

    # 设置守护线程的两种方式
    # my_singer.setDaemon(True)
    # my_singer = threading.Thread(target=singer, daemon=True)

    my_singer.start()
    my_dancer.start()