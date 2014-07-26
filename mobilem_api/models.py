# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from exceptions import *
from django.core.validators import URLValidator, EmailValidator

import hashlib, urllib, requests, re, unicodedata

class SmsModel():
    __username = None
    __password = None
    __api_settings = None

    action = None
    parameters = None
    response = None
    

    dry = False
    api_url = "http://api.mobilem.cz/xmlapi2.xp"


    def __init__(self, user = None, password = None, action = None):
        self.__username = user if user else None
        self.__password = password if password else None
        self.action = action if action else "send"

        try:
            self.__api_settings = settings.MOBILEM_CZ_API
        except AttributeError:
            exception_text = "Missing 'MOBILEM_CZ_API' dict in your settings. Please read the instructions."
            raise MissingSettingException(exception_text)

        #api url 
        if 'api_url' in self.__api_settings.keys():
            self.api_url = self.__validate_url( self.__api_settings['api_url'] )

        #username, pass fallback
        if not self.__username or not self.__password:            

            #username missing
            if not self.__username:
                if 'username' in self.__api_settings.keys():
                    self.__username = self.__api_settings['username']
                else:
                    exception_text = "Missing 'username' in MOBILEM_CZ_API settings. Please read the instructions."
                    raise MissingSettingException(exception_text)

            #password missing
            if not self.__password:
                if 'password' in self.__api_settings.keys():
                    self.__password = self.__api_settings['password']
                else:
                    exception_text = "Missing 'password' in MOBILEM_CZ_API settings. Please read the instructions."
                    raise MissingSettingException(exception_text)



        self.parameters = {
            'action' : self.action,
            'login' : self.__username,
        }

    # getters
    def getUserName(self):
        return self.__username

    #helper methods
    def __md5(self, string):
        return hashlib.md5(string).hexdigest()

    #validation methods
    def __validate_number(self, number):
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
        if re.search( r'\D+', tmp_num):
            exception_text = "Number: '%s' does contains letters" % (number, )
            raise WrongNumberException(exception_text)
        return number

    def __validate_message(self, message):
        #0 chcek for empty
        if message == '' or not message:
            exception_text = "Inserted message is empty."
            raise WrongMessageException(exception_text)

        #remove accents
        message = unicode(message.decode('utf-8'))
        message =  ''.join(c for c in unicodedata.normalize('NFD', message) if unicodedata.category(c) != 'Mn') 

        return message

    def __validate_url(self, url):
        val = URLValidator()
        try:
            val(url)
        except Exception:
            exception_text = "Inserted URL '%s' is not URL." % url
            raise WrongUrlException(exception_text)

        return url

    def __validate_recack(self, recack):
        try:
            self.__validate_url(recack)
            return recack
        except WrongUrlException as e:
            try:
                val = EmailValidator()
                val(recack)
                return recack
            except:
                exception_text = "Param recack (== '%s') is URL nor email" % recack
                raise WrongRecackException(exception_text)



    def build_query(self):

        self.parameters['auth'] = self.__md5( self.__md5(self.__password) + self.__username + self.action + self.parameters['msg'][0:31] ) 

        return self.api_url + "?%s" % (urllib.urlencode(self.parameters))


    def send_sms(self, number, msg, delivery_report = None, delay = None, nosave = None, split = None, nick = None, others = None):
        self.response = None

        #settings fallback
        if 'url_params' in self.__api_settings.keys() and type(self.__api_settings['url_params']) == dict:
            for key, val in self.__api_settings['url_params'].iteritems():
                self.parameters[key] = val

        #mandatory params
        self.parameters['msisdn'] = self.__validate_number(number)
        self.parameters['msg'] = self.__validate_message(msg)

        #obligatory params
        if delivery_report:
            self.parameters['recack'] = 1
            self.parameters['recackaddr'] = self.__validate_recack(delivery_report)
        if delay:
            self.parameters['delay'] = delay #validate datetime

        #simple obligatory params
        if nosave:
            self.parameters['nosave'] = 1
        if split:
            self.parameters['split'] = 1
        if nick:
            self.parameters['nick'] = 1

        #others - fallback if we want to add params to URL not supported params in current implementation
        if others:
            splited = others.split('&')
            for param in splited:
                [name, value] = param.split('=')
                self.parameters[name] = value
        
        if not self.dry:
            return self.send_it()

    def send_it(self):
        if 'method' in self.__api_settings.keys():
            if self.__api_settings['method'].lower() == 'post':
                self.response = requests.post ( self.build_query() )
                return self.response
        
        self.response = requests.get ( self.build_query() )
        return self.response