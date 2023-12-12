from socket import *
import config
import os
from tkinter import *


from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase


bufferSize = 2048
client_socket = socket(AF_INET, SOCK_STREAM)  

def recv_msg():
  try:
    return client_socket.recv(bufferSize).decode()
  except timeout:
    return None  

def send_msg(message, expect_return_msg=True):
  client_socket.send(f"{message}\r\n".encode())
  recv = recv_msg()
  if expect_return_msg:
    print(recv)
    return recv
  
def ehlo():
    send_msg("EHLO",False)
    
def quit():
  return send_msg("QUIT",False)

def connect():
  client_socket.connect((config.mailServer, config.smtp))
  ehlo()
  
def send_mail(subject,body, from_addr, toEmail,ccEmail,bccEmail):
  email_header = f"From: {from_addr}\r\n"
  email_header += f"To: {",".join(toEmail)}\r\n"
  
  if len(ccEmail)>0:
    email_header += f"Cc: {",".join(ccEmail)}\r\n"
 
  if len(bccEmail)>0 :
    email_header += f"Bcc: {",".join(bccEmail)}"
  send_msg(f"MAIL FROM:<{from_addr}>")
  
  if len(toEmail+ccEmail)>0 :
    for mail in toEmail + ccEmail : 
      send_msg(f"RCPT TO:<{mail}>")
    send_msg(f"DATA")
    send_msg(f"{email_header}", expect_return_msg=False)
    send_msg(f"Subject: {subject}\r\n{body}\r\n.", expect_return_msg=False)
 
# gui file
def send_file(subject, body, from_addr, toEmail, ccEmail, bccEmail, attachment_path=None):
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = ",".join(toEmail)
    msg["Subject"] = subject

    if len(ccEmail) > 0:
        msg["Cc"] = ",".join(ccEmail)

    if len(bccEmail) > 0:
        print("kakakakaa")
        msg["Bcc"] = ",".join(bccEmail)

    # Thêm nội dung email
    msg.attach(MIMEText(body, 'plain'))

    if attachment_path:
        attachment = MIMEBase('application', 'octet-stream')
        with open(attachment_path, 'rb') as attachment_file:
            attachment.set_payload(attachment_file.read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', f'attachment; filename="{attachment_path}"')
        msg.attach(attachment)

    send_msg(f"MAIL FROM:<{from_addr}>")

    if len(toEmail + ccEmail) > 0:
        for mail in toEmail + ccEmail:
            send_msg(f"RCPT TO:<{mail}>")

    send_msg("DATA")

    send_msg(msg.as_string(), expect_return_msg=False)

    send_msg(".", expect_return_msg=False)
  
connect()

