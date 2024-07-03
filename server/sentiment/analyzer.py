import re

class SentimentAnalyzer:
    def __init__(self):
        self.sentiment_lexicon = {
            'delicious': 3, 'tasty': 2, 'savory': 2, 'flavorful': 2, 'bland': -1,
            'spicy': 1, 'sweet': 2, 'sour': -1, 'bitter': -2, 'salty': -1,
            'fresh': 2, 'stale': -2, 'juicy': 2, 'dry': -2, 'crispy': 2,
            'soggy': -2, 'succulent': 3, 'delectable': 3, 'mouthwatering': 3,
            'yummy': 2, 'unappetizing': -2, 'greasy': -1, 'burnt': -2,
            'overcooked': -2, 'undercooked': -2, 'perfectly cooked': 3, 'raw': -2,
            'heavenly': 3, 'inedible': -3, 'palatable': 1, 'scrumptious': 3,
            'appetizing': 2, 'repulsive': -3, 'gross': -3, 'finger-licking': 2,
            'hearty': 2, 'rich': 2, 'creamy': 2, 'buttery': 2, 'zesty': 2,
            'smoky': 1, 'burned': -2, 'underdone': -2, 'overdone': -2, 'rubbery': -2,
            'oily': -1, 'slimy': -2, 'fluffy': 2, 'dense': -1, 'light': 1,
            'heavy': -1, 'melty': 2, 'chewy': -1, 'filling': 1, 'comforting': 2,
            'divine': 3, 'unpalatable': -3, 'exquisite': 3, 'vile': -3,
            'tasteless': -2, 'aromatic': 2, 'fragrant': 2, 'piquant': 2,
            'mouth-watering': 3, 'lip-smacking': 2, 'nutritious': 2, 'nourishing': 2,
            'refreshing': 2, 'tempting': 2, 'indulgent': 2, 'satisfying': 2,
            'exquisite': 3, 'divine': 3, 'ambrosial': 3, 'displeasing': -2,
            'inedible': -3, 'tender': 2, 'juicy': 2, 'succulent': 3, 'gamey': -1,
            'rubbery': -2, 'tangy': 2, 'zingy': 2, 'heavenly': 3, 'unctuous': 1,
            'unseasoned': -2, 'burnt': -2, 'overpowering': -1, 'watery': -1,
            'gummy': -2, 'mushy': -1, 'chunky': 1, 'smooth': 2, 'velvety': 2,
            'gritty': -2, 'cloying': -2, 'bittersweet': -1, 'rancid': -3,
            'putrid': -3, 'overripe': -2, 'underripe': -2, 'ripe': 2, 'fizzy': 1,
            'carbonated': 1, 'bubbly': 2, 'flat': -1, 'frothy': 1, 'effervescent': 2
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