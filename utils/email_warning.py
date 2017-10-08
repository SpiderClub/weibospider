import os
from traceback import format_tb

import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import (
    parseaddr, formataddr)

from config import get_email_args
from logger import other


email_args = get_email_args()
smtp_server = email_args['server']
smtp_port = email_args['port']
from_addr = os.getenv('EMAIL_ACCOUNT') or email_args['from']
from_password = os.getenv('EMAIL_PASS') or email_args['password']
to_addr = os.getenv('EMAIL_TO') or email_args['to']
email_subject = email_args['subject']
warning_info = email_args['warning_info']


def _format_addr(nick_addr):
    name, addr = parseaddr(nick_addr)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def gen_msg(content, subject, from_nick=None, to_nick=None):
    if from_nick is None:
        from_nick = from_addr
    if to_nick is None:
        to_nick = to_addr
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = _format_addr('{} <{}>'.format(from_nick, from_addr))
    msg['To'] = _format_addr('{} <{}>'.format(to_nick, to_addr))
    msg['Subject'] = Header(subject).encode()
    return msg


def send_email(email_from=from_addr, email_pass=from_password, to_addrs=None, server=smtp_server, port=smtp_port,
               from_nick='weibospider', to_nick='SpiderUser'):
    if to_addrs is None or isinstance(to_addrs, str):
        to_addrs = [to_addr]
    msg = gen_msg(warning_info, email_subject, from_nick, to_nick)
    server = smtplib.SMTP(server, port)
    try:
        server.starttls()
        server.login(from_addr, email_pass)
        rs = server.sendmail(email_from, to_addrs, msg.as_string())
    except Exception as e:
        other.error('failed to send emails, {} is raised, here are details:{}'.format(e, format_tb(e.__traceback__)[0]))
    else:
        return rs
    finally:
        server.quit()
