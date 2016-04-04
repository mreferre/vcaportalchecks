
## Check the status of a(n authenticated) web service using a basic AWS Lambda function. 

## Massimo Re Ferre' [www.it20.info](http://www.it20.info)

This simple Python function (wrapped in an AWS Lambda function) checks the availability of the vCloud Air login service and save the result of the query in a DynamoDB table. 

The idea behind this code was to ~~create a historical set of data with returned status codes to determine the availability of a web service (vCloud Air login in this case)~~ play around with Lambda.     

## Requirements

To be able to consume this code as-is you'd need:

- an AWS account
- a vCloud Air account
- the AWS CLI 

# Disclosure 

This is just a personal POC to play around with Lambda. There are a lot of "bad practices" that went into it (i.e. embedding user names and passwords into the code). Note [I did mind to investigate how to make it look better](http://stackoverflow.com/questions/36225031/how-to-properly-use-external-credentials-in-an-aws-lambda-function/) BUT I did not bother to implement the best practices suggested. Perhaps something to keep in mind for the next phase of these experiments. 

Similarly the way the DynamoDB table has been designed may be far from optimal (e.g. probably you want the HASH values to be as diverse as possible to optimize the back-end partitioning of the data, in my case the HASH is the status of the service - most likely and hopefully that will always be `201` for this particular code and web service being tested)

## Setup

These are the (high level instructions to make it work):

* clone this repository and position yourself at the root of it
* configure the AWS CLI to point to the region you want to work with
* run the `./vcaportalchecks-createtable.sh` script (which calls the AWS CLI) to create the DynamoDB table required to host the data
* Create an AWS user and grant it r/w access to the table created above  
* move into the `/lambdafunction` directory
* tweak the `./vcaportalchecks.py` with the proper vCloud Air credentials (to test the login) and AWS credentials (to insert the result of the query into DynamoDB)   
* per the [instructions here](http://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html
) download a couple of additional library that are needed for the Python function to work
	* `(sudo) pip install boto  -t .`
	* `(sudo) pip install httplib2  -t .`
* zip everything in this folder into a `.zip` file
* createa a lamda function uploading the `.zip` file created above
	* Runtime: `Python 2.7`
	* Handler: `vcaportalchecks.VcaPortalCheck` <- this must be in the [filename.function] format
	* Role: `Lambda base execution`
	* Timeout: `10 seconds` <- default is 3 seconds 

[BTW: One reads the 15 or so bullets above and immediately understands the value of "infrastructure as code"] 

You should now be able to test the lambda function. 

While Lambda (IMO anyway) shines when used in conjuction with event-driven approaches (e.g. when "x" happens, trigger lambda function "y"), you could schedule this Python function to run every, say, 15 minutes and check the status of a web service while storing the results of each query for historical analysis.   

## License:

Apache Licensing version 2
