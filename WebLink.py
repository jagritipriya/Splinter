import os
import smtplib
import getpass
import time
import imaplib
import email
import os.path as op
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from Contacts import Contact
from InitializeOwner import FirstMan
import re
import datetime
from QureyParser import QueryParser

class EmailObject:
    MYSELF = "My Self"
    send_from = ''
    send_to = []
    files = []
    subject = ''
    message = ''
    def __init__(self):
        contact_object = Contact()
        my_email_address = contact_object.getEmailAddresses(self.MYSELF)
        self.send_from = my_email_address['Personal']
        if len(my_email_address)>1:
            choice = input("Should I use your work email address ?")
            choice_words = choice.split()
            for word in choice_words:
                if word in "yeah yes right":
                    self.send_from = my_email_address['Work']            

        Name = input("Whom do you want to send the mail : ")
        contacts_email_address = contact_object.getEmailAddresses(Name)
        for email in list(contacts_email_address.values()):
            self.send_to.append(email)
        self.subject = input("What should be the subject of email :")
        self.message = input("What is your message ?")
"""
        self.send_to = contacts_email_address['Personal']
        if len(contacts_email_address)>1:
            print("These are the available email address : \n",contacts_email_address)
            choice = input("Which email address you want to choose ?")
            choice_words = choice.split()
            for word in choice_words:
                if word in "work professional":
                    self.send_to = contacts_email_address['Work']""" 
            
        
        
        
class DarkMail:
    MYSELF = "My Self"
    QP = QueryParser()
    def SendMail(self,emailobject, files=[],
                    server="smtp.gmail.com", port=587, username='', password='',
                    use_tls=True):
        send_from = emailobject.send_from
        send_to = emailobject.send_to
        subject = emailobject.subject
        message = emailobject.message
        username = send_from
        One = FirstMan()
        Hawk_Radiation = One.Hawking_Radiation()
        password = Hawk_Radiation[username]
        if username == '' or password == '':
            print("I don't have your Gmail Credentials !")
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
    

    def ReadEmails(self):
        From_Emails = []
        Subjects = []
        Dates = []

        contact_object = Contact()
        my_email_address = contact_object.getEmailAddresses(self.MYSELF)
        FROM_EMAIL = my_email_address['Personal']
        One = FirstMan()
        Hawk_Radiation = One.Hawking_Radiation()
        FROM_PWD = Hawk_Radiation[FROM_EMAIL]
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
                        email_from = msg['from']
                        #print("Mail from :",email_from)
                        incontact,name = self.isInContact(email_from)
                        #print("Is in contact : ",incontact)
                        if not incontact:
                            #print("Continuing")
                            continue
                        else:
                            From_Emails.append(name)
                            Subjects.append(msg['subject'])
                            Dates.append(msg['Date'])
                            
                            for part in msg.walk():
                                # each part is a either non-multipart, or another multipart message
                                # that contains further parts... Message is organized like a tree
                                if part.get_content_type() == 'text/plain':
                                    print(part.get_payload()) # prints the raw text
                            # downloading attachments
                            for part in msg.walk():
                                # this part comes from the snipped I don't understand yet... 
                                if part.get_content_maintype() == 'multipart':
                                    continue
                                if part.get('Content-Disposition') is None:
                                    continue
                                fileName = part.get_filename()

                                if bool(fileName):
                                    filePath = os.path.join('/Users/mohit7me/Desktop/Stuff', fileName)
                                    if not os.path.isfile(filePath) :
                                        fp = open(filePath, 'wb')
                                        fp.write(part.get_payload(decode=True))
                                        fp.close()

                                    subject = str(msg).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
                                    #print('Downloaded "{file}"'.format(file=fileName))
        
        except Exception as e:
            print (e)
        #print("All mails : ",From_Emails)
        return From_Emails,Subjects,Dates
    
    def doIHaveAMail(self):
        From_Emails,Subjects,Dates = self.ReadEmails()
        #print("Dates are : ",Dates)
        if len(From_Emails) > 0:
            day_from = Dates[-1]
            print("I have a few important Emails for you from last {} days".format(self.howOld(day_from)))
            choice = input("Do you want to hear what I've got from your inbox ?")
            print(self.QP.isAgreeing(choice))
            if self.QP.isAgreeing(choice):
                for i in range(len(From_Emails)):
                    print("You have a mail from {} sent {} days ago, about {}".format(From_Emails[i],self.howOld(Dates[i]),Subjects[i]))
                

    def isInContact(self,From):
        #print("Inside incontact")
        contacts = Contact()
        allmails = contacts.getAllEmails()
        #print("Got all the mails : ",allmails)
        found = re.findall(r'(.*)<(.*)>',From)
        if len(found) == 0:
            return False,None
        From_Name,From_Email = re.findall(r'(.*)<(.*)>',From)[0]
        #print("From_Email : ",type(From_Email))
        if From_Email in allmails:
            #print("Inside if ")
            return True,From_Name
        else:
            return False,None

    def howOld(self,rawdate):
        print("Date is: ",rawdate)
        import calendar
        month2number = dict((v,k) for k,v in enumerate(calendar.month_abbr))
        rawdate = rawdate.split()
        year = int(rawdate[3])
        month = int(month2number[rawdate[2]])
        day = int(rawdate[1])
        x = datetime.datetime(year,month,day)
        #print("X is: ",x)
        #print("Now is: ",)
        y = datetime.datetime.now() - x
        print("Y is : ",y)
        try:
            return int(str(y).split()[0])
        except:
            return 0
