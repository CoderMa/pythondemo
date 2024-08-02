import unittest
import HTMLTestRunner


def all_case():
    rule = "test*.py"
    case_dir = "D:\\workspace\\pythonlearning\\venv\\blogtest\\test_case"
    test_unit = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(case_dir, pattern=rule, top_level_dir=None)
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


if __name__ == '__main__':
    # 返回实例
    runner = unittest.TextTestRunner()

    report_path = "D:\\workspace\\pythonlearning\\venv\\blogtest\\test_report\\result.html"
    with open(report_path, 'wb') as report:
        runner = HTMLTestRunner.HTMLTestRunner(stream=report,
                                               title="这是我的自动化测试报告，",
                                               description="用例执行情况")
        # run 所有用例
        runner.run(all_case())
