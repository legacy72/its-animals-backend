import re
import smtplib
import dns.resolver
from rest_framework.exceptions import ParseError
from dns.resolver import NXDOMAIN, NoAnswer
from disposable_email_domains import blocklist


def is_valid_format(email):
    regex = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if not re.match(regex, email):
        raise ParseError(detail="Введите настоящий email адрес")


def mx_lookup(domain):
    try:
        records = dns.resolver.resolve(domain, "MX")
    except NXDOMAIN:
        raise ParseError(detail="Доменное имя не найдено. Email невалидный")
    except NoAnswer:
        raise ParseError(
            detail="У домена осутствует Mail Exchanger. Email невалидный"
        )
    mxRecord = records[0].exchange
    mxRecord = str(mxRecord)
    return mxRecord


def get_smpt_response(mxRecord, fromAddress, addressToVerify):
    server = smtplib.SMTP()
    server.set_debuglevel(0)

    # SMTP Conversation
    server.connect(mxRecord)
    # server.local_hostname(Get local server hostname)
    server.helo(server.local_hostname)
    server.mail(fromAddress)
    code, message = server.rcpt(str(addressToVerify))
    server.quit()


    if code != 250:
        raise ParseError(detail="Нет ответа от SMTP-сервера. Email невалидный")
    return code, message


def get_domain(email):
    splitAddress = email.split("@")

    domain = str(splitAddress[1])
    if domain in blocklist:
        raise ParseError(detail="Домен занесен в черный список. Email невалидный")

    return domain
