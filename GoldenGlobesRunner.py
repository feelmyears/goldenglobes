import utils
from TweetDB import TweetDB
from GoldenGlobesApp import GoldenGlobesApp
from GoldenGlobesKB import GoldenGlobesKB
from AwardClassifier import AwardClassifier
from scorer import Scorer
from nltk.corpus import stopwords as nltkstopwords

def main():
    print 'main'
    USE_FULL_SET = True
    USE_PICKLE = True

    tweetDB = None
    if USE_PICKLE:
        tweet_data = 'goldenglobesTweetDB'
        tweetDB = utils.load(tweet_data)
    else:
        tweet_data = 'goldenglobes.tab' if USE_FULL_SET else 'goldenglobes_mod.tab'
        tweetDB = TweetDB()
        tweetDB.import_tweets(tweet_data)
        tweetDB.process_tweets()
        utils.save(tweetDB, 'goldenglobesTweetDB')

    # Initializing GoldenGlobesKB, Classifier, GoldenGlobesApp, and Scorer
    kb = GoldenGlobesKB()
    stopwords = nltkstopwords.words('english')
    classifier = AwardClassifier(kb.get_awards(), stopwords)
    app = GoldenGlobesApp(tweetDB, kb, classifier)
    s = Scorer(app)

    # Score App
    s.score_app()

if __name__ == "__main__":
    main()
