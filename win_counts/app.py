import json
import json
import boto3
import winner_pb2  # This is generated from your protobuf file
import base64

# import requests

s3 = boto3.client("s3")
bucket_name = "buckerforsimrank"
file_name = "win-counts.json"


def grpc_encode(response_data):
    """
    Encodes WinnerResponse data to protobuf binary format.
    """
    return base64.b64encode(response_data.SerializeToString())


def grpc_decode(data):
    """
    Decodes a base64 encoded protobuf binary data to WinnerRequest.
    """
    # Decode the base64 string to bytes
    decoded_data = base64.b64decode(data)

    # Now parse the bytes using protobuf
    request_data = winner_pb2.WinnerRequest()
    request_data.ParseFromString(decoded_data)
    return request_data


def lambda_handler(event, context):
    # Decode the protobuf data

    # print(event)

    request_data = grpc_decode(
        event["body"]
    )  # Implement grpc_decode based on your setup

    winner = request_data.winner  # Extracted from the protobuf data

    # Read the win counts file from S3
    file_content = s3.get_object(Bucket=bucket_name, Key=file_name)["Body"].read()
    win_counts = json.loads(file_content)

    # Update win counts
    win_counts[winner] += 1

    # Save updated counts back to S3
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=json.dumps(win_counts))

    # Encode the response in protobuf
    response_data = winner_pb2.WinnerResponse()  # Create a protobuf response
    response_data.police = win_counts["police"]
    response_data.thief = win_counts["thief"]
    response_data.tie = win_counts["tie"]
    encoded_response = grpc_encode(
        response_data
    )  # Implement grpc_encode based on your setup

    return {"statusCode": 200, "body": encoded_response}
    # return {"statusCode": 200, "body": event}
