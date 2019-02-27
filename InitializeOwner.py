from cryptography.fernet import Fernet
from Contacts import Contact

class FirstMan:
    SHADOW_FILE_PATH = './Shadows/.nofile'
    SECRET_FILE_PATH = './Shadows/.secrets'

    def Init(self):
        InitializeOwner = self.TakeContactDetails()
        print(InitializeOwner)
        InitializeSecrets = self.BlackHole()
        print(InitializeSecrets)
    
    def TakeContactDetails(self):
        Contact_Object = Contact()
        Owner_details = Contact_Object.getEmailAddresses(Name="My Self")
        if Owner_details == False:
            print("You have to give your basic contact details First")
            First_Name = input("Tell me your First Name :")
            Family_Name = input("Tell me your house Name :")
            Full_Name = First_Name+" "+Family_Name
            
            My_Details = Contact_Object.ask_details(add_phone=1,add_email=1,name=Full_Name)
            my_vcard = Contact_Object.create_vcard(name=Full_Name,parameters= My_Details)
            Contact_Object.save_new_contact(First_Name="My",Family_Name="Self",data=my_vcard)
            return "Owner {} First of his name, of house {} is now known to my world".format(First_Name,Family_Name)
        
        return "Your Contact Details are :"+repr(Owner_details)
        

    def BlackHole(self):
        Contact_Object = Contact()
        Owner_details = Contact_Object.getEmailAddresses(Name="My Self")
        shadow_file = open(self.SHADOW_FILE_PATH,'a')
        shadow_file.close()
        shadow_file = open(self.SHADOW_FILE_PATH,'r')
        shadows = []
        pending_secrets = []
        for line in shadow_file.read():
            shadows.append(line)   
        shadow_file.close()
        if len(shadows) == 0:
            shadow_file = open(self.SHADOW_FILE_PATH,'a')
            key = Fernet.generate_key()
            shadow_file.write(str(key)[2:-1]+"\n")
            shadow_file.close()
        else:
            shadow_file = open(self.SHADOW_FILE_PATH,'r')
            shadow_content = shadow_file.read()
            key = shadow_content
        secret_file = open(self.SECRET_FILE_PATH,'a')
        secret_file.close()
        secret_file = open(self.SECRET_FILE_PATH,'r')
        secrets = []
        for line in secret_file:
            secrets.append(line)
        secret_file.close()
        if len(secrets) == 0:
            cipher_suite= Fernet(key)
            Contact_Object = Contact()
            secret_file = open(self.SECRET_FILE_PATH,'w')
            for email in list(Owner_details.values()):
                password = input("Enter your Password for {} :".format(email))
                password = bytes(password,encoding = 'utf-8')
                encrypted_password = cipher_suite.encrypt(password)
                secret_file.write(email+" : "+str(encrypted_password)+"\n")
            secret_file.close()
        else:
            cipher_suite= Fernet(key)
            for email in list(Owner_details.values()):
                for secret in secrets:
                    if email not in secret:
                        pending_secrets.append(email)
            secret_file = open(self.SECRET_FILE_PATH,'a')
            for email in pending_secrets:
                password = input("Enter your Password for {} :".format(email))
                password = bytes(password,encoding = 'utf-8')
                encrypted_password = cipher_suite.encrypt(password)
                secret_file.write("\n"+email+" : "+str(encrypted_password))
            secret_file.close()                
        return "Your Secrets are safe. Don't Worry !"
    
    def Hawking_Radiation(self):
        shadow_file = open(self.SHADOW_FILE_PATH,'r')
        shadow_string = shadow_file.read()
        shadow_bytes = bytes(shadow_string,encoding='utf-8')
        cipher_suite= Fernet(shadow_bytes)
        secret_file = open(self.SECRET_FILE_PATH,'r')
        secrets = []
        for line in secret_file:
            secrets.append(line)
        secret_file.close()
        HawkRadiation = dict()
        for secret in secrets:
            secret_part = secret.split(':')
            encrypted_password = bytes(secret_part[1][3:-1],encoding='utf-8')
            HawkRadiation[secret_part[0][:-1]] = str(cipher_suite.decrypt(encrypted_password))[2:-1]
        return HawkRadiation

