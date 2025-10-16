def load_fake_record():
    return [{"Data": '{"webTitle": "Test"}', "PartitionKey": "guardian_content"}]


def load_fake_response():
    return {
        "FailedRecordCount": 0,
        "Records": [{"SequenceNumber": "12345", "ShardId": "shardId-000000000000"}],
    }
