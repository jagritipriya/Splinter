import vobject

class Contact:
    def __init__(self,FirstName,FamilyName=None):
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
        filename = "%s-%s.vcf" % (First_Name,Family_Name)
        address = "./Contacts/"+filename
        f = open(address, "w")
        f.write(data)
        f.close()

    def create_vcard(self,name,parameters):
        contact = vobject.vCard()
        obj = contact.add("FN")
        obj.value = name

        Name = name.split()
        obj = contact.add('N')
        if len(Name) == 2:
            obj.value = vobject.vcard.Name( family=Name[1], given=Name[0])

        len_parameters = len(parameters.items())
        contact_parameters = list(parameters.keys())
        for params in contact_parameters:
            different_type_values = list(parameters[params].keys())
            for value in different_type_values:
                obj = contact.add(params)
                obj.type_param = value
                obj.value = parameters[params][value]
        print(contact.serialize())
        return contact.serialize()

#contact_details = {"Ph No":["Cell","9741047496"], "Email": ["Personal","mohit7me@gmail.com"]}
#contact_name = "Mohit Beniwal"

#Contact.add_new_contact(contact_name,contact_details)

First_Name = input("Enter first name :")
Family_Name = input("Enter Family name :")

new_contact = Contact(First_Name,Family_Name)




