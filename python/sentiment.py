import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews

def main():
    negids = movie_reviews.fileids('neg')
    posids = movie_reviews.fileids('pos')
    negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
    posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]
    negcutoff = int(len(negfeats) * 3 / 4)
    poscutoff = int(len(posfeats) * 3 / 4)
    trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
    testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
    classifier = NaiveBayesClassifier.train(trainfeats)

    with open("output.json") as fin:
        sid = SentimentIntensityAnalyzer()
        data = json.load(fin)
    for key in data:
        reviews = data[key]["reviews"]
        for i in range(len(reviews)):
            text = reviews[i]["review"]
            sentiment_dict = {'positive_probability':0, 'label':'', 'negative_probability':0}
            prob = classifier.prob_classify(word_feats(text.split(" ")))
            classification = classifier.classify(word_feats(text.split(" ")))
            sentiment_dict['positive_probability'] = prob.prob('pos')
            sentiment_dict['negative_probability'] = prob.prob('neg')
            sentiment_dict['label'] = classification
            reviews[i]["sentiment"] = sentiment_dict
        data[key]["reviews"] = reviews
    with open('out_with_sentiment.json', 'w') as outfile:
        json.dump(data, outfile)

def word_feats(words):
    return dict([(word, True) for word in words])

if __name__ == "__main__":main()