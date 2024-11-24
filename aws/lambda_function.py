import json
import requests
from bs4 import BeautifulSoup
from general_summarizer import generate_summary_bedrock_general
from product_selector import select_best_product
from collections import defaultdict
import random
from insights import retrieve_and_generate  
import boto3

def save_reviews_to_file(reviews, filename="reviews_summary.txt"):
    """
    Save reviews and summary to a text file.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        for review in reviews:
            file.write(f"{review}\n\n")
    print(f"Reviews saved to {filename}")


def scrapper_BeautifulSoup(url, class_name):
    """
    Scrape reviews from a given URL using BeautifulSoup.
    :param url: The URL to scrape from.
    :param class_name: The class name for the review elements.
    :return: A list of reviews (strings).
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        # Send a GET request to the URL
        response = requests.get(url, headers=headers)
        print(f"URL: {url}")
        print(f"Response Status Code: {response.status_code}")

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all review containers using the provided class_name
            review_containers = soup.find_all('p', class_=class_name)
            print(f"Found {len(review_containers)} reviews")

            # Extract and combine text from all matching review containers
            reviews = [review.get_text(strip=True) for review in review_containers]

            if not reviews:
                print("No reviews found in the specified container.")
            else:
                print(f"Extracted Reviews: {reviews[:5]}...")  # Displaying first 5 reviews for debugging

            return reviews
        else:
            print(f"Error: Failed to retrieve the content. Status Code: {response.status_code}")
            return []

    except requests.exceptions.RequestException as e:
        # Handle any errors with the request (e.g., network issues, invalid URL)
        print(f"Request Error: {e}")
        return []
    except Exception as e:
        # Catch any other unexpected errors
        print(f"Unexpected Error: {e}")
        return []

def lambda_handler(event, context):
    """
    AWS Lambda handler to scrape reviews and process them to generate insights, summary, and product selection.
    """
    try:
        # Ensure event body is parsed correctly
        if isinstance(event.get("body"), str):
            req_data = json.loads(event["body"])
        else:
            req_data = event["body"]  # Already parsed in case it's a dict

        movie_name = req_data.get("url")
        print(f"Received Movie Name: {movie_name}")

        movies = movie_name.split(",")

        if not movie_name:
            return {
                'statusCode': 400,
                'body': json.dumps("Error: 'url' field is required in the event input.")
            }

        dict_reviews = defaultdict(list)
        dict_reviews["reviews"] = []
        # Scrape critic reviews
        for m in movies:
            critic_reviews = scrapper_BeautifulSoup(
                f"https://www.rottentomatoes.com/m/{m}/reviews", 
                "review-text"
            )

            # Scrape public reviews
            audience_reviews = scrapper_BeautifulSoup(
                f"https://www.rottentomatoes.com/m/{m}/reviews?type=user", 
                "audience-reviews__review"
            )

            total_rating=0
            price = random.uniform(1, 60)
            
            # Combine reviews
            critic_reviews.extend(audience_reviews)
            all_reviews = critic_reviews
            print(f"Total Reviews Scraped: {len(all_reviews)}")
            
            dict_review = {}
            for i in range(len(all_reviews)):
                dict_review = {}  # Initialize a new dictionary for each review
                dict_review["product_id"] = m  # Assuming 'product_id' exists in your reviews
                dict_review["id"] = i + 1  # Assign an incremental ID starting from 1
                dict_review["review"] = all_reviews[i]
                dict_reviews["reviews"].append(dict_review)

                total_rating += random.uniform(1, 10)

            print(dict_reviews["reviews"][0])

        if not dict_reviews:
            return {
                'statusCode': 404,
                'body': json.dumps("Error: No reviews found for the provided movie name.")
            }

        # Step 1: Generate summary
        summary = generate_summary_bedrock_general(dict_reviews["reviews"])  # Now passing list of strings

        print(f"SUMMARY: {summary}")

        # Select the best product based on the reviews, summary, and insights
        best_product, best_review, best_quality_score, best_price_score, best_sentiment_score = select_best_product(dict_reviews["reviews"], None, None)

        # Generate summary only for the best product's reviews
        best_product_reviews = [review for review in dict_reviews["reviews"] if review['product_id'] == best_product]
        best_summary = generate_summary_bedrock_general(best_product_reviews)

        # Generate response
        average_rating = round(total_rating / len(all_reviews), 1)

        response = {
            "summary": best_summary,
            "rating": average_rating, 
            "price": price,
            "message": f"Summary and insights generated for movie '{movie_name}'.",
            "best_product": best_product,
            "best_review": best_review,
            "best_quality_score": best_quality_score,
            "best_price_score": best_price_score,
            "best_sentiment_score": best_sentiment_score
        }

        print("RESPONSE: ", response)

        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Internal Server Error: {str(e)}")
        }
