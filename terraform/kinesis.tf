resource "aws_kinesis_stream" "Guardian_content" {
  name             = "Guardian_content"
  retention_period = 72

  stream_mode_details {
    stream_mode = "ON_DEMAND"
  }
}

data "aws_iam_policy_document" "kinesis_data_policy_doc" {
  statement {
    effect = "Allow"
    actions = [
      "kinesis:DescribeStreamSummary",
      "kinesis:ListShards",
      "kinesis:PutRecord",
      "kinesis:PutRecords"
    ]
    resources = [aws_kinesis_stream.Guardian_content.arn]
  }
}

resource "aws_iam_policy" "kinesis_policy" {
  name   = "kinesis_policy"
  policy = data.aws_iam_policy_document.kinesis_data_policy_doc.json
}

# resource "aws_iam_policy_attachment" "kinesis_policy" {
#   name       = "kinesis_policy"
#   roles      = "article-streaming-admin" # switch to lambda iam role 
#   policy_arn = aws_iam_policy.kinesis_policy.arn
# }

