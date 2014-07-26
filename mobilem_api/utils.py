# -*- coding: utf-8 -*-
# pylint: disable=line-too-long

"""
Utils and helper functions for API
"""

import hashlib, re, unicodedata
from django.core.validators import URLValidator, EmailValidator
from mobilem_api.exceptions import WrongNumberException, WrongMessageException, WrongUrlException, WrongDeliveryReportException

#helper methods
def md5(string):
    """
    Just generate md5
    """
    return hashlib.md5(string).hexdigest()

#validation methods
def validate_number(number):
    """
    Validate phone number
    """

    #0 chcek for empty
    if number == '' or not number:
        exception_text = "Inserted number is empty."
        raise WrongNumberException(exception_text)

    #1 check first is plus sign
    if not number.startswith('+') and not number.startswith('00'):
        exception_text = "Number: '%s' does not start with plus (+) sign." % (number, )
        raise WrongNumberException(exception_text)

    #2 replacing spaces, and whitespaces
    number = number.strip().replace(' ', '')

    #3 except + sign, number must containst only digits
    tmp_num = number[1:] if number.startswith('+') else number
    if re.search(r'\D+', tmp_num):
        exception_text = "Number: '%s' does contains letters" % (number, )
        raise WrongNumberException(exception_text)
    return number

def validate_message(message):
    """
    Validate message
    """
    #0 chcek for empty
    if message == '' or not message:
        exception_text = "Inserted message is empty."
        raise WrongMessageException(exception_text)

    #remove accents
    message = unicode(message.decode('utf-8'))
    message = ''.join(c for c in unicodedata.normalize('NFD', message) if unicodedata.category(c) != 'Mn')

    return message

def validate_url(url):
    """
    Validate URL
    """
    val = URLValidator()
    try:
        val(url)
    except Exception:
        exception_text = "Inserted URL '%s' is not URL." % url
        raise WrongUrlException(exception_text)

    return url

def validate_delivery_report(recack):
    """
    Validate delivery report (Email OR Url)
    """
    try:
        validate_url(recack)
        return recack
    except WrongUrlException:
        try:
            val = EmailValidator()
            val(recack)
            return recack
        except:
            exception_text = "Param delivery_report (== '%s') is URL nor email" % recack
            raise WrongDeliveryReportException(exception_text)
