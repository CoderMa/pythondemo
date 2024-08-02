import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import unittest
import HTMLTestRunner
from common import logger

cur_path = os.path.dirname(os.path.realpath(__file__))


def add_case(caseName="case", rule="test*.py"):
    """1加载所有的测试用例"""
    case_path = os.path.join(cur_path, caseName)  # 用例文件夹
    if not os.path.exists(case_path):
        os.makedirs(case_path)
        print(case_path)

    # 定义discover方法的参数
    discover = unittest.defaultTestLoader.discover(case_path, pattern=rule, top_level_dir=None)
    print(discover)
    return discover


# def all_case2():
#     test_unit = unittest.TestSuite()
#     discover = add_case()
#
#     test_unit.addTests(discover)  # 直接加载discover
#     print(test_unit)
#     return test_unit


def run_case(all_case, reportName="report"):
    """2执行所有的用例， 并把结果写入HTML测试报告"""
    runner2 = unittest.TextTestRunner()

    now = time.strftime("%Y_%m_%d_%H_%M_%S")
    report_path = os.path.join(cur_path, reportName)  # 测试报告文件夹
    # 如果不存在这个report文件夹，就自动创建一个
    if not os.path.exists(report_path):
        os.makedirs(report_path)
    report_abspath = os.path.join(report_path, now + "result.html")
    print(report_abspath)

    with open(report_abspath, 'wb') as fp:
        runner2 = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                                title="这是我的自动化测试报告, 测试结果如下：，",
                                                description="用例执行情况")
        # run 所有用例
        runner2.run(all_case)


def get_report_file(report_path):
    """3获取最新的测试报告"""
    lists = os.listdir(report_path)
    lists.sort(key=lambda fn: os.path.getmtime(os.path.join(report_path, fn)))
    print("最新生成的测试报告：", lists[-1])
    # 找到最新生成的报告文件
    report_file = os.path.join(report_path, lists[-1])
    return report_file


def send_mail(sender, psw, receiver, smtpserver, report_file, port):
    """4发送最新的测试报告内容"""
    with open(report_file, 'rb') as f:
        mail_body = f.read()
    # 定义邮件内容
    msg = MIMEMultipart()
    body = MIMEText(mail_body, _subtype='html', _charset='utf-8')
    msg['Subject'] = "自动化测试报告"
    msg['from'] = sender
    msg['to'] = receiver
    msg.attach(body)

    # 添加附件
    att = MIMEText(mail_body, "base64", "utf-8")
    att["Content-Type"] = "application/octet-stream"
    att["Content-Disposition"] = 'attachment; filename="report.html"'
    msg.attach(att)

    try:
        smtp = smtplib.SMTP_SSL(smtpserver.encode(), port)
    except:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver, port)

    smtp.login(sender, psw)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
    print("test report email has been sent out!")


def all_case():
    # 待执行用例的目录
    case_dir = "D:\\workspace\\pythonlearning\\venv\\yoyotest\\case"
    test_unit = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(case_dir, pattern="test*.py", top_level_dir=None)

    """
    # discover方法筛选出来的用例，循环添加到测试套件中
    for test_suit in discover:
        for test_case in test_suit:
            # 添加用例到testcase
            test_unit.addTests(test_case)
    """

    test_unit.addTests(discover)  # 直接加载discover
    print(test_unit)
    return test_unit


"""
if __name__ == '__main__':
    # 返回实例
    runner = unittest.TextTestRunner()

    report_path = "D:\\workspace\\pythonlearning\\venv\\yoyotest\\report\\result.html"
    with open(report_path, 'wb') as report:
        runner = HTMLTestRunner.HTMLTestRunner(stream=report,
                                               title="这是我的自动化测试报告，",
                                               description="用例执行情况")
        # run 所有用例
        runner.run(all_case())
"""

if __name__ == '__main__':
    log = logger.Log()
    log.warning("-------加载测试用例---------")
    # 加载用例
    all_case = add_case()
    # 执行用例
    log.warning("-------执行测试用例---------")
    run_case(all_case)

    # 获取最新的测试报告文件
    report_path = os.path.join(cur_path, "report")  # 报告文件夹
    report_file = get_report_file(report_path)

    # 邮箱配置
    from config import readConfig

    sender = readConfig.sender
    psw = readConfig.psw
    smtp_server = readConfig.smtp_server
    port = readConfig.port
    receiver = readConfig.receiver
    # 发送报告
    # send_mail(sender, psw, receiver, smtp_server, report_file, port)
