```yaml
MySSMParameter:
  Type: Custom::SSMParameterInput
  Properties:
    Name: My/Parameter/Name
    [WithDecryption: True/False]
```

Access the value by Ref-ing the resource.
All outputs from GetParameter are available as attributes.
