import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import configparser

class EmailSender:
    def __init__(self,
            account = '',
            password = '',
            user = '',
            recipient = '',
            title = '',
            content = '',
            smtpSever = 'smtp.gmail.com',
            smtpPort = 587,
            file = []):

        if account == '' or password == '':
            self.read_ini()
        else:
            self.account = account
            self.password = password
            self.smtpSever = smtpSever
            self.smtpPort = smtpPort
        self.user = user
        self.recipient = recipient
        self.title = title
        self.content = content
        self.file = file
        self.smtp = None

    def read_ini(self):
        try:
            strININame = os.path.basename(__file__).split('.')[0]
            strINIPath = f'./INI/{strININame}.ini'
            config = configparser.ConfigParser()
            config.read(strINIPath)

            self.account = config.get('login', 'account')
            self.password = config.get('login', 'password')
            self.smtpSever = config.get('smtp', 'smtpSever')            
            self.smtpPortr = config.get('smtp', 'smtpPort')
        except Exception as e:
            print(e)


    def smtp_connect(self):
        try:
            smtp = smtplib.SMTP(self.smtpSever, self.smtpPort)
            smtp.ehlo()
            smtp.starttls()
            smtp.login(self.account, self.password)
            self.smtp = smtp
        except Exception as e:
            print(e)
            
    def send_email(self):
        
        self.smtp_connect()

        msg = MIMEMultipart()
        msg['From'] = self.user
        msg['To'] = self.recipient
        msg['Subject'] = self.title
        body = MIMEText(self.content, 'plain', 'utf-8') #設定文字編碼格式
        msg.attach(body)

        # attach files
        for file_path in self.file:
            with open(file_path, 'rb') as attachment:
                msg_file = MIMEBase('application', 'octet-stream')
                msg_file.set_payload(attachment.read())
                encoders.encode_base64(msg_file)
                filename = file_path.split("\\")[-1]
                msg_file.add_header(
                    'Content-Disposition',
                    f'attachment; filename="{filename}"')
                msg.attach(msg_file)

        status = self.smtp.sendmail(self.user, self.recipient, msg.as_string()) # 寄信並驗證是否傳送成功
        if status == {}:
            print("email傳送成功")
        else:
            print("email傳送失敗")
    
        self.smtp.quit()        
        
if __name__ == "__main__":
    email_sender = EmailSender()