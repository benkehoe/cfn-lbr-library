import unittest
import six
import os
import uuid
import datetime

import boto3
import botocore.exceptions
from dateutil.tz import tzlocal

from cfn_custom_resource import CloudFormationCustomResource, utils as ccr_utils

from S3Object import S3Object

class TestS3Object(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bucket = os.environ['TEST_BUCKET']
        cls.key_prefix = cls.__class__.__name__
        
        client = boto3.client('s3')
        paginator = client.get_paginator('list_objects_v2')
        
        response_iterator = paginator.paginate(
            Bucket=cls.bucket,
            Prefix=cls.key(''),
        )
        
        for results in response_iterator:
            if not results['KeyCount']:
                continue
            keys = [c['Key'] for c in results['Contents']]
            delete = {'Objects': [{'Key': key} for key in keys]}
            response = client.delete_objects(
                Bucket=cls.bucket,
                Delete=delete,
            )
    
    @classmethod     
    def key(cls, key):
        return '{}/{}'.format(cls.key_prefix, key)
    
    def test_create_text(self):
        key = self.key('test_create_text')
        properties = {
            'Bucket': self.bucket,
            'Key': key,
            'Text': 'Foobar',
        }
        event = ccr_utils.generate_request('create', 'Custom::S3Object', properties, CloudFormationCustomResource.DUMMY_RESPONSE_URL_SILENT)
        
        obj = S3Object()
        
        capturer = ccr_utils.ResponseCapturer()
        capturer.set(obj)
        
        now = datetime.datetime.now(tzlocal())
        
        obj.handle(event, ccr_utils.MockLambdaContext())
        
        client = boto3.client('s3')
        response = client.head_object(Bucket=self.bucket, Key=key)
        
        self.assertLess(now, response['LastModified'])
        
        #TODO: check object
    
    @unittest.expectedFailure
    def test_create_json(self):
        raise NotImplementedError
    
    @unittest.expectedFailure
    def test_create_binary(self):
        raise NotImplementedError
    
    @unittest.expectedFailure
    def test_update_text_not_moved(self):
        raise NotImplementedError
    
    def test_update_text_moved(self):
        key1 = self.key('test_update_text_moved1')
        properties1 = {
            'Bucket': self.bucket,
            'Key': key1,
            'Text': 'Value1',
        }
        event1 = ccr_utils.generate_request('create', 'Custom::S3Object', properties1, CloudFormationCustomResource.DUMMY_RESPONSE_URL_SILENT)
        
        obj1 = S3Object()
        
        obj1.handle(event1, ccr_utils.MockLambdaContext())
        
        key2 = self.key('test_update_text_moved2')
        properties2 = {
            'Bucket': self.bucket,
            'Key': key2,
            'Text': 'Value2',
        }
        event2 = ccr_utils.generate_request('update', 'Custom::S3Object', properties2, CloudFormationCustomResource.DUMMY_RESPONSE_URL_SILENT,
                                            old_properties=properties1)
        
        obj2 = S3Object()
        
        obj2.handle(event2, ccr_utils.MockLambdaContext())
        
        client = boto3.client('s3')
        response = client.head_object(Bucket=self.bucket, Key=key2)
        
        with self.assertRaises(botocore.exceptions.ClientError):
            response = client.head_object(Bucket=self.bucket, Key=key1)
    
    @unittest.expectedFailure
    def test_delete(self):
        raise NotImplementedError
    
    @unittest.expectedFailure
    def test_additional_properties(self):
        raise NotImplementedError
    
    @unittest.expectedFailure
    def test_two_bodies(self):
        raise NotImplementedError

    @unittest.expectedFailure
    def test_no_body(self):
        raise NotImplementedError
if __name__ == '__main__':
    unittest.main()