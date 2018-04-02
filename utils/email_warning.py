from traceback import format_tb

import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import (
    parseaddr, formataddr)

from logger import other_logger
from config import (
    email_from, email_password,
    email_port, email_server,
    warning_info, subject
)


def _format_addr(nick_addr):
    name, addr = parseaddr(nick_addr)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def gen_msg(content, subject, email_from, email_to, from_nick=None, to_nick=None):
    if from_nick is None:
        from_nick = email_from
    if to_nick is None:
        to_nick = email_to
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = _format_addr('{} <{}>'.format(from_nick, email_from))
    msg['To'] = _format_addr('{} <{}>'.format(to_nick, email_to))
    msg['Subject'] = Header(subject).encode()
    return msg


def send_email(email_from=email_from, email_pass=email_password,
               to_addrs=None, server=email_server, port=email_port,
               from_nick='weibospider', to_nick='SpiderUser'):
    if to_addrs is None or isinstance(to_addrs, str):
        to_addrs = [to_addrs]
    msg = gen_msg(warning_info, subject, email_from, to_addrs[0],
                  from_nick, to_nick)
    server = smtplib.SMTP(server, port)
    try:
        server.starttls()
        server.login(email_from, email_pass)
        rs = server.sendmail(email_from, to_addrs, msg.as_string())
    except Exception as e:
        other_logger.error('Failed to send emails, {} is raised, '
                           'here are details:{}'.format(e, format_tb(
            e.__traceback__)[0]))
    else:
        return rs
    finally:
        server.quit()
