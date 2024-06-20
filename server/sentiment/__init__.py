from server.sentiment.analyzer import SentimentAnalyzer

analyzer = SentimentAnalyzer()
comment = "This service is not too good but I really loved it. "
# result = analyzer.calculate_sentence_sentiment(comment)
score = analyzer.sentiment_score(comment)
# print(result)

print(f"Comment: {comment}\nSentiment Score: {score:.2f}/5\n")