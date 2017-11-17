# Hedge Your Own Funds: Run Monte Carlo Simulations on Amazon EC2 Spot Fleets: Lab Guide

* [Overview](#overview)
	* [Requirements](#req)
	* [Lab Overview](#labs)
	* [Conventions](#conventions)
	* [Workshop Cleanup](#clean)
* [Let's Begin!](#begin)
	* [Lab 1 - Set up the Workshop Environment on AWS](#lab1)
	* [Lab 2 - Explore the Algorithmic Trading Concepts with Jupyter ](#lab2)
	* [Lab 3 - Deploy an Automated Trading Strategy with EC2 Spot Fleet](#lab3)
	* [Lab	4 - Leverage a Fully Managed Solution using AWS Batch](#lab4)
* [Extra Credit](#extra)
* [Clean Up](#cleanup)

<a name="overview"></a>
## Overview:  
Algorithmic trading, or algo-trading is the process of using algorthims for placing a stock trade based on a set of perceived market conditions. These algorthims are based on price, quantity or other mathematical model without the risk of human emotion influencing the buy or sell action. This workshop will walk your through some of the basic tools and concepts that algorithmic traders employ to build fully automated trading systems. 

Monte Carlo Simulations involve repeated random sampling to model the probability of a complex problem that is difficult to predict using other methods due to the nature of the variables involved. We will use Monte Carlo Simulations to simulate and predict future stock movement by repeatedly sampling random stock values based on past results. 

The goal of this workshop is not to become financial gurus. I doubt we'll be rich at the end, but hopefully we'll have learned different ways to build batch processing pipelines using AWS services and save up to 90% using EC2 Spot Fleets. 

If you'd like to learn more: [Basics of Algorithmic Trading: Concepts and Examples](https://www.investopedia.com/articles/active-trading/101014/basics-algorithmic-trading-concepts-and-examples.asp)

<a name="req"></a>
### Requirements:  
* AWS account - if you don't have one, it's easy and free to [create one](https://aws.amazon.com/)
* AWS IAM account with elevated privileges allowing you to interact with CloudFormation, IAM, EC2, SQS, and CloudWatch Logs
* A workstation or laptop with an ssh client installed, such as [putty](http://www.putty.org/) on Windows or terminal or iterm on Mac
* Familiarity with Python, [Jupyter](http://jupyter.org/), AWS, and basic understanding of [algorthimic stock trading](http://www.investopedia.com/articles/active-trading/101014/basics-algorithmic-trading-concepts-and-examples.asp)  - not required but a bonus

<a name="Labs"></a>
### Lab Overview:  
These labs are designed to be completed in sequence.  If you are reading this at a live AWS event, the workshop attendants will give you a high level run down of the labs.  Then it's up to you to follow the instructions below to complete the labs.  Don't worry if you're embarking on this journey in the comfort of your office or home - presentation materials can be found in the git repo in the top-level [presentation](https://github.com/awslabs/spot-montecarlo-workshop/tree/master/presentation) folder.

**Lab 1:** Setup the workshop environment on AWS  
**Lab 2:** Explore the Algorithmic Trading Concepts with Jupyter  
**Lab 3:** Deploy an Automated Trading Strategy  

<a name="conventions"></a>
### Conventions:  
Throughout this README, we provide commands for you to run in the terminal.  These commands will look like this: 

<pre>
$ ssh -i <b><i>PRIVATE_KEY.PEM</i></b> ec2-user@<b><i>EC2_PUBLIC_DNS_NAME</i></b>
</pre>


The command starts after `$`.  Words that are ***UPPER_ITALIC_BOLD*** indicate a value that is unique to your environment.  For example, the ***PRIVATE\_KEY.PEM*** refers to the private key of an SSH key pair that you've created, and the ***EC2\_PUBLIC\_DNS\_NAME*** is a value that is specific to an EC2 instance launched in your account.  

<a name="clean"></a>
### Workshop Cleanup:
This section will appear again below as a reminder because you will be deploying infrastructure on AWS which will have an associated cost.  Fortunately, this workshop should take no more than 2 hours to complete, so costs will be minimal.  See the appendix for an estimate of what this workshop should cost to run.  When you're done with the workshop, follow these steps to make sure everything is cleaned up.

1. Delete any manually created resources throughout the labs.  
2. Delete any data files stored on S3.  
3. Delete the CloudFormation stack launched at the beginning of the workshop.

<a name="begin"></a>
## Let's Begin!  
<a name="lab1"></a>
### Lab 1 - Set up the Workshop Environment on AWS: 

#### Create an SSH Key   

1.  First, you'll need to select a [region](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html). For this lab, you will need to choose a region where the AWS-provided Deep Learning AMI is available. (See Step 3 for a full list.) At the top right hand corner of the AWS Console, you'll see a **Support** dropdown. To the left of that is the region selection dropdown.

2. Then you'll need to create an SSH key pair which will be used to login to the instances once provisioned.  Go to the EC2 Dashboard and click on **Key Pairs** in the left menu under Network & Security.  Click **Create Key Pair**, provide a name (can be anything, make it something memorable) when prompted, and click **Create**.  Once created, the private key in the form of .pem file will be automatically downloaded.  

3. If you're using linux or mac, change the permissions of the .pem file to be less open.  

	$ chmod 400 <b><i>PRIVATE_KEY.PEM</i></b>

	>If you're on windows you'll need to convert the .pem file to .ppk to work with putty.  Here is a link to instructions for the file conversion - [Connecting to Your Linux Instance from Windows Using PuTTY](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html)

#### Launch the Workshop template
For your convenience, we provide a CloudFormation template to stand up the core infrastructure.  

The template sets up a VPC, IAM roles, S3 bucket, and an EC2 Instance. The EC2 instance will run a Jupyter Notebook which we will leverage in Lab 2 and a small website that we will use in Lab 3. The idea is to provide a contained environment, so as not to interfere with any other provisioned resources in your account.  In order to demonstrate cost optimization strategies, the EC2 Instance is an [EC2 Spot Instance](https://aws.amazon.com/ec2/spot/) deployed by [Spot Fleet](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-fleet.html).  If you are new to [CloudFormation](https://aws.amazon.com/cloudformation/), take the opportunity to review the [template](https://github.com/awslabs/spot-motecarlo-workshop/blob/master/lab-1-setup/cfn-templates/spot-montecarlo-workshop.yaml) during stack creation.


*Prior to launching a stack, be aware that a few of the resources launched need to be manually deleted when the workshop is over. When finished working, please review the "Workshop Cleanup" section to learn what manual teardown is required by you.*

1. Click on one of these CloudFormation templates that matches the region you created your keypair in to launch your stack:  

	Region | Launch Template
	------------ | -------------  
	**N. Virginia** (us-east-1) | [![Launch Monte Carlo Workshop into Ohio with CloudFormation](images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=spot-montecarlo-stack&templateURL=https://s3-us-west-2.amazonaws.com/reinvent2017-cmp316/monte-carlo-workshop.yaml) 
	**Ohio** (us-east-2) | [![Launch Monte Carlo Workshop into Ohio with CloudFormation](images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/new?stackName=spot-montecarlo-stack&templateURL=https://s3-us-west-2.amazonaws.com/reinvent2017-cmp316/monte-carlo-workshop.yaml)  
	**Oregon** (us-west-2) | [![Launch Monte Carlo Workshop into Oregon with CloudFormation](images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=spot-montecarlo-stack&templateURL=https://s3-us-west-2.amazonaws.com/reinvent2017-cmp316/monte-carlo-workshop.yaml)
	**Ireland** (eu-west-1) | [![Launch Monte Carlo Workshop into Ireland with CloudFormation](images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=spot-montecarlo-stack&templateURL=https://s3-us-west-2.amazonaws.com/reinvent2017-cmp316/monte-carlo-workshop.yaml)
	**Tokyo** (ap-northeast-1) | [![Launch Monte Carlo Workshop into Tokyo with CloudFormation](images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new?stackName=spot-montecarlo-stack&templateURL=https://s3-us-west-2.amazonaws.com/reinvent2017-cmp316/monte-carlo-workshop.yaml) 
	**Seoul** (ap-northeast-2) | [![Launch Monte Carlo Workshop into Seoul with CloudFormation](images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-2#/stacks/new?stackName=spot-montecarlo-stack&templateURL=https://s3-us-west-2.amazonaws.com/reinvent2017-cmp316/monte-carlo-workshop.yaml)
	**Sydney** (ap-southeast-2) | [![Launch Monte Carlo Workshop into Sydney with CloudFormation](images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=spot-montecarlo-stack&templateURL=https://s3-us-west-2.amazonaws.com/reinvent2017-cmp316/monte-carlo-workshop.yaml)

2. The template will automatically bring you to the CloudFormation Dashboard and start the stack creation process in the specified region. Click **Next** on the page it brings you to. Do not change anything on the first screen.

	![CloudFormation PARAMETERS](images/cf-initial.png)
**IMPORTANT**  
	*On the parameter selection page of launching your CloudFormation stack, make sure to choose the key pair that you created in step 1. If you don't see a key pair to select, check your region and try again.*
![CloudFormation PARAMETERS](images/cf-params.png)
  
3. Select a password to use for the Jupyter Notebook. You will use this password in Lab 2. After you've selected your ssh key pair, click **Next**. 
4. On the **Options** page, accept all defaults - you don't need to make any changes. Click **Next**. 
5. On the **Review** page, under **Capabilities** check the box next to **"I acknowledge that AWS CloudFormation might create IAM resources."** and click **Create**. Your CloudFormation stack is now being created.
6. Periodically check on the stack creation process in the CloudFormation Dashboard.  Your stack should show status **CREATE\_COMPLETE** in roughly 10-15 minutes. In the Outputs tab, take note of the **Jupyter** and **Web Server** values; you will need these in the next two labs. 
	
	![CloudFormation Complete](/images/cf-complete.png)
	
7. Click on the Output URLs for **Jupyter** and **Web Server**. Each should load a web page confirming that the environment has been deployed correctly.    

	Jupyter
	![CloudFormation Jupyter Complete](/images/jupyter.png)
	
	Web
	![CloudFormation Web Client Complete](/images/web.png)

If there was an error during the stack creation process, CloudFormation will rollback and terminate.  You can investigate and troubleshoot by looking in the Events tab.  Any errors encountered during stack creation will appear in the event log. 
    

<a name="lab2"></a>
### Lab 2 - Explore the Algorithmic Trading Concepts with Jupyter:

The [Jupyter Notebook](http://jupyter.org/) allows you to create and share documents that contain live code, equations, visualizations and narrative text.

1. Log into the Jupyter Notebook using the **Jupyter** URL output from the CloudFormation Template using the password you configured when building the stack.
2. Click on the notebook named *monte-carlo-workshop.ipynb* and it should open in a new tab.
3. Follow the instructions in the Notebook to complete Lab 2. If you're new to Jupyter, you press shift-enter to run code and/or proceed to the next section. When you're done with the Notebook, return here and we'll take the concepts we learned in this lab and build our own automated pipeline.


<a name="lab3"></a>
### Lab 3 - Deploy an Automated Trading Strategy on EC2 Spot Fleet:

#### Create the SQS Queue
1. quick create an sqs standard queue
2. record the SQS Name and URL for later
3. Edit IAM Instance Policy on the EC2 instance. Add sqs:* 
#### Configure the Web Client
4. Launch Web Site
5. click configuration
6. Paste in the SQS URL
7. Paste S3 resultsBucket name from CFN Output
8. Paste AWS Region from CFN Output - V2 maybe we populate this automagically
9. Click Save

#### Configure our Simulation 
10. click home on web page
11. Enter you simulation details. You can select whatever values you'd like, but too large of an iteration count, may take a long time to complete. We recommend the following configuration.
	12. Stock Symbol (e.g. AMZN)
	13. Short Window = 10 days
	14. Long Window = 30 days
	15. Trading Days  = 252 (one year)
	16. Iterations 1000
	17. Click Submit (You can also preview the json if you want to see the message body
18. You can view the json message in the SQS Queue.

#### Create the Spot Worker Fleet
1. From the Management Console, Click **Services**, and select EC2.
2. Select Spot Requests and click **Request Spot Instances**.
3. Select **Request and Maintain** to create a fleet of Spot Instances.
4. For **Target Capacity**, type **2**
5. Leave the Amazon Linux AMI as the Default.
6. Each EC2 Instance type and family has it's own independent Spot Market price. Under **Instance Types**, Click **Select** and pick the c3.xlarge, c3.2xlarge, and c4.xlarge to diversify our fleet. Click **Select** again to return to the previous screen.
7.  For **Allocation Strategy**, pick **Diversified**.
8. For **Network**, pick the VPC we created for the Spot Monte Carlo Workshop.
9. Under Availability Zone, check the box next to the first two AZs. The Network Subnet should auto-populate. If the subnet dropdown box says "No subnets in this zone", uncheck and select another AZ
10.  Select **Use automated bidding**
11. Click **Next**
12. We will use User Data to bootstrap our work nodes. Cut and paste the user data [script](https://github.com/aws-samples/ec2-spot-montecarlo-workshop/blob/master/templates/spotlabworker.sh) from the git hub repo.  You will need to replace **\<REPLACE WITH YOUR SQS QUEUE NAME>** with the name of the queue you created earlier. **TODO** Improve this workflow.
12. Under **IAM instance profile**, pull the dropdown and select the profile beginning with the workshop name you configured in the CloudFormation Template.
13. Select the Security Group named after your Workshop.
14. Under Tags, Add a Tag for Name, the value should be a name to identify (e.g. Worker Node)
15. We will accept the rest of the defaults, but take a moment at look at the options that you can configure for your Spot Fleet
	* Health Checks
	* Interruption behavior
	* Load Balancer registration
	* EBS Optimized
16. Click **Next** and review your settings. Click request fleet
17. Wait until the request is fulfilled, capacity shows 2 of 2, and the status is Active.
18. Once the workers come up, they should start processing the SQS messages automatically. Send some more stocks from the webpage.

#### Evaluate the Results
1. Check the S3 Bucket that was created by the CloudFormation template. In a few minutes you should see results start appearing the bucket. You'll see the following results files:
	* File Description 1
	* File Description 2 
	* File Description N
2. If you monitor the SQS queue for messages you should see them being picked up by the worker nodes. 
You've completed Lab 3, Congrats!

#### Extra Credit
* Use [AWS QuickSight](https://https://quicksight.aws/) to build visualizations, perform ad-hoc analysis, and quickly get business insights from your data
* Each job is handled fully by one worker. Maybe you could look at adding more parallelism to task scheduler.
* Configure Auto Scaling for your Spot Fleet based on SQS Queue Depth


<a name="lab4"></a>
### Lab	4 - Leverage a Fully Managed Solution using AWS Batch 

Coming Soon!





<a name="cleanup"></a>
## Clean Up

