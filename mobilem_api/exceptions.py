# -*- coding: utf-8 -*-


class MobilemApiException(Exception):
	num = 1000
class MissingSettingException(MobilemApiException):
	num = 1001


class ApiException(MobilemApiException):
	num = 1100



class ValidationException(MobilemApiException):
	num = 1200

class WrongNumberException(ValidationException):
	num = 1201

class WrongMessageException(ValidationException):
	num = 1202

class WrongUrlException(ValidationException):
	num = 1203

class WrongRecackException(ValidationException):
	num = 1204

