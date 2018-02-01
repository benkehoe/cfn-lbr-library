```
MyS3Object:
  Type: Custom::S3Object
  Properties:
    Bucket: MyBucket
    Key: MyKey
    
    Text: <text>
    -OR-
    Binary: <base64>
    -OR-
    Json: <object, list, etc>
    
    [Other inputs to S3.PutObject]
```

Ref returns the ARN.
Bucket, Key are attributes.