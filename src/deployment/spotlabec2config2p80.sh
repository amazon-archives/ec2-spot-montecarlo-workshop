#!/bin/bash -ex
# output user data logs into a separate place for debugging
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
# get node into yum
curl --silent --location https://rpm.nodesource.com/setup_6.x | bash -
# install node (and npm) with yum
yum -y install nodejs


mkdir /home/ec2-user/spotlab
cd /home/ec2-user/spotlab

wget https://s3.us-east-2.amazonaws.com/sjd-reinvent/2017/source/spotlab80.zip
unzip ./spotlab80.zip
rm ./spotlab80.zip
node /home/ec2-user/spotlab/bin/www > stdout.txt 2>&1