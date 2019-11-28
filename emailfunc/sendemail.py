import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formataddr


sender = "kellypql@126.com"
password = "Winner123"
# receivers = "312200746@qq.com"


def sendExcel(receivers, subject, filepath, filename):
    msg = MIMEMultipart('related')
    msg['From'] = formataddr(["sender", sender])  # 发件人邮箱昵称、发件人邮箱账号
    msg['To'] = formataddr(["receiver", receivers])  # 收件人邮箱昵称、收件人邮箱账号
    msg['Subject'] = subject
    text = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
    msg.attach(text)

    attachment = MIMEApplication(open(filepath, 'rb').read())
    attachment.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(attachment)

    try:
        server = smtplib.SMTP('smtp.126.com', 25)
        server.set_debuglevel(1)
        server.login(sender, password)
        server.sendmail(sender, receivers, msg.as_string())
        server.quit()
        print("邮件发送成功")

    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
