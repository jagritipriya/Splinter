from fuzzywuzzy import fuzz 
from fuzzywuzzy import process 

class QueryParser:
    choices = ["Send an email","Add a new contact","read my mails","Recommend me a restaurant"]
    choice2switch = {"Send an email":0,"Add a new contact":1,"read my mails":2,"Recommend me a restaurant":3}
    def WhatDoesMasterNeed(self,raw_text = ''):
        if raw_text == '':
            return False
        objective = process.extractOne(raw_text,self.choices)[0]

        return self.choice2switch[objective]
    def isAgreeing(self,choice):
        choices = ["yeah","sure","definetly","yes","tell me","go ahead","obviously","no","not at all","stop","leave it","oh no"]
        objective = process.extractOne(choice,choices)[0]
        not_agreeing = ["no","not at all","stop","leave it","oh no"]
        agreeing = ["yeah","sure","definetly","yes","tell me","go ahead","obviously"]
        #print("Objective is : ",objective)
        if objective in agreeing:
            return True
        else:
            return False
    
    def matchChoices(self,choice,choices):
        return process.extractOne(choice,choices)[0]