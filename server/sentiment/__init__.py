from server.sentiment.analyzer import SentimentAnalyzer

analyzer = SentimentAnalyzer()
comment = "food is good but not good enough"
# result = analyzer.calculate_sentence_sentiment(comment)
score = analyzer.sentiment_score(comment)
# print(result)

print(f"Comment: {comment}\nSentiment Score: {score:.2f}/100\n")