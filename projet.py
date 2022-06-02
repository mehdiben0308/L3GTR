# /usr/bin/env python3
import imaplib
import 
import email
from time import *
import os
import base64
from bs4 import BeautifulSoup
import mimetypes



# PART 1 LOGIN TO SMTPLIB AND IMAPLIB

#1.1
ail = input("please give me ur email : ")
passw= input("now give me ur password : ")
print(ail)
print(passw)
mail= imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(ail, passw)
mail.select("inbox")

#1.2
server= smtplib.SMTP("smtp.gmail.com",587)
server.starttls()
server.login(ail,passw)
answer="Email recieved and attachements downloaded successfully"
list_of_senders = []





#checking mailbox and asking user number of mails to check :

result, data= mail.uid("search", None, "ALL")
item_list=data[0].split()
hm=int(input("tell me how many mails do u want to check from latest one"))
fm=2*hm



#checking the email data :
for i in item_list[-hm:]:
	
	result2, fetched=mail.uid('fetch',i,'(RFC822)')
	raw_read=fetched[0][1].decode("utf-8")
	message_read=email.message_from_string(raw_read)
	subject=message_read['from']
	da=message_read['date']
	counter=1
	for part in message_read.walk():
		if part.get_content_maintype()=="multipart":
			continue
		if part.get('Content-Disposition') is None:
                	continue
		dd=part.get_filename()
		ss="unchecked"
		list_of_senders = list_of_senders + subject
		filename=ss+dd
		content_type=part.get_content_type()
		if not filename:
			ext=mimetypes.guess_extension(content_type)
			if not ext:
				ext='.bin'
			filename='msg_part_nonchecked_%08d%s'  %(counter, ext)
			print(filename)
		counter += 1
#saving the file:
save_path= os.path.join(os.getcwd(),"emails",da,subject)
if not os.path.exists(save_path):
	os.makedirs(save_path)
with open(os.path.join(save_path, filename), 'wb') as fp:
	fp.write(part.get_payload(decode=True))





	
	print(content_type)
	if "plain" in content_type:
		print(part.get_payload())
		print("this is plain")
	elif "html" in content_type:
		html_=part.get_payload()
		soup= BeautifulSoup(html_, "html.parser")
		text= soup.get_text()
		print(text)
		print("html")
	else:
		print(content_type)
		
for b in list_of_senders :
	server.sendmail(ail,b,answer)
server.quit()














