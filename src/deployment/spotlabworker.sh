#!/bin/bash -ex
# output user data logs into a separate place for debugging
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1

pip install pandas-datareader

mkdir /home/ec2-user/spotlabworker
cd /home/ec2-user/spotlabworker

wget https://s3.us-east-2.amazonaws.com/sjd-reinvent/2017/source/spotlabworker.zip
unzip ./spotlabworker.zip
rm ./spotlabworker.zip
python /home/ec2-user/spotlabworker/qp.py > stdout.txt 2>&1