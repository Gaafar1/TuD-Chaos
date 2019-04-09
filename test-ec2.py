print("\n\nWelcome to TUD Chaos Monkey (tud_cm)")

import boto3
import random
import datetime
import time

#listing the instances in the asg group:
ec2 = boto3.resource('ec2')
instances = ec2.instances.filter(
    Filters=[{'Name': 'tag:Name', 'Values': ['Gaafar-ASG-G']},{'Name': 'instance-state-name', 'Values': ['running']}])
for instance in instances :
    startlist =[instance.id for instance in instances ]
print ("\nYou have the following number of instances running:\n")

print (*startlist,sep='\n')

print("\n#####################################################################\n")

#input number of instances to disturp


x = int(input("\nHow many do you want tud_cm to disrupt >> "))

ids = random.sample(startlist,x)

print("The following ",x," Instance IDs will be distruppted\n")
print(*ids,sep='\n')

# start timer 

startime  = datetime.datetime.now()

# terminate the randomley selected instances

ec2 = boto3.client('ec2')
ec2.terminate_instances(InstanceIds=ids)
print ("\nPlease wait while the selected intanceses are terminated...")

# wait until selected instances are  Terminated :

waiter=ec2.get_waiter('instance_terminated')
waiter.wait(InstanceIds=ids)
print( "\nThe following instances are now terminated:\n")
print(*ids,sep='\n')

#listing the running instances after selection terminted :

print ("\nYou have the following  instances running:\n")

ec2 = boto3.resource('ec2')
instances = ec2.instances.filter(
    Filters=[{'Name': 'tag:Name', 'Values': ['Gaafar-ASG-G']},{'Name': 'instance-state-name', 'Values': ['running']}])
for instance in instances:
    endlist = [instance.id for instance in instances]
print(*endlist,sep='\n')

# waiting for the reinstatment of new instances :
print ("\nNow timing reinstatement…\nPlease wait while these AWS HA reinstates the instances …")

while (len(startlist)) != (len(endlist)):
    time.sleep(30)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'tag:Name', 'Values': ['Gaafar-ASG-G']},{'Name': 'instance-state-name', 'Values': ['running']}])
    endlist = [instance.id for instance in instances]

#listing the latest available instances :

else:
    print("\nHere is the list of the instances running now\n")
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter(
    Filters=[{'Name': 'tag:Name', 'Values': ['Gaafar-ASG-G']},{'Name': 'instance-state-name', 'Values': ['running']}])
for instance in instances:
    print(instance.id)

# ending timer and calculating the time lapsed :
endtime = datetime.datetime.now()
timeelapsed = endtime - startime

# printing the result:

print ("\n====tud_cm Test Result====\n")
print(x,"instances stopped,",x," instances reinstated in",timeelapsed,"\n")


