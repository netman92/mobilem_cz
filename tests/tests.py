# -*- coding: utf-8 -*-

from django.test import SimpleTestCase
from unittest import TestCase
from mobilem_api.models import SmsModel
from mobilem_api.exceptions import *
import pdb


class SmsBaseTest(TestCase):

    def test_basic_constructor(self):
        """
        Test constructor of SmsModel
        """

    	sms = SmsModel('name', 'pass')
        
        actual  = sms.getUserName()
        expected = 'name'
        self.assertEqual(expected, actual)



    def test_sms_url(self):
        """
        Test SMS API URL
        """

    	sms = SmsModel('testuser', 'testpassword')
        sms.dry = True
        sms.send_sms("+420123456789","testsms")

    	
    	actual = sms.build_query() 
    	expected = sms.api_url + "?action=send&msisdn=%2B420123456789&login=testuser&auth=3f5fdc05d63cb36677f8e3317742c812&msg=testsms"

    	self.assertEqual(expected, actual)

    def test_number_verification_start_with_plus(self):
        """
        Test number verification (start with +)
        """

        sms = SmsModel('testuser', 'testpassword')
        sms.dry = True
        
        try:
            sms.send_sms("420123456789","testsms")
            self.fail('sms.send_sms("420123456789","testsms") should throw WrongNumberException')
        except WrongNumberException as e:
            pass
        except:
            self.fail('sms.send_sms("420123456789","testsms") should throw WrongNumberException')

    def test_number_verification_contains_letter(self):
        """
        Test number verification contains letter
        """

        sms = SmsModel('testuser', 'testpassword')
        sms.dry = True

        try:
            sms.send_sms("420a23456789","testsms")
            self.fail('sms.send_sms("420a23456789","testsms") should throw WrongNumberException')
        except WrongNumberException as e:
            pass
        except:
            self.fail('sms.send_sms("420a23456789","testsms") should throw WrongNumberException')
    
    def test_number_verification_empty(self):
        """
        Test number verification empty num
        """

        sms = SmsModel('testuser', 'testpassword')
        sms.dry = True

        try:
            sms.send_sms("","testsms")
            self.fail('sms.send_sms("","testsms") should throw WrongNumberException')
        except WrongNumberException as e:
            pass
        except:
            self.fail('sms.send_sms("","testsms") should throw WrongNumberException')


    def test_message_verification_empty(self):
        """
        Test message verification empty msg
        """

        sms = SmsModel('testuser', 'testpassword')
        sms.dry = True

        try:
            sms.send_sms("+1234","")
            self.fail('sms.send_sms("+1234","") should throw WrongMessageException')
        except WrongMessageException as e:
            pass
        except:
            self.fail('sms.send_sms("+1234","") should throw WrongMessageException')

    def test_message_accents_remove(self):
        """
        Test message remove accents
        """

        sms = SmsModel('testuser', 'testpassword')
        sms.dry = True
        sms.send_sms("+420123456789","ľščťžýáíétôä")

        
        actual = sms.build_query() 
        expected = sms.api_url + "?action=send&msisdn=%2B420123456789&login=testuser&auth=89cc9f0e58351dcddea1e60c1685d914&msg=lsctzyaietoa"

        self.assertEqual(expected, actual)


    def test_sms_others_params(self):
        """
        Test sms others params
        """

        sms = SmsModel('testuser', 'testpassword')
        sms.dry = True
        sms.send_sms(number = "+420123456789", msg = "ahoj", others = 'test=hello&test2=world')

        
        actual = sms.build_query() 
        expected = sms.api_url + "?test2=world&msisdn=%2B420123456789&auth=e897b7d014a4b1f9cfaedacaa8163254&test=hello&action=send&login=testuser&msg=ahoj"

        self.assertEqual(expected, actual)

    def test_api_recac_worng(self):
        """
        Test sms recac wrong
        """

        sms = SmsModel('testuser', 'testpassword')
        sms.dry = True
        

        try:
            sms.send_sms(number = "+420123456789", msg = "ahoj", delivery_report =  "test")
            self.fail('sms.send_sms(number = "+420123456789", msg = "ahoj", recac = "test") should throw WrongRecackException')
        except WrongRecackException as e:
            pass
        except:
            self.fail('sms.send_sms(number = "+420123456789", msg = "ahoj", recac = "test") should throw WrongRecackException')

    def test_api_recack(self):
        """
        Test sms recack good
        """

        sms = SmsModel('testuser', 'testpassword')
        sms.dry = True
        sms.send_sms(number = "+420123456789", msg = "ahoj", delivery_report =  "http://test.com")

        actual = sms.build_query() 
        expected = sms.api_url + "?recack=1&msisdn=%2B420123456789&auth=e897b7d014a4b1f9cfaedacaa8163254&msg=ahoj&action=send&login=testuser&recackaddr=http%3A%2F%2Ftest.com"

        self.assertEqual(expected, actual)

        sms = SmsModel('testuser', 'testpassword')
        sms.dry = True
        sms.send_sms(number = "+420123456789", msg = "ahoj", delivery_report =  "test@test.com")

        actual = sms.build_query() 
        expected = sms.api_url + "?recack=1&msisdn=%2B420123456789&auth=e897b7d014a4b1f9cfaedacaa8163254&msg=ahoj&action=send&login=testuser&recackaddr=test%40test.com"

        self.assertEqual(expected, actual)
        

