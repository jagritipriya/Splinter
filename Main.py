from WebLink import EmailObject
from WebLink import DarkMail
from InitializeOwner import FirstMan
from Contacts import Contact

My_Contacts = Contact()
My_Contacts.showContactList()

exit()


First_Man = FirstMan()
InitializeOwner = First_Man.TakeContactDetails()
print(InitializeOwner)
InitializeSecrets = First_Man.BlackHole()
print(InitializeSecrets)

New_Email = EmailObject()

EmailHandle = DarkMail()

EmailHandle.SendMail(New_Email.send_from,New_Email.send_to,New_Email.subject,New_Email.message)

