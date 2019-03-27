
#Aws autoscaling create-auto-scaling-group --auto-scaling-group-name Gaafar-ASG --instance-id i-06b9c2d435cf3075e --min-size 1 --max-size 4 --desired-capacity 4
#aws autoscaling describe-auto-scaling-groups --auto-scaling-group-name Gaafar-ASG


import boto3


def as_get_instances(client, asgroup, NextToken = None):
    # this is downright ridiculous because boto3 sucks
    irsp = None
    if NextToken:
        irsp = client.describe_auto_scaling_instances(MaxRecords=2, NextToken=NextToken)
    else:
        irsp = client.describe_auto_scaling_instances(MaxRecords=2)

    for i in irsp['AutoScalingInstances']:
        if i['AutoScalingGroupName'] == 'Gafar-ASG':
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


# terminate the randomley selected instances

ec2 = boto3.resource('ec2')

ec2.instances.filter(InstanceIds=ids).terminate()

#Sleep time  

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

print("\nThis ASG gruop now has these 4  running instances :\n\n",list)
