import hashlib  
from urllib.request import urlretrieve
from smtplib import SMTP_SSL as SMTP, SMTPException
from email.mime.text import MIMEText
import json

PATH = 'Downloads/'


def MD5(filename):
    md5 = hashlib.md5()
    try:
        with open(PATH + filename, "rb") as file:
            for i in iter(lambda: file.read(4096), b""):
                md5.update(i)
        return md5.hexdigest()
    except IOError as error:
        return -1


def sendMassage(fileUrl, md5, toEmail):
    fromEmail = "youremail@mail" # set email
    textMessage = '''Your file ''' + fileUrl + '''\nMD5 =  ''' + str(md5)
    msg = MIMEText(textMessage, 'plain')
    msg['Subject'] = "BostonGene"
    
    try:
        server = SMTP('smtp.mail.ru') # set server
        server.login("youremail@mail", "yourpassword") # set login and password
        server.sendmail(fromEmail, toEmail, msg.as_string())
        server.quit()
        return True
    except SMTPException as e:
        return False


def handleFile(email, fileUrl, filename):
    try:
        urlretrieve(fileUrl, PATH + filename)
    except:
        return False
    
    md5 = MD5(filename)
    
    if (md5 == -1): 
        return False
    if (email):
        if (sendMassage(fileUrl, md5, email)):
            responseData = {}
            responseData["md5"] = md5
            responseData["url"] = fileUrl
            return responseData
        else:
            return False

    responseData = {}
    responseData["md5"] = md5
    responseData["url"] = fileUrl
    return responseData
    
