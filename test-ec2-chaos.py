import boto3


def as_get_instances(client, asgroup, NextToken = None):
    # this is downright ridiculous because boto3 sucks
    irsp = None
    if NextToken:
        irsp = client.describe_auto_scaling_instances(MaxRecords=2, NextToken=NextToken)
    else:
        irsp = client.describe_auto_scaling_instances(MaxRecords=2)

    for i in irsp['AutoScalingInstances']:
        if i['AutoScalingGroupName'] == 'Gaafar-ASG':
            yield i['InstanceId']

    if 'NextToken' in irsp:
        for i in as_get_instances(client, asgroup, NextToken = irsp['NextToken']):
            yield i


if __name__ == '__main__':

    client = boto3.client('autoscaling', region_name='eu-west-1')

#list of instances:

print("\nThis ASG gruop has these 4  running instances :","\n\n",list(as_get_instances(client,'content_server')))

print("\n#####################################################################\n")

#output the random instances choices

print("\nThe following instancese will be distruppted :")

import random

list  = list(as_get_instances(client, 'content_server'))

ids = random.sample(list,2)

print("\n",ids,"\n")

#print(random.sample(list,2))

# terminate the randomley selected instances

ec2 = boto3.resource('ec2')

ec2.instances.filter(InstanceIds=ids).terminate()

import re

client = boto3.client('ec2')
rsp = client.describe_instances(InstanceIds=ids)
if rsp:
  status = rsp['Reservations'][0]['Instances'][0]
  if status['State']['Name'] == 'terminated':
    stopped_reason = status['StateTransitionReason']
    current_time = rsp['ResponseMetadata']['HTTPHeaders']['date']
    stopped_time = re.findall('.*\((.*)\)', stopped_reason)[0]
    print ('Stopped time:', stopped_time)
    print ('Current time:', current_time)

# start sleep time
import time

time.sleep(300)

#checking treminated intstances

print("\n the following instances are in terminated state:\n")


ec2 = boto3.resource('ec2')

instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['terminated']}])
for instance in instances:
    print(instance.id)

#checking what instances are running again

print("\n#######################################################################\n")

print("\nThis ASG gruop now has these 4  running instances :",list)


