import unittest
import six
import os

import boto3
import botocore.exceptions

from cfn_custom_resource import CloudFormationCustomResource, utils as ccr_utils

from SSMParameterInput import SSMParameterInput

secure_string_key_id = os.environ.get('TEST_SECURE_STRING_KEY_ID')
TEST_SECURE = bool(secure_string_key_id)

class TestSSMParameterInput(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.name_prefix = '/{}'.format(cls.__class__.__name__)
        
        client = boto3.client('ssm')
        
        cls.param_string_name = cls.name('string_param')
        cls.param_string_value = 'string param value'
        
        cls.param_stringlist_name = cls.name('stringlist_param')
        cls.param_stringlist_value = 'foo,bar,baz'
        
        if TEST_SECURE:
            cls.param_securestring_name = cls.name('securestring_param')
            cls.param_securestring_value = 'secure_val'
            cls.param_securestring_key_id = secure_string_key_id
        
        cls.nonexistant_param_name = cls.name('nonexistant')
        
        paginator = client.get_paginator('get_parameters_by_path')
        response_iterator = paginator.paginate(
            Path=cls.name_prefix,
            Recursive=True,
        )
        
        names = []
        for response in response_iterator:
            names.extend(p['Name'] for p in response['Parameters'])
        
        if names:
            client.delete_parameters(
                Names=names,
            )
        
        client.put_parameter(
            Name=cls.param_string_name,
            Value=cls.param_string_value,
            Type='String',
        )
        
        client.put_parameter(
            Name=cls.param_stringlist_name,
            Value=cls.param_stringlist_value,
            Type='StringList',
        )
        
        if TEST_SECURE:
            client.put_parameter(
                Name=cls.param_securestring_name,
                Value=cls.param_securestring_value,
                Type='String',
                KeyId=cls.param_securestring_key_id,
            )
        
    @classmethod     
    def name(cls, name):
        return '{}/{}'.format(cls.name_prefix, name)
    
    def test_create_string(self):
        properties = {
            'Name': self.param_string_name,
        }
        event = ccr_utils.generate_request('create', 'Custom::SSMParameterInput', properties, CloudFormationCustomResource.DUMMY_RESPONSE_URL_SILENT)
        
        obj = SSMParameterInput()
        
        capturer = ccr_utils.ResponseCapturer()
        capturer.set(obj)
        
        obj.handle(event, ccr_utils.MockLambdaContext())
        
        self.assertEqual(obj.physical_resource_id, self.param_string_value)

if __name__ == '__main__':
    unittest.main()