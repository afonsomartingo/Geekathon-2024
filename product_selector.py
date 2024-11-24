# product_selector.py

def calculate_quality_score(review_text, summary):
    """
    Calculate the quality score based on the review text and summary.
    """
    if isinstance(summary, dict):
        summary = summary.get('summary', '')

    if not summary:
        # If summary is None or empty, return a default quality score
        print("Warning: Summary is None or empty, default quality score applied.")
        return 5

    if 'durable' in summary.lower():
        quality_score = 10
    else:
        quality_score = 5
    return quality_score


def calculate_price_score(rating, price):
    """
    Calculate price score based on rating and price.
    Higher ratings and lower prices are considered better value.
    """
    # Normalize rating (scale 0 to 1)
    normalized_rating = rating / 5

    # Normalize price (assuming a reasonable price range, e.g., $0 to $100)
    max_price = 100
    normalized_price = 1 - (price / max_price)  # Higher price = lower score

    # Combine normalized rating and price to calculate the price score
    price_score = (normalized_rating + normalized_price) / 2
    return price_score

def calculate_sentiment_score(review_text):
    """
    Calculate the sentiment score based on review text.
    """
    # Example sentiment analysis: Positive review = higher score, negative review = lower score
    positive_keywords = ['amazing', 'great', 'fantastic', 'loved']
    negative_keywords = ['terrible', 'worst', 'poor', 'disappointing']
    
    score = 0
    for word in positive_keywords:
        if word in review_text.lower():
            score += 1
    for word in negative_keywords:
        if word in review_text.lower():
            score -= 1
    return score

def calculate_product_score(review, summary, insights):
    """
    Calculate the overall product score based on review, summary, and insights.
    """
    review_text = review['review']
    rating = review['rating']
    price = review['price']

    quality_score = calculate_quality_score(review_text, summary)
    price_score = calculate_price_score(rating, price)
    sentiment_score = calculate_sentiment_score(review_text)

    # Combine the scores to get the overall product score
    product_score = (quality_score + price_score + sentiment_score) / 3
    return product_score, quality_score, price_score, sentiment_score
def select_best_product(reviews, summary, insights):
    """
    Select the best product based on the reviews, summary, and insights.
    """
    best_product = None
    highest_score = -float('inf')
    best_review = None
    best_quality_score = None
    best_price_score = None
    best_sentiment_score = None

    # Ensure summary is not None before processing
    #if not summary:
    #    print("Warning: Summary is None, skipping summary-related calculations.")

    for review in reviews:
        product_score, quality_score, price_score, sentiment_score = calculate_product_score(review, summary, insights)
        if product_score > highest_score:
            highest_score = product_score
            best_product = review['product_id']
            best_review = review
            best_quality_score = quality_score
            best_price_score = price_score
            best_sentiment_score = sentiment_score

    return best_product, best_review, best_quality_score, best_price_score, best_sentiment_score
