resource "aws_kinesis_stream" "message_broker" {
  name             = "message-broker"
  retention_period = 72

  stream_mode_details {
    stream_mode = "ON_DEMAND"
  }

}
