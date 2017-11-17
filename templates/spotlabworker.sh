#!/bin/bash
yum -y install git python-numpy python-matplotlib python-zmq python-scipy
pip install pandas-datareader
pip install scipy 
pip install boto3

REGION=`curl http://169.254.169.254/latest/dynamic/instance-identity/document|grep region|awk -F\" '{print $4}'`

mkdir /home/ec2-user/spotlabworker
chown ec2-user:ec2-user /home/ec2-user/spotlabworker
cd /home/ec2-user/spotlabworker

wget https://s3-us-west-2.amazonaws.com/reinvent2017-cmp316/queue_processor.py
wget https://s3-us-west-2.amazonaws.com/reinvent2017-cmp316/worker.py
echo "QUEUE = '<REPLACE WITH YOUR SQS QUEUE NAME>'" > config.py
echo "REGION = '$REGION'" >> config.py
aws configure set default.region $REGION
python /home/ec2-user/spotlabworker/queue_processor.py > stdout.txt 2>&1