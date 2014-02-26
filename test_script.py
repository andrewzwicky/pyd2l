import threading
import queue
from urllib.request import urlopen

from pyd2l.match import Match, InvalidMatchError


def sequence(ids):
    matches = []

    for match_id in ids:
        print(match_id, end=' ')
        try:
            matches.append(Match(match_id, urlopen('http://dota2lounge.com/match?m={}'.format(match_id))))
            print('succesful')
        except InvalidMatchError:
            print('failed')
            pass

    return matches


def threaded(ids):
    def get_url(q, url):
        page = urlopen(url)
        id = int(page.geturl().replace('http://dota2lounge.com/match?m=', ''))
        try:
            match = Match(id, page)
            print('{} succesful'.format(id))
            q.put(match)
        except InvalidMatchError:
            print('{} failed'.format(id))
            pass

    urls = ['http://dota2lounge.com/match?m={}'.format(match_id) for match_id in ids]

    q = queue.Queue()

    for url in urls:
        t = threading.Thread(target=get_url, args=(q, url))
        t.daemon = True
        t.start()
        t.join()


    return [q.get() for _ in range(q.qsize())]


if __name__ == "__main__":
    ids = list(range(1150, 1171))
    seq = sequence(ids)
    thr = threaded(ids)
    print(seq == thr)
