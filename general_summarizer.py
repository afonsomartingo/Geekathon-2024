import boto3
import os
import json
from botocore.exceptions import ClientError
import re

AWS_DEFAULT_REGION = "us-west-2"

# Sensitive credentials should be handled securely (use environment variables or AWS IAM roles instead)
AWS_ACCESS_KEY_ID = "**********"
AWS_SECRET_ACCESS_KEY = "**********"
AWS_SESSION_TOKEN = "**********"

# Create a Bedrock Runtime client
client = boto3.client(
    "bedrock-runtime",
    region_name=AWS_DEFAULT_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN,
)

# Model ID for Meta Llama 3
model_id = "meta.llama3-70b-instruct-v1:0"

def generate_summary_bedrock_general(reviews):
    """
    Generate a summary for a given set of reviews.
    """
    review_texts = [r["review"] for r in reviews]
    reviewprompt = f"""
    **Task:**  
    Analyze a collection of movie reviews and craft an insightful and engaging summary. Your response should emulate a thoughtful film critic, capturing the essence of the reviews with a clear and compelling narrative.

    **Instructions:**  
    1. Thoroughly analyze the provided movie reviews, noting the nuances and sentiments expressed. Highlight the film's standout elements, such as storytelling, acting, cinematography, direction, or soundtrack, using examples from the reviews.
    2. Identify and elaborate on the **main positive aspects (pros)**, describing each point with context and examples. Mention scenes, performances, or techniques that resonated with viewers.
    3. Highlight and explain any **negative aspects (cons)**, focusing on recurring criticisms or notable shortcomings with specific references from the reviews.
    4. Provide an **overall sentiment analysis**, articulating whether the reviews are predominantly positive, negative, or mixed. Use examples to support your conclusion.
    5. **Assign a Rating (0-10):**  
    - Evaluate the reviews and assign a rating based on a structured assessment of key elements:
        - **Story/Plot:** Was the story engaging and well-developed? (Score: 0-10)
        - **Acting/Performances:** Were the actors convincing and impactful? (0-10)
        - **Cinematography/Visuals:** Did the film’s visuals enhance the experience? (0-10)
        - **Direction:** Was the director’s vision clear and well-executed? (0-10)
        - **Audience Engagement:** Did the film hold the audience’s attention and evoke emotions? (0-10)
    Add the scores from these categories to calculate the final rating. Provide the rating in this format:  
    `Rating: X/10`  
    (Replace `X` with the calculated rating.)

    6. Conclude with a **comprehensive summary** that weaves together key insights into a cohesive and thoughtful critique.

    **Response Style:**  
    Adopt a tone that feels professional yet conversational and approachable, akin to a seasoned film reviewer. Aim to engage the reader while providing detailed analysis. Avoid generic statements; instead, use vivid descriptions and specific examples.

    For example:
    - Instead of "The acting was good," try:  
    "The performances left a lasting impression, particularly the lead actor, who brought a raw and captivating energy to every scene."

    **Input Data:**  
    Please analyze the following movie reviews: {review_texts}
    """

    # Embed the prompt in Llama 3's instruction format
    formatted_prompt = f"""
    <|begin_of_text|><|start_header_id|>user<|end_header_id|>
    {reviewprompt}
    <|eot_id|>
    <|start_header_id|>assistant<|end_header_id|>
    """

    # Format the request payload using the model's native structure
    native_request = {
        "prompt": formatted_prompt,
        "max_gen_len": 1000,
        "temperature": 0.5,
    }

    # Convert the native request to JSON
    request = json.dumps(native_request)

    try:
        # Invoke the model with the request
        response = client.invoke_model(modelId=model_id, body=request)
    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        return "Error generating summary"

    # Decode the response body
    response_body = json.loads(response["body"].read())

    # Extract the summary from the response
    summary = response_body.get('generation', '').strip()
    
    return summary
