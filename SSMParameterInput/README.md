```yaml
MySSMParameter:
  Type: Custom::SSMParameterInput
  Properties:
    Name: My/Parameter/Name
```

A drop-in replacement for CloudFormation SSM parameter types
(see https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html#aws-ssm-parameter-types )
CloudFormation SSM parameter types don't allow for building the key from other 
inputs. They also don't allow for SecureString types. This resource will allow
getting the encrypted value of a SecureString, and the KeyId is available as
an attribute.

Access value by Ref-ing the resource.
All outputs from GetParameter are available as attributes.
