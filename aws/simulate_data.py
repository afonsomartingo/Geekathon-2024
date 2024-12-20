# simulate_data.py

def get_mock_reviews():
    return [
        {"product_id": 101, "id": 1, "review": "Amazing product! Totally worth it.", "rating": 5, "price": 29.99},
        {"product_id": 102, "id": 2, "review": "Not bad, but could be better.", "rating": 3, "price": 19.99},
        {"product_id": 101, "id": 3, "review": "Terrible experience. Never buying again.", "rating": 1, "price": 29.99},
        {"product_id": 103, "id": 4, "review": "Pretty good value for the price.", "rating": 4, "price": 39.99},
        {"product_id": 102, "id": 5, "review": "Loved it. Highly recommend!", "rating": 5, "price": 19.99},
        {"product_id": 101, "id": 6, "review": "Quality was okay but shipping took forever.", "rating": 3, "price": 29.99},
        {"product_id": 104, "id": 7, "review": "Exceeded my expectations!", "rating": 5, "price": 49.99},
        {"product_id": 101, "id": 8, "review": "The item broke after one use.", "rating": 1, "price": 29.99},
        {"product_id": 102, "id": 9, "review": "Exactly as described. Very satisfied.", "rating": 4, "price": 19.99},
        {"product_id": 103, "id": 10, "review": "Poor customer service ruined it for me.", "rating": 2, "price": 39.99},
        {"product_id": 104, "id": 11, "review": "Fast delivery and great quality.", "rating": 5, "price": 49.99},
        {"product_id": 101, "id": 12, "review": "Meh. It's just okay.", "rating": 3, "price": 29.99},
        {"product_id": 102, "id": 13, "review": "I am thrilled with this purchase!", "rating": 5, "price": 19.99},
        {"product_id": 103, "id": 14, "review": "It arrived damaged, very disappointed.", "rating": 1, "price": 39.99},
        {"product_id": 104, "id": 15, "review": "Good for the price. Would buy again.", "rating": 4, "price": 49.99},
        {"product_id": 101, "id": 16, "review": "Highly overpriced for what you get.", "rating": 2, "price": 29.99},
        {"product_id": 102, "id": 17, "review": "Amazing quality and great packaging.", "rating": 5, "price": 19.99},
        {"product_id": 103, "id": 18, "review": "It didn’t meet my expectations.", "rating": 2, "price": 39.99},
        {"product_id": 104, "id": 19, "review": "Works perfectly, very happy with it.", "rating": 5, "price": 49.99},
        {"product_id": 101, "id": 20, "review": "Decent product, but not great.", "rating": 3, "price": 29.99},
        {"product_id": 102, "id": 21, "review": "An absolute must-have!", "rating": 5, "price": 19.99},
        {"product_id": 103, "id": 22, "review": "Poorly made, wouldn’t recommend.", "rating": 1, "price": 39.99},
        {"product_id": 104, "id": 23, "review": "Very durable and well-designed.", "rating": 4, "price": 49.99},
        {"product_id": 101, "id": 24, "review": "Average at best.", "rating": 3, "price": 29.99},
        {"product_id": 102, "id": 25, "review": "Exceptional! Will buy more.", "rating": 5, "price": 19.99},
        {"product_id": 103, "id": 26, "review": "I had high hopes, but it failed.", "rating": 2, "price": 39.99},
        {"product_id": 104, "id": 27, "review": "Perfect for my needs!", "rating": 5, "price": 49.99},
        {"product_id": 101, "id": 28, "review": "Not worth the price.", "rating": 2, "price": 29.99},
        {"product_id": 102, "id": 29, "review": "Better than expected. Very happy.", "rating": 5, "price": 19.99},
        {"product_id": 103, "id": 30, "review": "Feels cheap and flimsy.", "rating": 1, "price": 39.99},
        {"product_id": 104, "id": 31, "review": "Well-packaged and high quality.", "rating": 4, "price": 49.99},
        {"product_id": 101, "id": 32, "review": "Overhyped and underdelivered.", "rating": 2, "price": 29.99},
        {"product_id": 102, "id": 33, "review": "Amazing craftsmanship!", "rating": 5, "price": 19.99},
        {"product_id": 103, "id": 34, "review": "It’s okay, not great.", "rating": 3, "price": 39.99},
        {"product_id": 104, "id": 35, "review": "Totally satisfied with this purchase.", "rating": 5, "price": 49.99},
        {"product_id": 101, "id": 36, "review": "I regret buying this.", "rating": 1, "price": 29.99},
        {"product_id": 102, "id": 37, "review": "Fantastic product and price.", "rating": 5, "price": 19.99},
        {"product_id": 103, "id": 38, "review": "Could be better, but it’s okay.", "rating": 3, "price": 39.99},
        {"product_id": 104, "id": 39, "review": "Highly durable and well-made.", "rating": 5, "price": 49.99},
        {"product_id": 101, "id": 40, "review": "Not as advertised, disappointing.", "rating": 2, "price": 29.99},
        {"product_id": 102, "id": 41, "review": "Love it! Would recommend to anyone.", "rating": 5, "price": 19.99},
        {"product_id": 103, "id": 42, "review": "Does the job, but nothing special.", "rating": 3, "price": 39.99},
        {"product_id": 104, "id": 43, "review": "Outstanding product!", "rating": 5, "price": 49.99},
        {"product_id": 101, "id": 44, "review": "Fell apart after a few uses.", "rating": 1, "price": 29.99},
        {"product_id": 102, "id": 45, "review": "Great value for money.", "rating": 4, "price": 19.99},
        {"product_id": 103, "id": 46, "review": "Below expectations, unfortunately.", "rating": 2, "price": 39.99},
        {"product_id": 104, "id": 47, "review": "One of the best purchases ever.", "rating": 5, "price": 49.99},
        {"product_id": 101, "id": 48, "review": "It works, but barely.", "rating": 2, "price": 29.99},
        {"product_id": 102, "id": 49, "review": "Solid performance and great quality.", "rating": 5, "price": 19.99},
        {"product_id": 103, "id": 50, "review": "Nothing extraordinary about it.", "rating": 3, "price": 39.99}
    ]
