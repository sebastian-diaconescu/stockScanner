from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentScaner:
    def __init__(self):
        # Instantiate the sentiment intensity analyzer with the existing lexicon
        self.vader = SentimentIntensityAnalyzer()
        # Update the lexicon
        new_words = {
            'crushes': 10,
            'beats': 5,
            'misses': -5,
            'trouble': -10,
            'falls': -100,
        }

        self.vader.lexicon.update(new_words)


    def GetSentiment(self, title):
        #score = self.vader.polarity_scores(sentence)
        return 5