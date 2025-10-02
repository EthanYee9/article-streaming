# Assume lambda policy document
data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}
# Creating Role for lambda
resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

# Create policy document for kinesis access
data "aws_iam_policy_document" "kinesis_data_policy_doc" {
  statement {
    effect = "Allow"
    actions = [
      "kinesis:DescribeStreamSummary",
      "kinesis:ListShards",
      "kinesis:PutRecord",
      "kinesis:PutRecords",
    ]
    resources = [aws_kinesis_stream.Guardian_content.arn]
  }
}

# Create Lambda kinesis write policy document
resource "aws_iam_policy" "kinesis_policy" {
  name   = "kinesis_policy"
  policy = data.aws_iam_policy_document.kinesis_data_policy_doc.json
}

# Attach kinesis write policy to lambda 
resource "aws_iam_role_policy_attachment" "lambda_kinesis_write_policy_attachment" {
  role       = aws_iam_role.iam_for_lambda.name
  policy_arn = aws_iam_policy.kinesis_policy.arn
}

# Create secret manager policy doc
data "aws_iam_policy_document" "secrete_manager_data_policy_doc" {
  statement {
    effect = "Allow"
    actions = [
      "secretsmanager:GetSecretValue"
    ]
    resources = [aws_secretsmanager_secret.guardian_api_key.arn]
  }
}

# Create secret manager policy 
resource "aws_iam_policy" "lambda_secret_policy" {
  name   = "lambda_secrets_policy"
  policy = data.aws_iam_policy_document.secrete_manager_data_policy_doc.json
}

# Attaching lambda with secret manager polict 
resource "aws_iam_role_policy_attachment" "attach_lambda_secret_policy" {
  role       = aws_iam_role.iam_for_lambda.name
  policy_arn = aws_iam_policy.lambda_secret_policy.arn
}
