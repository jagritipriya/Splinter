from WebLink import EmailObject
from WebLink import DarkMail
from InitializeOwner import FirstMan
from Contacts import Contact
from QureyParser import QueryParser
from Recommendation import Recommender
# Checking the information about the owner
First_Man = FirstMan()
First_Man.Init()

TellMe = QueryParser()
while(1):
    command = input("What can I do for you ?")
    objective = TellMe.WhatDoesMasterNeed(command)
    #objective = 4
    if(objective == 0):
        New_Email = EmailObject()
        EmailHandle = DarkMail()
        EmailHandle.SendMail(New_Email)
    elif(objective == 1):
        First_Name = input("Tell me First Name: ")
        Family_Name = input("Tell me their Family Name: ")
        Add_New_Contact = Contact(First_Name,Family_Name)
    elif(objective == 2):
        EmailHandle = DarkMail()
        EmailHandle.doIHaveAMail()
    elif(objective == 3):
        rc= Recommender()
        rc.JudgeTheRestaurant()
    elif(objective == 4):
        print("Read Mails")
        
    elif(objective == False):
        print("Sorry I couldn't hear you !")

#harshitashankar98@gmail.com
#jagriti.priya16@gmail.com