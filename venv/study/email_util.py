import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# email_info = {"smtp_server": 'smtp.qq.com',
#               "port": 465,
#               "sender": '378250459@qq.com',
#               "psw": 'njcuxbqhakkzbjbb',
#               "receiver": 'mjlei007@163.com'}

email_info = {"smtp_server": 'ismtp.beyondsoft.com',
              "port": 25,
              "sender": 'majilei@beyondsof.com',
              "psw": 'Qwer!@#$5',
              "receiver": 'mjlei007@163.com'}


class EmailUtil(object):

    def __init__(self):
        self.email_info = email_info
        self.sender = self.email_info['sender']
        self.psw = self.email_info['psw']
        self.smtpserver = self.email_info['smtp_server']
        self.receiver = self.email_info['receiver']
        self.port = self.email_info['port']

    def get_mail_body(self, file_path):
        mail_body = None
        if not os.path.exists(file_path):
            print("file not exist")
            return mail_body

        with open(file_path, 'rb') as f:
            mail_body = f.read()

        return mail_body

    def send_mail(self, mail_body):
        """4发送最新的测试报告内容"""
        # with open(file_path, 'rb') as f:
        #     mail_body = f.read()

        # 定义邮件内容
        msg = MIMEMultipart()
        body = MIMEText(mail_body, _subtype='html', _charset='utf-8')
        msg['Subject'] = "自动化测试报告"
        msg['from'] = self.sender
        msg['to'] = self.receiver
        msg.attach(body)

        # 添加附件
        att = MIMEText(mail_body, "base64", "utf-8")
        att["Content-Type"] = "application/octet-stream"
        att["Content-Disposition"] = 'attachment; filename="report.html"'
        msg.attach(att)

        try:
            # smtp = smtplib.SMTP_SSL(self.smtpserver.encode(), self.port)
            smtp = smtplib.SMTP_SSL(self.smtpserver, self.port)
        except Exception as e:
            print(e)
            smtp = smtplib.SMTP()
            smtp.connect(self.smtpserver, self.port)

        smtp.login(self.sender, self.psw)
        smtp.sendmail(self.sender, self.receiver, msg.as_string())
        smtp.quit()
        print("email has been sent out!")

    def send_mail2(self):
        # SMTP服务器地址和端口号
        smtp_server = 'smtp.qq.com'
        smtp_port = 465
        # 发送方邮箱地址和密码
        sender_email = self.sender
        sender_password = self.psw

        # 收件人邮箱地址
        recipient_email = self.receiver
        # 邮件主题和正文
        mail_subject = 'Python邮件测试'
        mail_content = '这是一封Python发送的邮件。'

        # 创建SMTP对象
        smtpObj = smtplib.SMTP_SSL(smtp_server, smtp_port)
        # 登录SMTP服务器
        smtpObj.login(sender_email, sender_password)

        # 发送邮件
        message = MIMEText(mail_content, 'plain', 'utf-8')
        message['Subject'] = mail_subject
        message['From'] = sender_email
        message['To'] = recipient_email

        smtpObj.sendmail(sender_email, recipient_email, message.as_string())

        # 关闭SMTP连接
        smtpObj.quit()


if __name__ == '__main__':
    file_path = './result.html'
    email = EmailUtil()
    # mail_body = email.get_mail_body(file_path)
    # email.send_mail(mail_body)
    email.send_mail2()
