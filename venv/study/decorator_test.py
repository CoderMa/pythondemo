import time


def func_outside(func):
    def func_inside():
        start = time.time()
        func()
        end = time.time()

        take_time = end - start
        print(take_time)

    return func_inside


# 通用版本的装饰器
def func_out(func):
    def func_in(*args, **kwargs):
        # 函数中如果没有return 证明函数是没有返回值的 默认返回None
        ret = func(*args, **kwargs)
        return ret

    return func_in


@func_outside  # 执行此行代码相当于： my_test = func_outside(my_test)
def my_test():
    for i in range(100000):
        print(i)


# 就近原则：谁距离login近谁就先执行装饰
@func_outside  # login = fun_outside(login)
@func_out      # login = fun_out(login)
def login():
    print("login...")


login()
my_test()

# 结论1: 调用被装饰的函数就相当于调用闭包中的内层函数
# 结论2: 外层函数的参数就是原始被装饰的函数
