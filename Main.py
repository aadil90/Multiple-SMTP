"""
Written by
Muhammad Aadil
"""
#Import essential Libraries
import smtplib as SM
import json as js
import os
import datetime as dt
import time
import csv

TimerStart = time.perf_counter()
STD = []

#Importing Config Files 
CONFIG_FILE_NAME = "Config.json"
FILE = open(CONFIG_FILE_NAME)
MAIN_CONFIG_FILE = js.load(FILE)

# Email File Collection

EMAILS_FILE = MAIN_CONFIG_FILE['Files']['Emails']['FileName']

try:
    EMAILS = open(EMAILS_FILE)
    EMAILS = EMAILS.read().split('\n')
except FileNotFoundError:
    print('File Not Found Please Review Config file \
          and Set proper file for Emails')

# BODY File Collection for Email Message

BODY_FILE = MAIN_CONFIG_FILE['Files']['Body']['FileName']

try:
    MESSAGE = open(BODY_FILE)
    MESSAGE = MESSAGE.read()
except FileNotFoundError:
    print('File Not Found Please Review Config file \
          and Set proper file for Message Body')

# Server File Collection for IP Rotation

SERVER_FILE_JSON = MAIN_CONFIG_FILE['Files']['Servers']['FileName']

try:
    SERVERS_FILE = open(SERVER_FILE_JSON)
    SERVERS_FILE = SERVERS_FILE.read().split('\n')
    SERVERS_FILE_STR = ''.join(SERVERS_FILE)
    SERVERS_FILE = js.loads(SERVERS_FILE_STR)
    
    SERVER_HOST = SERVERS_FILE['Server']['HOST']
    SERVER_PORT = SERVERS_FILE['Server']['Port']
    SERVER_IP   = SERVERS_FILE['Server']['IP']
    SERVER_Domain = SERVERS_FILE['Server']['Domain']
    SERVER_SubDomain = SERVERS_FILE['Server']['SubDomain']   
    SERVER_EMAIL = SERVERS_FILE['Server']['Email']
    SERVER_PASS  = SERVERS_FILE['Server']['Password']
    
    
except FileNotFoundError:
    print('File Not Found Please Review Config file \
          and Set proper file for SERVER file')

                      
def SEND_EMAIL(SERVER_HOST,SERVER_PORT,SENDER,RECIEVER,MESSAGE,PASSWORD):
    """
    
    """
    try:
        SERVER_TO_RUN = SM.SMTP(SERVER_HOST,SERVER_PORT)
        SERVER_TO_RUN.starttls()
        SERVER_TO_RUN.login(SENDER,PASSWORD)
        
        for ONE_EMAIL in RECIEVER:
            MESSAGE_TO_SEND = f'Email Sent by:\n{SENDER} \n\n' +MESSAGE+ '\n\nRecieved by : \n'\
            + ONE_EMAIL + ' \nEnd of Email\n'
            # print(MESSAGE_TO_SEND)
            # print(ONE_EMAIL)
            # SERVER_TO_RUN.sendmail(SENDER, ONE_EMAIL, MESSAGE)
            STD.append(MESSAGE_TO_SEND)
        
    except SM.SMTPException:
        print('SMTP Exception Unknown Error - Sorry we are unable to send\
              email to ' + RECIEVER)
    finally:
        SERVER_TO_RUN.quit()
        
SEND_EMAIL(SERVER_HOST, SERVER_PORT, SERVER_EMAIL , EMAILS, MESSAGE, SERVER_PASS)

# --------------LOG FILE GENERATOR
if not os.path.isdir('./Log'):
    os.mkdir('./Log')

DateTime = dt.datetime.today()
DateTime = str(DateTime)
DateTime = DateTime.replace(':','-')+'.txt'
DateTime = DateTime.replace(' ', '_')

file = str('Log/'+'LogFile'+DateTime.replace(' ', ''))

BeautifyUpper = '=' *40
DateTimeToWrite = str(dt.datetime.today())
BeautifyLower = '=' *40

BeautifyFinal = BeautifyUpper +'\n' + DateTimeToWrite \
    +'\n' + BeautifyLower +'\n'
    
# print(BeautifyFinal)

StopTimer = time.perf_counter()
Elapsed = StopTimer - TimerStart
Elapsed = float('{:.2f}'.format(Elapsed))

# print(Elapsed)

DateTimeToWriteInLast = str(dt.datetime.today()) 
BeautifyFinalInLast = BeautifyUpper  +'\n' + DateTimeToWriteInLast \
    +'\n' +BeautifyLower +'\n'+BeautifyUpper\
        +'\n'+'Elapsed Time in Seconds '+\
            str(Elapsed)  +'\n' + BeautifyLower  +'\n' 
print(BeautifyFinalInLast)
with open(file, 'w') as PerLine:
    PerLine.write(BeautifyFinal)
    for EachMail in STD:
        PerLine.write(f'\n\n****\n{EachMail}\n\n****\n')
    PerLine.write(BeautifyFinalInLast)
