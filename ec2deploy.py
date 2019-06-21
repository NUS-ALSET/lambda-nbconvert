#!/usr/bin/env python3
import boto3
import argparse
import time

parser = argparse.ArgumentParser(description='')
parser.add_argument('bucket_name')
parser.add_argument('stack_name')
parser.add_argument('region')
parser.add_argument('enable_cors')
args = parser.parse_args()

# comment occurences of AWS_SESSION_TOKEN and session_token
# if you are not using an AWS Educate Account

session = boto3.Session()
access_key = session.get_credentials().access_key
secret_key = session.get_credentials().secret_key
session_token = session.get_credentials().token
ec2 = session.resource('ec2')

start_up_script = """#!/usr/bin/env bash
export AWS_ACCESS_KEY_ID='{access_key}'
export AWS_SECRET_ACCESS_KEY='{secret_key}'
export AWS_SESSION_TOKEN='{session_token}'
trap 'shutdown now' EXIT
set -x -e
apt update
apt install -y awscli docker.io zip
cd /home/ubuntu
git clone https://github.com/NUS-ALSET/lambda-nbconvert.git
cd lambda-nbconvert
./scripts/deploy.sh '{bucket_name}' '{stack_name}' '{region}' '{enable_cors}'
cat<<'END'
--------------------------------------------------------------------------------
Stack {stack_name} was successfully deployed
--------------------------------------------------------------------------------
END
sleep 10
""".format(access_key=access_key,
           secret_key=secret_key,
           session_token=session_token,
           bucket_name=args.bucket_name,
           stack_name=args.stack_name,
           region=args.region,
           enable_cors=args.enable_cors)

i = ec2.create_instances(ImageId='ami-0ac019f4fcb7cb7e6',
                         InstanceType='t2.micro',
                         UserData=start_up_script,
                         MinCount=1,
                         MaxCount=1,
                         InstanceInitiatedShutdownBehavior='terminate')[0]

print('Instance {} was started. Waiting for output ...'.format(i.instance_id))

prev_output = ''
while True:
    time.sleep(10)
    o = i.console_output()
    if 'Output' in o:
        output = o['Output']
        if output != prev_output:
            print('...\n'*3)
            print(output)
            prev_output = output
    if i.state['Name'] == 'terminated':
        break

success_string = 'Stack {} was successfully deployed'.format(args.stack_name)

print(('#'*60+'\n')*3)
if success_string in prev_output:
    print(success_string)
else:
    print('There were some problems. See above output for more details')
