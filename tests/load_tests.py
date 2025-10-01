import pytest 
from unittest.mock import patch, MagicMock
from src.streaming_script import publish_to_kinesis

@pytest.fixture
def mock_kinesis_client():
    with patch("src.streaming_script.boto3.client") as mock_client:
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
    
    yield mock_instance

class TestPublishToKinesis:
    def test_0_failed_records(self, mock_kinesis_client):
        fake_records = [
            {"Data": '{"webTitle": "Test"}', "PartitionKey": "guardian_content"}
        ]
        fake_response = {
            "FailedRecordCount": 0,
            "Records": [{"SequenceNumber": "12345", "ShardId": "shardId-000000000000"}]
        }
        
        mock_kinesis_client.put_records.return_value = fake_response
        
        result = publish_to_kinesis(fake_records, "Guardian_content")
        assert result["FailedRecordCount"] == 0
    
    def test_response_contains_records(self, mock_kinesis_client):
        fake_records = [
            {"Data": '{"webTitle": "Test"}', "PartitionKey": "guardian_content"}
        ]
        fake_response = {
            "FailedRecordCount": 0,
            "Records": [{"SequenceNumber": "12345", "ShardId": "shardId-000000000000"}]
        }
        
        mock_kinesis_client.put_records.return_value = fake_response

        result = publish_to_kinesis(fake_records, "Guardian_content")
        assert type(result["Records"]) == list
        assert len(result["Records"]) > 0

        for record in result["Records"]:
            assert type(record) == dict