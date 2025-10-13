# Article Data Streaming

## Overview

This project is an application which retrieves articles from the Guardian API and publishs it to a message broker (AWS Kinesis) so that it can be consumed and analysed by other applications. The application accepts a search term (e.g. "machine learning"), an optional
"date_from" field, and a reference to a message broker. It will use the search terms to search for articles in the Guardian API and posts details of up to ten hits to the message broker.

## Tech Stack 
**Language:** Python, Terraform 

**Libraries:** Boto3

**Cloud Services:** AWS (Lambda, Kinesis, Secrets Manager)

**Testing:** Pytest


## Setup Instructions 

You will need Python 3, access to Guardain API key, an AWS account and an IAM user to deploy the terraform infrastructure.

*Get started by forking and cloning this repository.* 

### Next, create your virtual environment using:
```
python -m venv venv
```

*Activate your virtual environment using:*
```
source venv/bin/activate
```

*Export PYTHONPATH:*
```
export PYTHONPATH=$(pwd)
```

*Install dependencies  using:*
```
pip install -r requirements.txt
```

### Configure AWS Credentials
*Configure AWS Credentials with:*
```
 aws configure
 ```
 *Enter your `AWS Access Key ID`, `Secret Access Key` and `Region Name`.*

### Provision AWS Resources with Terraform
- Navigate to the `terraform` directory. In the terminal, run the following:
```
terraform init 
```
*Initialises the working directory, containing Terraform configuration files.*   
```
terraform plan 
```
*Creates a preview of the changes Terraform will make.*
```
terraform apply 
```
*Performs the changes shown in the plan, and asks for the Guardian API key.* 

### Invoking From Command Line

## Expected Outputs
After invoking the Lambda function, within your ``Guardian_content`` data stream in Kinesis, you should see records with a json containing:

- webPublicationDate
- webTitle
- webUrl
- content_preview: containg the first 1000 characters

Example:

```
{
    "webPublicationDate": "2025-08-10T16:39:47Z",
    "webTitle": "Learning to live with the torture of tinnitus | Letters",
    "webUrl": "https://www.theguardian.com/society/2025/aug/10/learning-to-live-with-the-torture-of-tinnitus",
    "content_preview": "One night, I heard a dripping tap. I asked my husband to check all the taps – upstairs bathroom, downstairs toilet, the kitchen. He assured me there were no dripping taps." 
}
```

## Removing Infrastructure 

To remove the infrastructure, run:
```
terraform destroy 
```
*Destroys the infrastructure.*
