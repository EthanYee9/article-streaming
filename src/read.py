import boto3, json

client = boto3.client("kinesis")

# get shard IDs
shards = client.list_shards(StreamName="Guardian_content")["Shards"]
for shard in shards:
    shard_id = shard["ShardId"]
    print("Reading from shard:", shard_id)

    # get an iterator starting at the oldest available record
    shard_iterator = client.get_shard_iterator(
        StreamName="Guardian_content",
        ShardId=shard_id,
        ShardIteratorType="TRIM_HORIZON"
    )["ShardIterator"]

    # fetch records
    response = client.get_records(ShardIterator=shard_iterator, Limit=10)
    for r in response["Records"]:
        print("Got record:", json.loads(r["Data"]))