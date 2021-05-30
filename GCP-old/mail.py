# send mail
import smtplib

# need to install sendmail for the script to send emails.

sender = 'mb2love@gmail.com'
rec = ['maximb@cloudnow.co.il']

msg = """From: From Person <mb2love@gmail.com>
To: To Person <maximb@cloudnow.co.il>
Subject: SMTP e-mail test 3

This is a test e-mail message.
"""

#smtplib.SMTP('mb2love@gmail.com', 25)
smtpObj = smtplib.SMTP('localhost')
smtpObj.sendmail(sender, rec, msg)
print "Successfully sent email"


'''
try:
    smtplib.SMTP('mb2love@gmail.com', 25)
    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(send, rec, msg)
    print "Successfully sent email"
except SMTPException:
    print "Error: unable to send email"
'''
