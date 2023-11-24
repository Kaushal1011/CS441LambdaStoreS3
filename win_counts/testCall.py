import requests
import json
import winner_pb2
import base64

url = "https://lbg0sr2jhd.execute-api.us-east-1.amazonaws.com/Prod/process_winner"


def generate_base64_encoded_protobuf(agentname):
    # Create an instance of WinnerRequest
    winner_request = winner_pb2.WinnerRequest()
    winner_request.winner = agentname  # Example value

    # Serialize the protobuf message to a binary string
    serialized_data = winner_request.SerializeToString()

    # Encode the binary data to base64
    base64_encoded_data = base64.b64encode(serialized_data)

    return base64_encoded_data


# Your base64-encoded protobuf data
base64_encoded_data = generate_base64_encoded_protobuf("thief")


def invoke_lambda_via_http(encoded_data):
    """
    Invokes the Lambda function via an HTTP POST request with base64-encoded protobuf data.
    """
    try:
        # Prepare the payload
        payload = encoded_data

        headers = {"Content-Type": "application/grpc+proto"}

        # Make an HTTP POST request
        response = requests.post(url, data=payload, headers=headers)

        # Check for a successful response
        if response.status_code == 200:
            return response
        else:
            return (
                f"Error: Received status code {response.status_code} {response.json()}"
            )

    except Exception as e:
        print(f"Error invoking Lambda function via HTTP: {e}")
        return None


def decodeResponse(data):
    decoded = base64.b64decode(data)
    protocData = winner_pb2.WinnerResponse()
    protocData.ParseFromString(decoded)
    return protocData


# Invoke the Lambda function and print the response
lambda_response = invoke_lambda_via_http(base64_encoded_data)
data = lambda_response.text
decoded = decodeResponse(data)
print(decoded.police)
print(decoded.thief)
print(decoded.tie)
