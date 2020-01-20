import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .models import *
from .hashers import *
from .html import *
import random
import string
from datetime import datetime,timedelta
import jwt
from settings.models import *
from POC.admininfo import *

def Genurl(userobj):
    key = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    userobj.key = key
    userobj.save()
    userdat = [userobj.email,userobj.username,userobj.account_id,key]
    token = "{}".format(jwt.encode({"data":encrypt_message_rsa(str(userdat), jsondata["publickey"]),'token_created_at':str(datetime.now()),
                            'a': {2: True},
                            'exp': datetime.utcnow() + timedelta(seconds=86400)},
                            jsondata["publickey"],
                            algorithm='HS256').decode('utf-8'))
    return '''http://192.168.5.80:8080/adminuser/forgot/referral/?token={}'''.format(token)


def Emailsend(receiver_email):
    try:
        if SMTPdetailModel.objects.filter().exists():
            smtpdb = SMTPdetailModel.objects.get()
            sender_email = smtpdb.SMTP_EMAIL
            smtpurl = smtpdb.SMTPUSERNAME
            smtpport = int(smtpdb.SMTPPORT)
            password = decrypt_message_rsa(smtpdb.SMTPPASSWORD, jsondata["privatekey"])
        else:
            sender_email = jsondata["SMTP_EMAIL"]
            smtpurl = jsondata["SMTPUSERNAME"]
            smtpport = int(jsondata["SMTPPORT"])
            password = decrypt_message_rsa(jsondata["SMTPPASSWORD"], jsondata["privatekey"])
        message = MIMEMultipart("alternative")
        message["Subject"] = "Reset your Password for Admin LTE Technologies Referral Program Referral Account"
        message["From"] = sender_email
        message["To"] = receiver_email.email
        now = datetime.now()
        EMAIL_CONTENT = {"username":receiver_email.username,"rmpurl":Genurl(receiver_email),"fromname":"Admin LTE"}
        COPYRIGHT_TEXT = {"year": now.year}
        html = Html(EMAIL_CONTENT,COPYRIGHT_TEXT)
        part1 = MIMEText("","text")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtpurl, smtpport, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email.email, message.as_string()
            )
        return {"msg":ugettext("Mail Successfully Sent")}
    except Exception as e:
        logger.error(e)
        return {"error":e}