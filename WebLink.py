import smtplib
import os.path as op
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

user = ''
password = ''
subject = "A Photo"
message = "I hope its working"
send_from = "mohit7me@gmail.com"
sent_to = "mohit7me@gmail.com"
class DarkMail:
    def SendMail(send_from, send_to, subject, message, files=[],
                    server="smtp.gmail.com", port=587, username='', password='',
                    use_tls=True):

        """Compose and send email with provided info and attachments.
        Args:
            send_from (str): from name
            send_to (str): to name
            subject (str): message title
            message (str): message body
            files (list[str]): list of file paths to be attached to email
            server (str): mail server host name
            port (int): port number
            username (str): server auth username
            password (str): server auth password
            use_tls (bool): use TLS mode
        """
        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = COMMASPACE.join(send_to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

        msg.attach(MIMEText(message))

        for path in files:
            part = MIMEBase('application', "octet-stream")
            with open(path, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="{}"'.format(op.basename(path)))
            msg.attach(part)

        smtp = smtplib.SMTP('smtp.gmail.com', port)
        if use_tls:
            smtp.starttls()
        try:
            smtp.login(username, password)
        except:
            return "Username or password is inccoret"
        try:
            smtp.sendmail(send_from, send_to, msg.as_string())
            smtp.quit()
            return "Email Sent Successfully"
        except:
            smtp.quit()
            return "Something went wrong"
    
    def ReceiveMail():
        import getpass
        import smtplib
        import time
        import imaplib
        import email
        def read_email_from_gmail(FROM_EMAIL,FROM_PWD):
            sender_list = []
            email_time_list = []
            emails = dict()
            try:
                mail = imaplib.IMAP4_SSL('imap.gmail.com')
                mail.login(FROM_EMAIL,FROM_PWD)
                mail.select('INBOX')
                typ, data = mail.search(None, 'ALL')         
                mail_ids = data[0].decode('utf-8')
                id_list = mail_ids.split()   
                first_email_id = int(id_list[-10])
                latest_email_id = int(id_list[-1])

                for i in range(latest_email_id,first_email_id, -1):
                    typ, data = mail.fetch(str(i), '(RFC822)' )
                    for response_part in data:
                        if isinstance(response_part, tuple):
                            msg = email.message_from_string(response_part[1].decode('utf-8'))
                            msg2 = msg
                            email_subject = msg['subject']
                            email_from = msg['from']
                            print ('From : ' + email_from + '\n')
                            print ('Subject : ' + email_subject + '\n')
                            print ('Raw Date:', msg['Date'])
                            sender_list.append(email_from)
                            email_time_list.append(msg['Date'])
                            emails[(email_from,msg['Date'])] = email_subject
                            return sender_list,email_time_list,emails
            except Exception as e:
                print ("Exeception: ")
                print(e)
