# coding: utf-8
import json
import random
import re
import time
import requests

class Crawler():
    def __init__(self, total_user, wpath, headers, crawl_repo=False, crawl_follow=False, crawl_commit=False, start_id=1, end_id=34991752):
        self.total_user = total_user
        self.wpath = wpath
        self.headers = headers
        self.crawl_repo = crawl_repo
        self.crawl_follow = crawl_follow
        self.crawl_commit = crawl_commit
        self.start_id = start_id
        self.end_id = end_id
        self.init_urls()

    def init_urls(self):
        self.url_rate_limit = "https://api.github.com/rate_limit"
        self.url_user_profile = 'https://api.github.com/user/'
        self.url_search_commits = 'https://api.github.com/search/commits'

    def check_rate_limit(self):
        # in case 403 Forbidden
        remaining = requests.get(url=self.url_rate_limit,headers=self.headers).json()['rate']['remaining']
        while remaining == 0:
            print("exceeds X-RateLimit-Remaining, please wait 10 minutes")
            time.sleep(300)
            remaining = requests.get(url=self.url_rate_limit, headers=self.headers).json()['rate']['remaining']

    def get_user_profile_by_id(self, id):
        url = self.url_user_profile + str(id)
        # in case rate limit
        self.check_rate_limit()
        user_profile_response = requests.get(url, headers=self.headers)
        # if d exists, return user profile, else return None
        if user_profile_response.status_code == 200:
            return user_profile_response.json()
        elif user_profile_response.status_code != 404:
            print(url, user_profile_response.status_code)

    # repos, followers, following
    def get_specified_user_list(self, url):
        # remove the suffix like: {/owner}{/repo}
        url = re.sub(r'{.*}$', "", url)
        page = 0
        detailed_list = []
        # detailed list should be integrated
        while True:
            # in case rate limit
            self.check_rate_limit()
            page += 1
            params = {"per_page": 100, "page": page}
            # Array, each element is a dict
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code != 200:
                print(url, response.status_code)
                return

            detail_per_page = response.json()
            if len(detail_per_page) == 0:
                break
            detailed_list += detail_per_page
        return detailed_list

    def get_user_commits(self, name):
        self.headers['Accept'] = 'application/vnd.github.cloak-preview'
        page = 0
        commits = []
        commits_len = 0

        try:
            while True:
                page += 1
                params = {"q": "author:"+name, "per_page": 100, "page": page}
                self.check_rate_limit()
                response = requests.get(self.url_search_commits,headers=self.headers, params=params)
                if response.status_code != 200:
                    print(self.url_search_commits, response.status_code)
                    return
                commits_per_page = response.json()
                if len(commits_per_page['items']) == 0:
                    break
                commits += commits_per_page['items']
                commits_len = commits_per_page['total_count']
            if len(commits) != commits_len:
                return
            return commits

        # remove Accept
        finally:
            self.headers.pop('Accept')


    def detect_suspicious_user(self, html_url):
        # in case rate limit
        self.check_rate_limit()
        user_html_response = requests.get(html_url, headers=self.headers)
        # 404 - True, 200 - False, others - None
        if user_html_response.status_code == 404:
            return True
        elif user_html_response.status_code == 200:
            return False
        else:
            print(html_url, user_html_response.status_code)

    def get_user_info(self, id):
        user = self.get_user_profile_by_id(id)
        # if id doesn't exist, return None
        if not user:
            return
        # if id is suspicious, flag
        is_suspicious = self.detect_suspicious_user(user['html_url'])
        if is_suspicious:
            user['is_suspicious'] = True
            return user
        elif not is_suspicious:
            user['is_suspicious'] = False
        elif is_suspicious is None:
            return

        if self.crawl_repo:
            repos_list = self.get_specified_user_list(user['repos_url'])
            if repos_list is None:
            # or len(repos_list) != user['public_repos']:
                return
            user['repos_list'] = repos_list

        if self.crawl_follow:
            followers_list = self.get_specified_user_list(user['followers_url'])
            following_list = self.get_specified_user_list(user['following_url'])
            if followers_list is None or following_list is None:
                # or len(followers_list) != user['followers']
                # or len(following_list) != user['following']
                return
            user['followers_list'] = followers_list
            user['following_list'] = following_list

        if self.crawl_commit:
            commits_list = self.get_user_commits(user['login'])
            if commits_list is None:
                return
            user['commits_count'] = len(commits_list)
            user['commits_list'] = commits_list

        return user

    def pop_url(self, info):
        if isinstance(info, list):
            for each in info:
                self.pop_url(each)
        if isinstance(info, dict):
            for key in list(info.keys()):
                if re.match(r'.*_?url$', key):
                    info.pop(key)
                elif not isinstance(info[key], str):
                    self.pop_url(info[key])

    def write_result(self, user_info, wf):
        # delete urls
        for user_key in list(user_info.keys()):
            if re.match(r'.*_?url$', user_key):
                user_info.pop(user_key)
            # get repos_list/followers_list/following_list/commits_list
            else:
                self.pop_url(user_info[user_key])
        # writing results
        json.dump(user_info, wf, ensure_ascii=False)
        wf.write('\n')

    def run(self):
        cur = 0
        with open(self.wpath, 'a') as wf:
            while cur < self.total_user:
                try:
                    id = random.randint(self.start_id, self.end_id)

                    user_info = self.get_user_info(id)
                    # in case: id doesn't exist or the information is not integrated
                    if not user_info:
                        continue
                    #delete urls
                    self.write_result(user_info, wf)

                    cur += 1
                    print(str(cur), "users got")
                except KeyboardInterrupt:
                    exit()
                except Exception as ex:
                    print(ex)
                    time.sleep(5)
                    continue

