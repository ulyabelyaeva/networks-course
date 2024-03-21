#!/usr/local/bin/python2

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(frm, to, subj, text, html):
    # msg = email.mime.text.MIMEText(text)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subj
    msg['From'] = frm
    msg['To'] = to

    # Send the message via our own SMTP server, but don't include the
    # envelope header.

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    s = smtplib.SMTP('mail.cfd.spb.ru', 25)
    s.login('worker@cfd.spb.ru', '') # I removed my pasword ^-^, sorry (
    s.sendmail(frm, (to), msg.as_string())
    s.quit()


text = "Hiiiii!"
html = """\
<html>
  <head></head>
  <body>
    <p>That's homework <a href="https://github.com/ulyabelyaeva/networks-course/blob/master/lab05/lab05.md">link</a> you wanted.
    </p>
  </body>
</html>
"""
send_email('worker@cfd.spb.ru', 'ulyss.spb@gmail.com', 'Subject', text, html)
