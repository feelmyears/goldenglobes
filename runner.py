from joblib import Parallel, delayed
import multiprocessing
import logging
import time
import utils
from TweetDB import TweetDB
from kb import *
from nltk.corpus import stopwords as nltkstopwords
from goldenglobes import *
from scorer import Scorer
from AwardClassifier import AwardClassifier

def main():
    print 'main'
    logging.basicConfig(filename='performance.log', level=logging.DEBUG)
    USE_FULL_SET = True
    USE_PICKLE = True
    PARALLEL=False
    start_time=time.time()
    logging.info(" startup at time:" +str(start_time))
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

    load_time=time.time()
    logging.info("tweets loaded after :" +str(load_time-start_time))
    # Getting Awards
    awards = MOTION_PICTURE_AWARDS + TELEVISION_AWARDS


    # Initializing Award Clasifier
    stopwords = nltkstopwords.words('english')
    classifier = AwardClassifier(awards, stopwords)
    classifier_time=time.time()
    logging.info("classifier created after :" +str(classifier_time-load_time))

    # Creating GoldenGlobes app

    gg = GoldenGlobes(awards, tweetDB, classifier)
    # s = Scorer(gg)
    # s.score_app()

    #parallelize this for loop
    end_time=time.time()
    logging.info("classification completed after :" +str(end_time-classifier_time))

    # logging.info("Begin Finding Host")
    #print "host"
    #print gg.find_host()
    bonuses = gg.get_bonuses()
    for bonus in bonuses:
        print bonus
        print bonuses[bonus]
    #print "presenters"
    # logging.info("Begin Finding Presenters")
    #print gg.find_presenters()
    print "award winners"
    # logging.info("Begin Finding Awards winners")
    winners = gg.find_winners()
    for a in gg.get_awards():
        print a
        print winners[a]


if __name__ == "__main__":
    main()
