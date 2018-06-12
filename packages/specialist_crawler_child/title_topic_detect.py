# -*- coding: utf-8 -*-

import sys
from gensim import corpora
import webpage
import argparse
import multiprocessing as mult
import pickle
import random
from sklearn.naive_bayes import BernoulliNB

n_urls = 2000
n_tests = 100
IN_TOPIC = 0
OUT_OF_TOPIC = 1

cache_file_dir = 'title_topic_detect_cache/'


class TitleTopicClassifier(object):
    def __init__(self):
        self.dictionary = corpora.Dictionary.load_from_text(
            cache_file_dir + 'gensim_title.dict')
        with open(cache_file_dir + 'clf_title.pickle', 'rb') as f:
            self.clf = pickle.load(f)

    def classfy(self, text):
        bow = self.dictionary.doc2bow(text)
        res = self.clf.predict([alist_to_vector(bow, self.dictionary)])
        return res[0]

    def classfy_log_probability(self, text):
        bow = self.dictionary.doc2bow(text)
        res = self.clf.predict_log_proba(
            [alist_to_vector(bow, self.dictionary)])
        return res[0]


def alist_to_vector(al, dictionary):
    r = [0 for i in range(len(dictionary))]
    for (i, f) in al:
        r[i] += f
    return r


def url_to_title_words(url):
    w = webpage.create_webpage_with_cache(url)
    return w.title_words


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "topic_url_list", help="sample webpages about topic")
    parser.add_argument(
        "random_url_list", help="random webpages")
    parser.add_argument('--cache', help='use cache', action='store_true')
    parser.add_argument('--ntopic', help='number of topics', nargs=1)
    args = parser.parse_args()

    with open(args.topic_url_list, 'r') as f:
        topic_urls1 = f.readlines()
        topic_urls1 = list(map(lambda x: x.replace('\n', ''), topic_urls1))
    f.close()
    with open(args.random_url_list, 'r') as f:
        random_urls1 = f.readlines()
        random_urls1 = list(map(lambda x: x.replace('\n', ''), random_urls1))
    f.close()

    random.shuffle(topic_urls1)
    topic_urls = topic_urls1[:n_urls]
    random.shuffle(random_urls1)
    random_urls = random_urls1[:n_urls]

    if not args.cache:
        p = mult.Pool(mult.cpu_count())
        texts = p.map(url_to_title_words,
                      topic_urls[:n_urls] + random_urls[:n_urls])
        print("Downloading finish", file=sys.stderr)

        texts = list(filter(lambda x: not x == [], texts))
        p.close()
        dictionary = corpora.Dictionary(texts)
        dictionary.save_as_text(cache_file_dir + 'gensim_title.dict')
        print('dictionary size = ', len(dictionary))

        sc_samples = list()
        sc_labels = list()

        p = mult.Pool(mult.cpu_count())
        texts = p.map(
            url_to_title_words, topic_urls[:n_urls])
        p.close()
        texts = list(filter(lambda x: not x == [], texts))
        bows = [dictionary.doc2bow(text) for text in texts]
        for bow in bows:
            sc_samples.append(alist_to_vector(bow, dictionary))
            sc_labels.append(IN_TOPIC)
        p = mult.Pool(mult.cpu_count())
        texts = p.map(
                url_to_title_words, random_urls[:n_urls])
        p.close()
        texts = list(filter(lambda x: not x == [], texts))
        bows = [dictionary.doc2bow(text) for text in texts]
        for bow in bows:
            sc_samples.append(alist_to_vector(bow, dictionary))
            sc_labels.append(OUT_OF_TOPIC)

        clf = BernoulliNB()
        clf.fit(sc_samples, sc_labels)
        with open(cache_file_dir + 'clf_title.pickle', 'wb') as f:
            pickle.dump(clf, f)
        print("Classifier making finish", file=sys.stderr)

    else:
        dictionary = corpora.Dictionary.load_from_text(cache_file_dir + 'gensim_title.dict')
        with open(cache_file_dir + 'clf_title.pickle', 'rb') as f:
            clf = pickle.load(f)

    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    for u in topic_urls1[n_urls:n_urls + n_tests]:
        c = TitleTopicClassifier()
        w = webpage.create_webpage_with_cache(u)
        print(u, c.classfy_log_probability(w.words))
        if c.classfy(w.title_words) == IN_TOPIC:
            true_positive += 1
        else:
            true_negative += 1
    for u in random_urls1[n_urls:n_urls + n_tests]:
        c = TitleTopicClassifier()
        w = webpage.create_webpage_with_cache(u)
        print(u, c.classfy_log_probability(w.words))
        if c.classfy(w.words) == OUT_OF_TOPIC:
            false_negative += 1
        else:
            false_positive += 1
    precision = true_positive / (true_positive + false_positive)
    recall = true_positive / (true_positive + false_negative)
    fmeasure = 2 * precision * recall / (precision + recall)
    print('TP=', true_positive, 'TN=', true_negative,
          'FP=', false_positive, 'FN=', false_negative,
          'precision=', precision, 'recall=', recall, 'fmeasure=', fmeasure)
