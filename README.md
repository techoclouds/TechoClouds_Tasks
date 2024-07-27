
# AWS Lambda Unused EBS Volume Reporter

## Overview

This project involves creating an AWS Lambda function to identify unused (available) EBS volumes and publish a report to an SNS topic. The provided code contains initial errors that need to be fixed before completing the remaining logic.

## Prerequisites

1. AWS CLI installed and configured.
2. Terraform installed.
3. Basic knowledge of AWS, Terraform, Python, Lambda, SNS, and EBS.

## Instructions

### Step 1: Understand the Provided Code

- `main.tf`: Contains Terraform configuration for creating an SNS topic, IAM role, and Lambda function.
- `lambda_function.py`: Contains the Lambda function code to describe EBS volumes and publish a report to SNS.
- `providers.tf`: Provides Terraform configuration for the AWS provider.

### Step 2: Set Up Your Environment

- Ensure AWS CLI is configured with appropriate permissions.
- Install Terraform.

### Step 3: Review the Provided Code

- Look at `main.tf` to understand the Terraform resources.
- Look at `lambda_function.py` to understand the Lambda function's logic.

### Step 4: Identify and Fix Initial Errors

#### a. Fixing Terraform Configuration

- Ensure the Terraform files are properly formatted and variables are set correctly.

#### b. Fixing Lambda Function Errors

**Issue**: Lambda is missing SNS publish permission.
- **Solution**: Add the required SNS publish permissions to the IAM role.

Update `aws_iam_role` resource in `main.tf`:

```hcl
resource "aws_iam_role" "ebs-checker-lambda-role" {
  name               = "ebs-checker-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
  inline_policy {
    name = "ebs"

    policy = jsonencode(
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "ebsvolume",
          "Effect": "Allow",
          "Action": "ec2:DescribeVolumes",
          "Resource": "*"
        },
        {
          "Effect": "Allow",
          "Action": "logs:CreateLogGroup",
          "Resource": "arn:aws:logs:us-east-1:811452661392:*"
        },
        {
          "Effect": "Allow",
          "Action": [
            "logs:CreateLogStream",
            "logs:PutLogEvents"
          ],
          "Resource": [
            "arn:aws:logs:us-east-1:811452661392:log-group:/aws/lambda/test:*"
          ]
        },
        {
          "Effect": "Allow",
          "Action": "sns:Publish",
          "Resource": "*"
        }
      ]
    }
    )
  }
}
```

#### c. Fixing Lambda Execution Errors

**Issue**: Error in SNS publish due to invalid parameter.
- **Solution**: Fix the `MessageStructure` and `Message` parameters.

Update `lambda_function.py`:

```python
import boto3
import json
import os
snsarn = os.getenv('SNSTOPIC')

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    sns = boto3.client('sns')
    
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
    
    print(snsarn)
    
    volume_ids = [volume['VolumeId'] for volume in response['Volumes']]
    
    print(json.dumps(volume_ids, default=str))
    
    message = {
        "default": json.dumps(volume_ids)
    }
    
    response = sns.publish(
        TopicArn=snsarn,
        Message=json.dumps(message),
        Subject='EBS Report from us-east-1',
        MessageStructure='json'
    )
```

### Step 5: Deploy the Infrastructure

- Initialize Terraform:
```bash
terraform init
```
- Apply Terraform configuration:
```bash
terraform apply
```

### Step 6: Test the Lambda Function

- Trigger the Lambda function manually from the AWS Lambda console.
- Check CloudWatch logs for any errors and debug if necessary.

### Step 7: Complete the Logic

- Calculate the total number of available EBS volumes and publish this count along with their IDs to SNS.

Update `lambda_function.py`:

```python
import boto3
import json
import os
snsarn = os.getenv('SNSTOPIC')

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    sns = boto3.client('sns')
    
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
    
    volume_ids = [volume['VolumeId'] for volume in response['Volumes']]
    total_available_volumes = len(volume_ids)
    
    message = {
        "default": json.dumps({
            "total_available_volumes": total_available_volumes,
            "volume_ids": volume_ids
        })
    }
    
    response = sns.publish(
        TopicArn=snsarn,
        Message=json.dumps(message),
        Subject='EBS Report from us-east-1',
        MessageStructure='json'
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Report published successfully!')
    }
```

### Step 8: Validation

- Ensure the SNS topic receives the message with the correct details.
- Verify the message content in the SNS subscription (e.g., email or SQS).

### Step 9: Cleanup

- Once done, clean up the resources to avoid unnecessary charges:
```bash
terraform destroy
```

## Key Points

- Make sure IAM roles have the necessary permissions.
- Properly format messages to meet SNS requirements.
- Use CloudWatch logs to debug and verify function execution.
- Ensure Terraform configurations are accurate and complete before applying.

By following these steps, you'll fix the initial errors and complete the logic to identify and report unused EBS volumes via SNS.
