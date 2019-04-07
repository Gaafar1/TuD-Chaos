print("\n\nWelcome to TUD Chaos Monkey (tud_cm)")

import boto3


def as_get_instances(client, asgroup, NextToken = None):
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

instances =  list(as_get_instances(client,'content_server'))

print ("\nYou have 6 instances running:\n") 

print (*instances, sep='\n')

print("\n#####################################################################\n")

#input number of instances to disturp 

import random

list  = list(as_get_instances(client,'content_server'))

x = int(input("\nHow many do you want tud_cm to disrupt >> "))

ids = random.sample(list,x)

print("The following ",x," Instance IDs will be distruppted\n")
print(*ids,sep='\n')

import datetime
startime  = datetime.datetime.now()
# terminate the randomley selected instances

import boto3
ec2 = boto3.client('ec2')
ec2.terminate_instances(InstanceIds=ids)
print ("\nPlease wait while the selected intanceses are terminated...")

# wait until Terminated :

waiter=ec2.get_waiter('instance_terminated')
waiter.wait(InstanceIds=ids)
print( "\nThe following instances are now terminated:\n")
print(*ids,sep='\n')

print ("\nYou have the following  instances running:\n")

import boto3 
ec2 = boto3.resource('ec2')

instances = ec2.instances.filter(
    Filters=[{'Name': 'tag:Name', 'Values': ['Gaafar-ASG-G']},{'Name': 'instance-state-name', 'Values': ['running']}])
for instance in instances:
    print(instance.id)

print ("\nNow timing reinstatement…\nPlease wait while these AWS HA reinstates the instances …")
import time 
time.sleep(240)

print("\nYou have the following  instances running:\n")

ec2 = boto3.resource('ec2')

instances = ec2.instances.filter(
    Filters=[{'Name': 'tag:Name', 'Values': ['Gaafar-ASG-G']},{'Name': 'instance-state-name', 'Values': ['running']}])
for instance in instances:
    print(instance.id)

endtime = datetime.datetime.now()

timeelapsed = endtime - startime
print ("====tud_cm Test Result====\n")
print("\n",x,"instances stopped,",x," instances reinstated in",timeelapsed) 
 
