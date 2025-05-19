import json

def handler(event, context):
    print("Received event:")
    print(json.dumps(event, indent=2))
    for record in event.get("Records", []):
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        print(f"New file uploaded: s3://{bucket}/{key}")
    return {"statusCode": 200}