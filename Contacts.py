import vobject

class Contact:
    CONTACT_FILE_PATH = "./Contacts/ContactList.csv"
    CONTACT_REPOSITORY_PATH = "./Contacts/"
    def __init__(self,FirstName=None,FamilyName=None):
        if FirstName == None and FamilyName == None:
            return
        First_Name = FirstName
        Family_Name = FamilyName
        what_to_add = input("Do you want to add Phone number or Email address : ")
        add_email = 0
        add_phone = 0
        what_to_add_words = what_to_add.split()
        for word in what_to_add_words:
            if word in "phone number mobile":
                add_phone =1 
            if word in "email mail address":
                add_email = 1
            if word in "both":
                add_phone = 1
                add_email = 1
        if not add_phone and not add_email:
            print("Why did you asked me to add a contact number ? ")
            print("Leave it ")
            return None
        Parameters = self.ask_details(add_phone,add_email)
        data = self.create_vcard(FirstName+" "+FamilyName, Parameters)
        print("Recieved values are :",data)
        self.save_new_contact(First_Name,Family_Name,data)
    def ask_details(self,add_phone = 0, add_email = 0):
        if add_phone:
            add_more = 1
            Phone_Numbers = dict()
            personal_count = 0
            work_count = 0
            while(add_more):
                already_exist_flag = 0
                phone_number = input("What is the phone number ? ")
                for key in Phone_Numbers.keys():
                            if phone_number == Phone_Numbers[key]:
                                already_exist_flag = 1
                if already_exist_flag:
                    print("This Phone Number already exist as Persons's ",key," Phone number")
                
                else:
                    Phone_Type = input("Is this personal phone number or work phone number ")
                    personal_flag = 0
                    work_flag = 0
                    phone_type_words = Phone_Type.split()
                    for word in phone_type_words:
                        if word in "personal self own":
                            personal_flag = 1
                    if personal_flag == 0:
                        work_flag = 1
                    if personal_flag:
                        if "Personal" not in Phone_Numbers.keys():
                            Phone_Numbers["Personal"] = phone_number
                            personal_count+=1
                        else:
                            Phone_Numbers["Personal_"+str(personal_count)] = phone_number
                
                    if work_flag:
                        if "Work" not in Phone_Numbers.keys():
                            Phone_Numbers["Work"] = phone_number
                        else:
                            Phone_Numbers["Work_"+str(work_count)] = phone_number
                add_more_number = input("Add more numbers ? ")
                if add_more_number.lower() in "no nah":
                    add_more = 0
        if add_email:
            add_more = 1
            Emails = dict()
            personal_count = 0
            work_count = 0
            while(add_more):
                personal_flag = 0
                work_flag = 0
                already_exist_flag = 0
                email = input("What is the Email address ? ")
                for key in Emails.keys():
                            if email == Emails[key]:
                                already_exist_flag = 1
                if already_exist_flag:
                    print("This Email already exist as Persons's ",key," Email")
                else:
                    Email_Type = input("Is this personal email or work email")
                    email_type_words = Email_Type.split()
                    for word in email_type_words:
                        if word in "personal self own":
                            personal_flag = 1
                    if personal_flag == 0:
                        work_flag = 1
                    if personal_flag:
                        if "Personal" not in Emails.keys():
                            Emails["Personal"] = email
                            personal_count+=1
                        else:
                            Emails["Personal_"+str(personal_count)] = email
                    
                    if work_flag:
                        if "Work" not in Emails.keys():
                            Emails["Work"] = email
                        else:
                            Emails["Work_"+str(work_count)] = email
                add_more_email = input("Add more emails ? ")
                if add_more_email.lower() in "no nah":
                    add_more = 0
        if add_phone and not add_email:
            return({"Ph No":Phone_Numbers})
        if add_email and not add_phone:
            return({"Emails":Emails})
        
        return({"tel":Phone_Numbers,"Email":Emails}) 
            
        
    def save_new_contact(self,First_Name,Family_Name,data):
        print("entring save_new_contact")
        filename = "%s-%s.vcf" % (First_Name,Family_Name)
        address = self.CONTACT_REPOSITORY_PATH+filename
        f = open(address, "w")
        f.write(data)
        f.close()
        contact_file = open(self.CONTACT_FILE_PATH,'a')
        contact_file.close()
        ContactList = self.getContactList()
        index = len(ContactList)+1
        contact_file = open(self.CONTACT_FILE_PATH,'a')
        contact_file.write(str(index)+",{} {} \n".format(First_Name,Family_Name))
        contact_file.close()

    def create_vcard(self,name,parameters):
        contact = vobject.vCard()
        obj = contact.add("FN")
        obj.value = name

        Name = name.split()
        obj = contact.add('N')
        if len(Name) == 2:
            obj.value = vobject.vcard.Name( family=Name[1], given=Name[0])
        contact_parameters = list(parameters.keys())
        for params in contact_parameters:
            different_type_values = list(parameters[params].keys())
            for value in different_type_values:
                obj = contact.add(params)
                obj.type_param = value
                obj.value = parameters[params][value]
        return contact.serialize()

    def getContactList(self):
        contact_list = []
        contact_file = open(self.CONTACT_FILE_PATH,'r')
        for line in contact_file:
            contact_list.append(line)
        contact_file.close()
        return contact_list
    
    def findContact(self,Name):
        contact_list = self.getContactList()
        name_words = Name.split()
        found_flag = 0
        recorded_name = ''
        for word in name_words:
            for item in contact_list:
                if word in item:
                    found_flag = 1
                    recorded_name = item
        if found_flag == 0:
            print("Contact is not already saved")
            return "Command Execution Failed"
        temp_string = recorded_name.split(',')
        temp_string = temp_string[1].split()
        temp_string = '-'.join(temp_string)
        contact_vcard = temp_string+".vcf"
        contact_vcard_path = self.CONTACT_REPOSITORY_PATH+contact_vcard
        return contact_vcard_path
        
    def getEmailAddresses(self,Name):
        contact_file_path = self.findContact(Name)
        contact_file = open(contact_file_path,'r')
        contact_file_content = contact_file.read()
        contact_vcard = vobject.readOne(contact_file_content)
        contact_emails = dict()
        for email in contact_vcard.contents['email']:
            contact_emails[email.type_param] = email.value
        return contact_emails

    def getPhoneNumbers(self,Name):
        contact_file_path = self.findContact(Name)
        contact_file = open(contact_file_path,'r')
        contact_file_content = contact_file.read()
        contact_vcard = vobject.readOne(contact_file_content)
        contact_phone_numbers = dict()
        for tel in contact_vcard.contents['tel']:
            contact_phone_numbers[tel.type_param] = tel.value
        return contact_phone_numbers

#fn = input("Enter the first name : ")
#ln = input("Enter the family name")

#new_contact = Contact(fn,ln)
new_contact = Contact()
contact_vcard = new_contact.findContact("Mohit Beniwal")
contact_emails = new_contact.getEmailAddresses("Mohit Beniwal")
print(contact_emails)

contact_phones = new_contact.getPhoneNumbers("Mohit Beniwal")
print(contact_phones)
#v = vobject.readOne( s )
#>>> for tel in v.contents['tel']:
#...     print tel