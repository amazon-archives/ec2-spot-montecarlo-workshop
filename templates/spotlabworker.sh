#!/bin/bash -ex
# output user data logs into a separate place for debugging
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
yum -y install git python-numpy python-matplotlib python-zmq python-scipy
pip install pandas-datareader scipy

REGION=`curl http://169.254.169.254/latest/dynamic/instance-identity/document|grep region|awk -F\" '{print $4}'`

mkdir /home/ec2-user/spotlabworker
chown ec2-user:ec2-user /home/ec2-user/spotlabworker
cd /home/ec2-user/spotlabworker
aws configure set default.region $REGION
wget https://s3-us-west-2.amazonaws.com/reinvent2017-cmp316/queue_processor.py
wget https://s3-us-west-2.amazonaws.com/reinvent2017-cmp316/worker.py
echo "QUEUE = '<REPLACE WITH YOUR SQS QUEUE NAME>'" > config.py

python /home/ec2-user/spotlabworker/queue_processor.py > stdout.txt 2>&1