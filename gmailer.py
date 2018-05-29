#!/usr/bin/env python
# 
# Gmailer
# Louis Scianni

import smtplib 
import email.utils
from email.mime.text import MIMEText
from sys import argv
from getpass import getpass

def get_help():
    print('gmailer\nSend and email from a gmail account\nusage:gmailer.py [emailaddress] [subject] [recipient]')

def get_msg():
    msg = input('message:')
    return msg
    
def send_mail(sender, passwd, subjt, recv):
    """
    Send emails with a gmail account 
    """
    user_msg = get_msg()
    
    author = str(sender.split('@')[0]) # strip username from email address to use as author
    
    msg = MIMEText(user_msg)
    msg.set_unixfrom(author)
    msg['To'] = email.utils.formataddr(('Recipient', recv))
    msg['From'] = email.utils.formataddr((author, sender))
    msg['Subject'] = subjt
    
    smtp_obj = smtplib.SMTP('smtp.gmail.com')
    
    try:
        smtp_obj.set_debuglevel(True)
        smtp_obj.ehlo()

        if smtp_obj.has_extn('STARTTLS'): # If server supports starttls initialize TLS
            smtp_obj.starttls()
            smtp_obj.ehlo()
            
        smtp_obj.login(sender, passwd)        # authenticate
        smtp_obj.sendmail(sender, [recv], msg.as_string()) # send message to server
    finally:
        smtp_obj.quit()
    
try:
    sender = argv[1]
    passwd = getpass('%s\' password:' % sender)
    subject = argv[2]
    receivers = argv[3]
    
except IndexError:
    get_help()
    
if __name__ == '__main__':
    try:
        send_mail(sender, passwd, subject, receivers)
    except NameError:
        pass