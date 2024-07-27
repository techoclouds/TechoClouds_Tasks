import boto3
import json
import os
snsarn=os.getenv('SNSTOPIC')

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
  
  for volume in response['Volumes']:
  
      print(json.dumps(volume['VolumeId'], default=str))
      
  response = sns.publish(
  TopicArn=snsarn,
  Message='HEllo FRom Lambda',
  Subject='ebs report from us-east-1',
  MessageStructure='json'
  )
  
  

