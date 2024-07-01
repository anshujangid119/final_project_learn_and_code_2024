import re

class SentimentAnalyzer:
    def __init__(self):
        self.sentiment_lexicon = {
            'perfect': 3, 'good': 1, 'great': 2, 'excellent': 3, 'positive': 2, 'happy': 2,
            'fantastic': 3, 'amazing': 3, 'bad': -1, 'terrible': -2, 'awful': -3,
            'negative': -2, 'sad': -2, 'horrible': -3, 'poor': -1, 'love': 3, 'loved':3,
            'like': 2, 'dislike': -2, 'hate': -3, 'wonderful': 3, 'best': 3,
            'worst': -3, 'superb': 3, 'mediocre': -1, 'horrendous': -3, 'enjoy': 2,
            'abysmal': -3, 'delightful': 3, 'disgusting': -3, 'joyful': 3, 'depressing': -3,
            'satisfactory': 1, 'disappointing': -2, 'pleased': 2, 'upset': -2,
            'thrilled': 3, 'angry': -3, 'content': 1, 'frustrated': -2
        }

        self.negation_words = {'not', 'no', 'never', 'none'}
        self.intensifiers = {'very': 1.5, 'extremely': 2, 'quite': 1.2, 'really': 1.5, 'slightly': 0.5}

        self.contraction_patterns = [
            (re.compile(r"n't"), ' not'),
            (re.compile(r"'re"), ' are'),
            (re.compile(r"'s"), ' is'),
            (re.compile(r"'d"), ' would'),
            (re.compile(r"'ll"), ' will'),
            (re.compile(r"'t"), ' not'),
            (re.compile(r"'ve"), ' have'),
            (re.compile(r"'m"), ' am')
        ]

    def preprocess_and_tokenize(self, comment):
        for pattern, replacement in self.contraction_patterns:
            comment = pattern.sub(replacement, comment)
        comment = re.sub(r'[^a-zA-Z\s]', '', comment)
        return re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', comment.lower())

    def calculate_sentence_sentiment(self, sentence):
        words = sentence.split()
        sentence_score = 0
        sentence_weight = 0
        negation = False
        intensifier = 1

        for word in words:
            if word in self.negation_words:
                negation = not negation
            elif word in self.intensifiers:
                intensifier = self.intensifiers[word]
            elif word in self.sentiment_lexicon:
                sentiment = self.sentiment_lexicon[word] * intensifier
                sentence_score += -sentiment if negation else sentiment
                sentence_weight += abs(self.sentiment_lexicon[word])
                negation = False
                intensifier = 1

        return sentence_score, sentence_weight

    def sentiment_score(self, comment):
        sentences = self.preprocess_and_tokenize(comment)
        total_score = 0
        total_weight = 0

        for sentence in sentences:
            sentence_score, sentence_weight = self.calculate_sentence_sentiment(sentence)
            print(sentence_score)
            total_score += sentence_score
            total_weight += sentence_weight

        if total_weight > 0:
            weighted_average_score = total_score / total_weight
            print(weighted_average_score)
            # Normalize the score to a 1 to 5 scale
            normalized_score = 2 * weighted_average_score + 3
            normalized_score = max(1, min(5, normalized_score))  # Ensure the score is within 1 to 5
        else:
            normalized_score = 3  # Neutral score if no sentiment words are found

        return normalized_score

    def analyze_comments(self, comments):
        """
        Analyze a list of comments and return their sentiment scores.
        """
        return [self.sentiment_score(comment) for comment in comments]


# calculate_sentence_sentiment()