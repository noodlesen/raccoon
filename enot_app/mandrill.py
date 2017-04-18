#import os
import smtplib
import json
from premailer import transform
from datetime import datetime

from django.template import Context
from django.template.loader import get_template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from enot.settings import MANDRILL_USERNAME, MANDRILL_PASSWORD

from django.utils.translation import activate



def send_email(**kwargs):

    msg = MIMEMultipart('alternative')

    msg['Subject'] = kwargs['subject']
    msg['From']    = kwargs['sender']
    # format: "sender name <sender@email>"
    msg['To']      = kwargs['to']

    text = "К сожалению, наша рассылка поддерживает только HTML формат письма"
    part1 = MIMEText(text, 'plain')

    activate('ru')

    html = transform(
        get_template(kwargs['template']).render(Context(kwargs['context']))
    )
    part2 = MIMEText(html, 'html')


    username = MANDRILL_USERNAME
    password = MANDRILL_PASSWORD

    msg.attach(part1)
    msg.attach(part2)

    s = smtplib.SMTP('smtp.mandrillapp.com', 587)

    s.login(username, password)
    s.sendmail(msg['From'], msg['To'], msg.as_string())

    s.quit()




