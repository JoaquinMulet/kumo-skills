# PART I: SAM Template Reference

## Minimal Lambda Function

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Parameters:
  Environment:
    Type: String
    Default: dev
    AllowedValues: [dev, staging, prod]

Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub "my-function-${Environment}"
      PackageType: Image          # Use 'Zip' for non-Docker
      MemorySize: 2048            # MB
      Timeout: 300                # seconds
      Environment:
        Variables:
          ENVIRONMENT: !Ref Environment
    Metadata:
      Dockerfile: Dockerfile      # Relative to DockerContext
      DockerContext: ../           # Relative to template.yaml location
      DockerTag: latest
```

## S3 Bucket with Lifecycle

```yaml
  MyBucket:
    Type: AWS::S3::Bucket
    DeletionPolicy: Retain
    Properties:
      BucketName: !Sub "my-bucket-${Environment}-${AWS::AccountId}"
      VersioningConfiguration:
        Status: Enabled
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      LifecycleConfiguration:
        Rules:
          - Id: DeleteTempFiles
            Prefix: temp/
            Status: Enabled
            ExpirationInDays: 1
          - Id: DeleteOutputFiles
            Prefix: output/
            Status: Enabled
            ExpirationInDays: 15
```

## SQS Dead Letter Queue

```yaml
  MyDLQ:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: !Sub "my-dlq-${Environment}"
      MessageRetentionPeriod: 1209600  # 14 days

  MyFunction:
    Properties:
      DeadLetterQueue:
        Type: SQS
        TargetArn: !GetAtt MyDLQ.Arn
      Policies:
        - SQSSendMessagePolicy:
            QueueName: !GetAtt MyDLQ.QueueName
```

## CloudWatch Alarms

```yaml
  # Alert on Lambda errors
  ErrorAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub "my-function-errors-${Environment}"
      AlarmDescription: "Lambda error rate too high"
      Namespace: AWS/Lambda
      MetricName: Errors
      Dimensions:
        - Name: FunctionName
          Value: !Ref MyFunction
      Statistic: Sum
      Period: 300          # 5 min
      EvaluationPeriods: 2
      Threshold: 3
      ComparisonOperator: GreaterThanThreshold
      TreatMissingData: notBreaching

  # Alert on near-timeout
  DurationAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub "my-function-near-timeout-${Environment}"
      Namespace: AWS/Lambda
      MetricName: Duration
      Dimensions:
        - Name: FunctionName
          Value: !Ref MyFunction
      Statistic: Maximum
      Period: 300
      EvaluationPeriods: 1
      Threshold: 240000    # 240s (timeout is 300s) - in milliseconds
      ComparisonOperator: GreaterThanThreshold
      TreatMissingData: notBreaching

  # Alert on DLQ messages
  DLQAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub "my-dlq-messages-${Environment}"
      Namespace: AWS/SQS
      MetricName: ApproximateNumberOfMessagesVisible
      Dimensions:
        - Name: QueueName
          Value: !GetAtt MyDLQ.QueueName
      Statistic: Sum
      Period: 300
      EvaluationPeriods: 1
      Threshold: 0
      ComparisonOperator: GreaterThanThreshold
      TreatMissingData: notBreaching
```

## Lambda-to-Lambda Invocation

When one Lambda needs to invoke another asynchronously:

```yaml
  IngestFunction:
    Properties:
      Environment:
        Variables:
          PROCESS_FUNCTION: !Ref ProcessFunction  # SAM resolves to function name
      Policies:
        - Statement:
            - Effect: Allow
              Action: lambda:InvokeFunction
              Resource: !GetAtt ProcessFunction.Arn
```

```python
# In Python handler:
import boto3, json
lambda_client = boto3.client("lambda")

lambda_client.invoke(
    FunctionName=os.environ["PROCESS_FUNCTION"],
    InvocationType="Event",  # Async - returns 202 immediately
    Payload=json.dumps({"key": "value"}),
)
```

## Conditional Resources

```yaml
Conditions:
  CreateBucket: !Equals [!Ref BucketName, ""]
  IsProd: !Equals [!Ref Environment, "prod"]

Resources:
  MyBucket:
    Type: AWS::S3::Bucket
    Condition: CreateBucket  # Only create if no bucket name provided
```

## Separate Dockerfiles per Function

For functions with different dependency footprints, use separate Dockerfiles:

```dockerfile
# Dockerfile (heavy - for processing Lambda)
FROM public.ecr.aws/lambda/python:3.12
RUN dnf install -y poppler-utils    # PDF rendering
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY my_library/ ${LAMBDA_TASK_ROOT}/my_library/
COPY lambda_handlers/ ${LAMBDA_TASK_ROOT}/
CMD ["process.handler"]
```

```dockerfile
# Dockerfile.ingest (lightweight - only boto3)
FROM public.ecr.aws/lambda/python:3.12
COPY lambda_handlers/ingest.py ${LAMBDA_TASK_ROOT}/
CMD ["ingest.handler"]
```

Reference in template:
```yaml
  ProcessFunction:
    Metadata:
      Dockerfile: Dockerfile          # Heavy image
      DockerContext: ../

  IngestFunction:
    Metadata:
      Dockerfile: Dockerfile.ingest   # Lightweight image
      DockerContext: ../
```

---
