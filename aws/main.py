import sys
import os
from dotenv import load_dotenv
import boto3

# Load environment variables from .env file
load_dotenv()

# Get AWS credentials from environment variables
aws_region = os.getenv("AWS_DEFAULT_REGION")
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_session_token = os.getenv("AWS_SESSION_TOKEN")

# Set up the AWS Bedrock Runtime client with the loaded credentials
client = boto3.client(
    "bedrock-runtime",
    region_name=aws_region,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token,
)

def save_reviews_to_file(reviews, product_id, summary, filename=None):
    """
    Save reviews and summary to a text file.
    """
    if filename is None:
        filename = f"reviews_product.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"Summary:\n{summary}\n\n")
        for review in reviews:
            file.write(f"Review ID: {review['id']}\n")
            file.write(f"Rating: {review['rating']}\n")
            file.write(f"Price: {review['price']}\n")
            file.write(f"Review: {review['review']}\n")
            file.write("\n")
    print(f"Reviews and summary saved to {filename}")

def main():
    reviews = get_mock_reviews()  # Simulate getting review data
    insights = calculate_insights_rag(reviews)
    
    # Prompt the user for the product ID (or choose best product)
    user_input = input("Enter product ID for summary or press Enter to summarize the best product: ").strip()

    if user_input:
        # Generate summary for the specified product's reviews
        specified_product_reviews = [review for review in reviews if review['product_id'] == int(user_input)]
        if specified_product_reviews:
            summary = generate_summary_bedrock_general(specified_product_reviews)
            print("Summary for Product ID", user_input, ":", summary)
            print("Insights:", insights)
            save_reviews_to_file(specified_product_reviews, user_input, summary)
        else:
            print("No reviews found for Product ID", user_input)
    else:
        # Select the best product based on the reviews, summary, and insights
        best_product, best_review, best_quality_score, best_price_score, best_sentiment_score = select_best_product(reviews, None, insights)

        # Generate summary only for the best product's reviews
        best_product_reviews = [review for review in reviews if review['product_id'] == best_product]
        summary = generate_summary_bedrock_general(best_product_reviews)
        
        print("Summary:", summary)
        print("Insights:", insights)
        print("Best Product Selected:", best_product)
        print("Best Review:", best_review)
        print("Quality Score:", best_quality_score)
        print("Price Score:", best_price_score)
        print("Sentiment Score:", best_sentiment_score)
        save_reviews_to_file(best_product_reviews, best_product, summary, filename=f"best_product_{best_product}.txt")


if __name__ == "__main__":
    main()