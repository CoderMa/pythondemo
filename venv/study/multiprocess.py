import multiprocessing
import os


def singer(count):
    print(os.getpid())
    print(os.getppid())
    for i in range(count):
        print("singer %d" % i)


def dancer(num):
    print(os.getpid())
    print(os.getppid())
    for i in range(num):
        print("dancer %d" % i)


if __name__ == '__main__':
    print(os.getpid())
    my_singer = multiprocessing.Process(target=singer, name="my_process1", args=(5,))
    my_dancer = multiprocessing.Process(target=dancer, name="my_process2", kwargs={"num": 6})

    # 设置守护进程的两种方式
    # my_singer.daemon = True
    # my_singer.terminate()

    my_singer.start()
    my_dancer.start()
