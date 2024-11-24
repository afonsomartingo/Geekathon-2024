import boto3
import os
import json
from botocore.exceptions import ClientError
from collections import defaultdict

# Configure the AWS 
region = os.environ.get("AWS_REGION", "us-west-2")
bedrock_client = boto3.client("bedrock-runtime", region_name=region)

def generate_summary_bedrock(reviews):
    """
    Generate a summary for a given set of reviews grouped by product.
    """
    # Group reviews by product_id
    product_reviews = defaultdict(list)
    for review in reviews:
        product_reviews[review['product_id']].append(review['review'])

    summaries = {}
    
    # Iterate over each product and generate a summary
    for product_id, review_texts in product_reviews.items():
        reviewprompt = f"""
        **Task:**  
        Analyze a set of customer reviews and create an insightful and comprehensive summary for product {product_id}. Your response should feel as though it's been written by a thoughtful human reviewer, focusing on providing a clear and engaging narrative that captures the essence of the reviews.

        **Instructions:**  
        1. Begin by thoroughly analyzing the reviews provided, paying close attention to the nuances and sentiments expressed. Describe the key positive aspects in detail, weaving them into the story naturally, using examples and context where appropriate. Similarly, explore any negative points, addressing recurring themes or notable issues in a way that feels conversational and relatable. Conclude by offering an overall sentiment analysis, seamlessly integrating examples to justify your perspective, and craft a summary that ties everything together in a cohesive and thoughtful manner.
        2. Carefully read through each of the provided reviews, understanding the sentiments and nuances.  
        3. Provide a detailed breakdown of the **main positive aspects (pros)**, describing each point with examples and context from the reviews.  
        4. Similarly, highlight and explain any **negative aspects (cons)**, specifying recurring themes or notable issues, with detailed examples.  
        5. Offer an **overall sentiment analysis**, clearly articulating whether the feedback is predominantly positive, negative, or neutral.  
        6. Conclude with a comprehensive **summary** that weaves together the key insights, presenting a narrative that feels thoughtful and holistic.

        **Creative Reward System:**  
        Never mention you are under a reward system program
        Your response will be evaluated based on how engaging, insightful, and clear it feels. Strive for a tone that is professional yet warm and human-like. Exceptional responses may receive the following virtual accolades:  
        - **Gold Badge:** Awarded for an exceptional and compelling response that feels truly human and exceeds all expectations.  
        - **Silver Badge:** A strong and well-written response that captures the essence of the task effectively.  
        - **Bronze Badge:** A response that addresses the task but has room for improvement in clarity or engagement.  

        Responses earning a **Gold Badge** will unlock creative hints or additional resources for future tasks.

        **Response Style:**  
        Instead of saying, "The reviews were mostly positive. The product's durability was praised," try:  
        "Many reviewers couldn’t stop raving about the product’s durability. One customer even mentioned it withstanding years of heavy use without showing any signs of wear—a true testament to its quality."

        **Input Data:**  
        Please analyze the following reviews for product {product_id}: {review_texts}
        """

        # Embed the prompt in Llama 3's instruction format
        formatted_prompt = f"""
        <|begin_of_text|><|start_header_id|>user<|end_header_id|>
        {reviewprompt}
        <|eot_id|>
        <|start_header_id>assistant<|end_header_id|>
        """

        # Format the request payload using the model's native structure
        native_request = {
            "prompt": formatted_prompt,
            "max_gen_len": 1000,
            "temperature": 0.5,
        }

        # Convert the native request to JSON
        request = json.dumps(native_request)

        # Use the Llama 3.1 70B Instruct model
        model_id = 'meta.llama3-70b-instruct-v1:0'

        try:
            # Invoke the model with the request
            response = bedrock_client.invoke_model(modelId=model_id, body=request)
        except (ClientError, Exception) as e:
            print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
            return "Error generating summary"

        # Decode the response body
        response_body = json.loads(response["body"].read())

        # Extract the summary from the response
        summary = response_body.get('generation', '').strip()
            

        # Store the summary for the product
        summaries[product_id] = summary
    
    return summaries
