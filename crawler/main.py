# coding: utf-8
import sys
import config
from utils.user_crawler import Crawler

def main(argv):
    headers = config.headers
    total_user = argv[0]
    wpath = argv[1]
    # crawl_repo = bool(argv[2])
    # crawl_follow = bool(argv[3])
    # crawl_commit = bool(argv[4])
    crawler = Crawler(total_user=total_user, wpath=wpath, headers=headers, crawl_repo=True, crawl_follow=True, crawl_commit=True, start_id=1, end_id=34991752)
    crawler.run()

# python main.py 100 data.txt
if __name__ == '__main__':
    # add token
    main(sys.argv[1:])
