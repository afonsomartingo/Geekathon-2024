def calculate_quality_score(review_text, summary):
    """
    Calculate the quality score based on the review text and summary.
    """
    if isinstance(summary, dict):
        summary = summary.get('summary', '')

    if not summary:
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
    normalized_rating = rating / 5
    max_price = 100
    normalized_price = 1 - (price / max_price)
    price_score = (normalized_rating + normalized_price) / 2
    return price_score


def calculate_sentiment_score(review_text):
    """
    Calculate the sentiment score based on review text.
    """
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
    rating = review.get('rating', 5)  # Default to 5 if no rating provided
    price = review.get('price', 50)  # Default to 50 if no price provided

    quality_score = calculate_quality_score(review_text, summary)
    price_score = calculate_price_score(rating, price)
    sentiment_score = calculate_sentiment_score(review_text)

    product_score = (quality_score + price_score + sentiment_score) / 3
    return product_score, quality_score, price_score, sentiment_score


def select_best_product(reviews, summary, insights):
    """
    Select the best product based on the reviews, summary, and insights.
    Handles multiple product_ids and returns the best for each.
    """
    product_scores = {}

    # Group reviews by product_id
    reviews_by_product = {}
    for review in reviews:
        product_id = review['product_id']
        if product_id not in reviews_by_product:
            reviews_by_product[product_id] = []
        reviews_by_product[product_id].append(review)

    # Calculate scores for each product
    for product_id, product_reviews in reviews_by_product.items():
        highest_score = -float('inf')
        best_review = None
        best_quality_score = None
        best_price_score = None
        best_sentiment_score = None

        for review in product_reviews:
            product_score, quality_score, price_score, sentiment_score = calculate_product_score(review, summary, insights)
            if product_score > highest_score:
                highest_score = product_score
                best_review = review
                best_quality_score = quality_score
                best_price_score = price_score
                best_sentiment_score = sentiment_score

        product_scores[product_id] = {
            'best_review': best_review,
            'highest_score': highest_score,
            'best_quality_score': best_quality_score,
            'best_price_score': best_price_score,
            'best_sentiment_score': best_sentiment_score,
        }

    # Identify the overall best product
    overall_best_product = max(product_scores.items(), key=lambda x: x[1]['highest_score'])

    return overall_best_product[0], product_scores[overall_best_product[0]]['best_review'], \
           product_scores[overall_best_product[0]]['best_quality_score'], \
           product_scores[overall_best_product[0]]['best_price_score'], \
           product_scores[overall_best_product[0]]['best_sentiment_score']
