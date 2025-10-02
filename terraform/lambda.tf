data "archive_file" "lambda_streaming_layer" {
  type        = "zip"
  source_file = "${path.module}/../src/layer/"
  output_path = "${path.module}/../src/layer.zip"
}

resource "aws_lambda_layer_version" "extract_dependencies_layer" {
  layer_name          = "extract_dependencies_layer"
  compatible_runtimes = ["python3.13"]
  filename            = data.archive_file.lambda_streaming_layer.output_path
}

data "archive_file" "lambda_stream_script" {
  type        = "zip"
  source_file = "${path.module}/../src/streaming_script.py"
  output_path = "${path.root}/deployments/streaming_script.zip"
}

resource "aws_lambda_function" "streaming_lambda" {
  filename      = data.archive_file.streaming_script.output_path
  function_name = "Streaming lambda"
  role          = aws_iam_role.iam_for_lambda.arn
  runtime       = "python3.13"
  layers        = [aws_lambda_layer_version.extract_dependencies_layer.arn]
}
