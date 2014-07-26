# -*- coding: utf-8 -*-
# pylint: disable=line-too-long, too-many-arguments

"""
models for mobilem_api
"""

from django.conf import settings
from mobilem_api.exceptions import MissingSettingException
from mobilem_api.utils import md5, validate_number, validate_message, validate_url, validate_delivery_report

import urllib, requests

class SmsModel(object):
    """
    Model for sending SMS
    """
    __username = None
    __password = None
    __api_settings = None

    action = None
    parameters = None
    response = None

    dry = False
    api_url = "http://api.mobilem.cz/xmlapi2.xp"


    def __init__(self, user=None, password=None, action=None):
        self.__username = user if user else None
        self.__password = password if password else None
        self.action = action if action else "send"

        try:
            self.__api_settings = settings.MOBILEM_CZ_API
        except AttributeError:
            exception_text = "Missing 'MOBILEM_CZ_API' dict in your settings."
            exception_text += "Please read the instructions."

            raise MissingSettingException(exception_text)

        #api url
        if 'api_url' in self.__api_settings.keys():
            self.api_url = validate_url(self.__api_settings['api_url'])

        #username, pass fallback
        if not self.__username or not self.__password:

            #username missing
            if not self.__username:
                if 'username' in self.__api_settings.keys():
                    self.__username = self.__api_settings['username']
                else:
                    exception_text = "Missing 'username' in MOBILEM_CZ_API settings."
                    exception_text += "Please read the instructions."
                    raise MissingSettingException(exception_text)

            #password missing
            if not self.__password:
                if 'password' in self.__api_settings.keys():
                    self.__password = self.__api_settings['password']
                else:
                    exception_text = "Missing 'password' in MOBILEM_CZ_API settings."
                    exception_text += "Please read the instructions."
                    raise MissingSettingException(exception_text)



        self.parameters = {
            'action' : self.action,
            'login' : self.__username,
        }

    # getters
    def get_user_name(self):
        """
        Username getter
        """
        return self.__username

    def build_query(self):
        """
        Method for build clean query with params
        """

        self.parameters['auth'] = md5(md5(self.__password) + self.__username + self.action + self.parameters['msg'][0:31])

        return self.api_url + "?%s" % (urllib.urlencode(self.parameters))


    def send_sms(self, number, msg, delivery_report=None, delay=None, nosave=None, split=None, nick=None, others=None):
        """
        Method for set attrs and send SMS
        """
        self.response = None

        #settings fallback
        if 'url_params' in self.__api_settings.keys() and type(self.__api_settings['url_params']) == dict:
            for key, val in self.__api_settings['url_params'].iteritems():
                self.parameters[key] = val

        #mandatory params
        self.parameters['msisdn'] = validate_number(number)
        self.parameters['msg'] = validate_message(msg)

        #obligatory params
        if delivery_report:
            self.parameters['recack'] = 1
            self.parameters['recackaddr'] = validate_delivery_report(delivery_report)
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
            return self.__send_it()

    def __send_it(self):
        """
        Internal method for sending SMS
        """
        if 'method' in self.__api_settings.keys():
            if self.__api_settings['method'].lower() == 'post':
                self.response = requests.post(self.build_query())
                return self.response

        self.response = requests.get(self.build_query())
        return self.response
