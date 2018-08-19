from kearch_common.requester import KearchRequester
from concurrent.futures import ThreadPoolExecutor
import time
import sys


CRAWLER_CHILD_IP = '192.168.11.10'
CRAWLER_CHILD_PORT = 10080

DATABASE_IP = '192.168.11.11'
DATABASE_PORT = 10080

NUM_THREAD = 5

REQUESTER_NAME = 'specialist_crawler_parent'

MAX_URLS = 100

# When you change DEBUG_UNIT_TEST true, this program run unit test.
DEBUG_UNIT_TEST = False


def crawl_a_page(url):
    if DEBUG_UNIT_TEST:
        ret = {'url': 'www.google.com', 'title_words': ['google', 'USA'], 'summary': 'Google is the biggest IT company.',
               'tfidf': {'google': 1.0}, 'inner_links': ['www.facebook.com'], 'outer_links': []}
        time.sleep(2)
        return ret
    else:
        crawler_requester = KearchRequester(CRAWLER_CHILD_IP, CRAWLER_CHILD_PORT, REQUESTER_NAME)
        ret = crawler_requester.request(path='/crawl_a_page', params={'url': url})
        return ret


# DEBUG CODE: Following lines are for debug. They are codes for unit test.
def get_next_urls_dummy(max_urls):
    urls = []
    for i in range(0, max_urls, 2):
        urls.extend(['www.google.com', 'www.facebook.com'])
    ret = {'urls': urls}
    time.sleep(5)
    return ret


if __name__ == '__main__':
    database_requester = KearchRequester(DATABASE_IP, DATABASE_PORT, REQUESTER_NAME)

    if DEBUG_UNIT_TEST:
        resp = get_next_urls_dummy(MAX_URLS)
    else:
        resp = database_requester.request(path='/get_next_urls', params={'max_urls': MAX_URLS})
    urls_in_queue = resp['urls']
    urls_to_push = list()
    data_to_push = list()

    while True:
        if DEBUG_UNIT_TEST:
            print('length of queue = ', len(urls_in_queue), file=sys.stderr)

        if len(urls_in_queue) == 0:
            if DEBUG_UNIT_TEST:
                # DEBUG CODE: Following lines are for debug. They are codes for unit test.
                resp = get_next_urls_dummy(MAX_URLS)
                urls_in_queue = resp['urls']
            else:
                # push data to database
                database_requester.request(path='/push_urls_to_queue', method='POST', payload={'urls': urls_to_push})
                database_requester.request(path='/push_webpage_to_database', method='POST', payload={'data': data_to_push})

                # fetch urls from database
                resp = database_requester.request(path='/get_next_urls', params={'max_urls': MAX_URLS})
                urls_in_queue = resp['urls']

        with ThreadPoolExecutor(max_workers=NUM_THREAD) as executor:
            results = executor.map(crawl_a_page, list(urls_in_queue[:NUM_THREAD]))
        results = filter((lambda x: x == {}), results)

        for r in results:
            urls_to_push.extend(r.inner_links)
            urls_to_push.extend(r.outer_links)
        for r in results:
            d = r
            del d['inner_links']
            del d['outer_links']
            data_to_push.append(d)

        urls_in_queue = urls_in_queue[NUM_THREAD:]