# 函数列表
func_list = {}


# 路由装饰器
def route(path):  # path = "/index.html"
    def func_out(func):  # func = index
        func_list[path] = func   # func_list["/index.html"] = index

        def func_in():
            func()

        return func_in

    return func_out


# 一个函数控制一个页面（切面化编程）
@route("/index.html")  # 1 route() 2 @func_out ==> index = func_out(index)
def index():
    with open("./resources/index.html", encoding="utf8") as f:
        content = f.read()
    return content


@route("/index1.html")  # 1 route() 2 @func_out ==> index1 = func_out(index1)
def index1():
    with open("./resources/index1.html", encoding="utf8") as f:
        content = f.read()
    return content


@route("/index2.html")
def index2():
    with open("./resources/index2.html", encoding="utf8") as f:
        content = f.read()
    return content


# func_list["/index.html"] = index
# func_list["/index2.html"] = index2


# 接口函数（不能随便修改的）
def application(request_path):
    try:
        func = func_list[request_path]
        return func()
    except Exception as e:
        print(e)
        return "PAGE NOT FOUND..."
