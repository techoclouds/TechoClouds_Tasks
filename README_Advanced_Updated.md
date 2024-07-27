
# Advanced AWS EBS Volume Report Assignment

## Overview

In this assignment, you will enhance your AWS, Terraform, and Python skills by implementing best practices such as adding tags, defining variables, and scheduling a Lambda function to run daily using CloudWatch Events. This guide will provide you with example snippets and instructions to complete the assignment.

## Prerequisites

- AWS account with appropriate permissions
- Basic knowledge of Terraform, AWS Lambda, SNS, and CloudWatch Events
- Python programming skills
- AWS CLI installed and configured
- Terraform installed

## Step-by-Step Guide

### Step 1: Review Provided Snippets

Review the provided snippets and understand what needs to be added or modified in your codebase.

### Step 2: Define Variables

Define variables in your Terraform configuration to improve flexibility and reusability. 

#### Example Variable Definitions

```hcl
variable "region" {
  description = "AWS region"
  default     = "us-east-1"
}

variable "lambda_function_name" {
  description = "Name of the Lambda function"
  default     = "ebs-checker"
}

variable "sns_topic_name" {
  description = "Name of the SNS topic"
  default     = "ebs-sns"
}
```

### Step 3: Add Tags to Resources

Add tags to your AWS resources for better management and organization.

#### Example Tag Definitions

```hcl
resource "aws_lambda_function" "ebs_checker" {
  ...
  tags = {
    Environment = "dev"
    Project     = "EBS Checker"
  }
}

resource "aws_sns_topic" "ebs_sns" {
  ...
  tags = {
    Environment = "dev"
    Project     = "EBS Checker"
  }
}
```

### Step 4: Schedule Lambda Function

Create a CloudWatch Event to trigger your Lambda function daily.

#### Example CloudWatch Event Definition

```hcl
resource "aws_cloudwatch_event_rule" "schedule_rule" {
  name                = "daily-ebs-check"
  description         = "Trigger Lambda function daily to check for unused EBS volumes"
  schedule_expression = "rate(1 day)"
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.schedule_rule.name
  target_id = "lambda"
  arn       = aws_lambda_function.ebs_checker.arn
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ebs_checker.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.schedule_rule.arn
}
```

### Step 5: Add Logging to Lambda Function

Enhance your Lambda function to include logging for better observability.

#### Example Logging

```python
import boto3
import json
import os
import logging

snsarn = os.getenv('SNSTOPIC')

logging.basicConfig(level=logging.INFO)

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    sns = boto3.client('sns')
    
    logging.info("Fetching available EBS volumes")
    response = ec2.describe_volumes(
        Filters=[
            {
                'Name': 'status',
                'Values': [
                    'available',
                ]
            },
        ]
    )
    
    volumes = [volume['VolumeId'] for volume in response['Volumes']]
    volume_count = len(volumes)
    
    logging.info(f"Found {volume_count} available EBS volumes")
    
    message = {
        'volume_count': volume_count,
        'volumes': volumes
    }
    
    sns.publish(
        TopicArn=snsarn,
        Message=json.dumps(message),
        Subject='EBS Report from us-east-1'
    )

    logging.info("EBS volume report sent to SNS")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Report sent to SNS')
    }
```

### Step 6: Enhance Lambda Logic

Further enhance your Lambda function to include additional data collection or processing logic.

#### Example Enhanced Logic

```python
import boto3
import json
import os
import logging

snsarn = os.getenv('SNSTOPIC')

logging.basicConfig(level=logging.INFO)

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    sns = boto3.client('sns')
    
    logging.info("Fetching available EBS volumes")
    response = ec2.describe_volumes(
        Filters=[
            {
                'Name': 'status',
                'Values': [
                    'available',
                ]
            },
        ]
    )
    
    volumes = [volume['VolumeId'] for volume in response['Volumes']]
    volume_count = len(volumes)
    
    logging.info(f"Found {volume_count} available EBS volumes")
    
    message = {
        'volume_count': volume_count,
        'volumes': volumes
    }
    
    sns.publish(
        TopicArn=snsarn,
        Message=json.dumps(message),
        Subject='EBS Report from us-east-1'
    )

    logging.info("EBS volume report sent to SNS")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Report sent to SNS')
    }
```

## Validation

1. Deploy your Terraform configuration.
2. Check that the Lambda function is created and tagged appropriately.
3. Verify that the CloudWatch Event rule is set to trigger the Lambda function daily.
4. Monitor the SNS topic for messages containing the EBS volume report.

## Cleanup

To avoid incurring unnecessary charges, clean up the resources after validation.

```sh
terraform destroy
```

## Key Points

- Define variables to enhance flexibility.
- Add tags for better resource management.
- Schedule Lambda functions using CloudWatch Events for automated tasks.
- Enhance Lambda logic for comprehensive data collection and reporting.

By following these best practices and completing this assignment, you'll gain valuable experience in managing AWS resources efficiently and automating tasks using Terraform and AWS services.
