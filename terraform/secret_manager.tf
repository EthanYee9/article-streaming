variable "guardian_api_key" {
  description = "Guardian API key"
  type        = string
  sensitive   = true
}

resource "aws_secretsmanager_secret" "guardian_api_key" {
  name                    = "Guardian_content"
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "creds" {
  secret_id = aws_secretsmanager_secret.guardian_api_key.id
  secret_string = jsonencode({
    api_key = var.guardian_api_key
  })
}
