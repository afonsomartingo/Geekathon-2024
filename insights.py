import boto3
import json

AWS_DEFAULT_REGION = "us-west-2"

# Sensitive credentials should be handled securely (use environment variables or AWS IAM roles instead)
AWS_ACCESS_KEY_ID = "**********"
AWS_SECRET_ACCESS_KEY = "**********"
AWS_SESSION_TOKEN = "**********"

# Configure AWS session
session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN,
    region_name=AWS_DEFAULT_REGION
)

# Initialize boto3 client for Bedrock Runtime
boto_runtime = session.client('bedrock-runtime', region_name=AWS_DEFAULT_REGION)

def retrieve_and_generate(input_text, kb_id, model_arn=None):
    try:
        # Ensure that kb_id is passed
        if not kb_id:
            raise ValueError("Knowledge Base ID (kb_id) is required.")

        # Correct API call to retrieve and generate
        response = boto_runtime.invoke_model(
            modelId=model_arn,  # Use the model ARN directly passed to the function
            body=json.dumps({
                'text': input_text,
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': kb_id,  # Your Knowledge Base ID
                    'modelArn': model_arn  # Use the model ARN directly
                },
                'type': 'KNOWLEDGE_BASE'
            })
        )

        # Parse the response
        response_body = response['body'].read().decode('utf-8')

        # Return the generated response as a JSON object
        return json.loads(response_body)

    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
query = "What is the process of photosynthesis?"
kb_id = "DRVFOSAVVH"  # Your Knowledge Base ID
model_arn = "arn:aws:bedrock:us-west-2:076122618127:model/llama-3.1-70b-instruct"  # ARN of Llama 3.1 70B Instruct

response = retrieve_and_generate(query, kb_id, model_arn)
if response:
    print("Generated Response:", response)
else:
    print("Failed to generate a response.")
