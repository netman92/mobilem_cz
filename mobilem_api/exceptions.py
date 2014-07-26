# -*- coding: utf-8 -*-
"""
Exceptions for app mobilem_api
"""

class MobilemApiException(Exception):
    """
    Common app exception
    """
    num = 1000
class MissingSettingException(MobilemApiException):
    """
    Missing settings exception
    """
    num = 1001


class ApiException(MobilemApiException):
    """
    mobile.cz api exception
    """
    num = 1100


class ValidationException(MobilemApiException):
    """
    Common validation exception
    """
    num = 1200

class WrongNumberException(ValidationException):
    """
    Exception if there is a wrong number inserted
    """
    num = 1201

class WrongMessageException(ValidationException):
    """
    Exception if there is a wrong message inserted
    """
    num = 1202

class WrongUrlException(ValidationException):
    """
    Exception if there is a wrong URL inserted
    """
    num = 1203

class WrongDeliveryReportException(ValidationException):
    """
    Exception if there is a wrong delivery report inserted
    """
    num = 1204

