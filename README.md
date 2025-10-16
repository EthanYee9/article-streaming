# Article Data Streaming

## Overview

This project is an AWS Lambda application which retrieves articles from the Guardian API and publishs it to a message broker (AWS Kinesis) so that it can be consumed and analysed by other applications. 

The application accepts a search term (e.g. "machine learning"), an optional "date_from" field, and a reference to a message broker. It will use the search terms to search for articles in the Guardian API and posts details of up to ten hits to the message broker.

Sensitive information such as the Guardian API key is securely managed using AWS Secrets Manager. This ensures that no credentials are hardcoded or stored in plain text, following best practices for cloud security.

All AWS resources including the Lambda function, IAM roles, and Kinesis stream are provisioned using Terraform.

This repository uses GitHub Actions to automatically test and validate all code changes before they are merged into the main branch.

## Tech Stack 
**Language:** Python, Terraform 

**Libraries:** Boto3, lxml

**Cloud Services:** AWS (Lambda, Kinesis, Secrets Manager)

**CI/CD**: GitHub Actions 

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

## Invoking From Command Line
To invoke the lambda function from command line:

```
aws lambda invoke \
  --function-name Streaming_lambda \
  --cli-binary-format raw-in-base64-out \
  --payload '{"search term": "<placeholder>", "message_broker_id": "Guardian_content", "from_date": "yyyy/mm/dd"}' \
  response.json
```

## Expected Outputs
After invoking the Lambda function, within your ``Guardian_content`` data stream in Kinesis, you should see records with a json containing:

- webPublicationDate
- webTitle
- webUrl
- content_preview: containg the first ~1000 characters

Example:

```
{
    "webPublicationDate": "2025-06-25T09:11:34Z",
    "webTitle": "UK graduates facing worst job market since 2018 amid rise of AI, says Indeed",
    "webUrl": "https://www.theguardian.com/money/2025/jun/25/uk-university-graduates-toughest-job-market-rise-of-ai",
    "content_preview": "University graduates in the UK are facing the toughest job market since 2018, figures suggest, as employers pause hiring and use AI to cut costs, according to analysts. The number of roles advertised for recent graduates is down 33% compared with last year and is at the lowest level in seven years, according to the job search site Indeed. Overall job postings as of mid-June were 5% lower compared with the end of March, as the broader job market struggles in the face of higher taxes for employers and minimum wage changes introduced from April. It means the UK is an outlier compared with the US and its peers in Europe, as it is the only economy with fewer job openings available than before the "
}
```

## Removing Infrastructure 

To remove the infrastructure, run:
```
terraform destroy 
```
*Destroys the infrastructure.*
