#coding:utf8
import datetime
import json
import random
import re
import sys
import time

import requests

import config
from crawler import load_data

# add token
headers = config.headers

def check_rate_limit_remaining():
    # 403 Forbidden
    url = "https://api.github.com/rate_limit"
    try:
        remaining = requests.get(url=url,headers=headers).json()['rate']['remaining']
        while remaining == 0:
            print "exceeds X-RateLimit-Remaining, please wait 5 minutes"
            time.sleep(300)
            remaining = requests.get(url=url, headers=headers).json()['rate']['remaining']
        print "RateLimit-Remaining:", remaining

    except requests.exceptions.ConnectionError:
        print "ConnectionError when checking rate limit -- please wait 3 seconds"
        time.sleep(3)
    except requests.exceptions.Timeout:
        print "Timeout when checking rate limit -- please wait 3 seconds"
        time.sleep(3)
    except KeyboardInterrupt:
        sys.exit()
    except:
        print "An Unknown Error during the rate limit check"

def get_single_user_profile_by_id(id):
    print "---- get_single_user_profile_by_id ----"
    url = 'https://api.github.com/user/' + str(id)
    try:
        # in case rate limit
        check_rate_limit_remaining()
        user_profile_response = requests.get(url, headers=headers)
        # if d exists, return user profile, else return None
        if user_profile_response.status_code == 200:
            return user_profile_response.json()

    except requests.exceptions.ConnectionError:
        print "ConnectionError when getting user profile -- please wait 3 seconds"
        time.sleep(3)
    except requests.exceptions.Timeout:
        print "Timeout when getting user profile -- please wait 3 seconds"
        time.sleep(3)
    except KeyboardInterrupt:
        sys.exit()
    except:
        print "An Unknown Error when getting a single user's profile by id"

# repos, followers, following
def get_single_user_detailed_list(url):
    #remove the suffix like: {/owner}{/repo}
    url = re.sub(r'{.*}$', "", url)
    page = 0
    detailed_list = []
    # detailed list should be integrated
    try:
        while True:
            print "---- get detailed list from "+url+" ----", "current: "+str(len(detailed_list))+" pieces"
            # in case rate limit
            check_rate_limit_remaining()
            page += 1
            params = {"per_page": 100, "page": page}
            # Array, each element is a dict
            response = requests.get(url, headers=headers, params=params)
            if response.status_code != 200:
                return
            detail_per_page = response.json()
            if len(detail_per_page) == 0:
                break
            detailed_list += detail_per_page
        return detailed_list
    except requests.exceptions.ConnectionError:
        print "ConnectionError when getting detailed list -- please wait 3 seconds"
        time.sleep(3)
    except requests.exceptions.Timeout:
        print "Timeout when getting detailed list -- please wait 3 seconds"
        time.sleep(3)
    except KeyboardInterrupt:
        sys.exit()
    except:
        print "An Unknown Error when getting a single user's detailed list"

def get_single_user_commits(name):
    headers['Accept'] = 'application/vnd.github.cloak-preview'
    url = 'https://api.github.com/search/commits'
    page = 0
    commits = []
    try:
        while True:
            print "---- get commits of "+name+" ----", "current: "+str(len(commits))+" pieces"
            page += 1
            params = {"q": "author:"+name, "per_page": 100, "page": page}
            check_rate_limit_remaining()
            commits_per_page = requests.get(url,headers=headers, params=params).json()
            if len(commits_per_page['items']) == 0:
                break
            commits += commits_per_page['items']
            print commits
        return commits

    except requests.exceptions.ConnectionError:
        print "ConnectionError when getting commits -- please wait 3 seconds"
        time.sleep(3)
    except requests.exceptions.Timeout:
        print "Timeout when getting commits -- please wait 3 seconds"
        time.sleep(3)
    except KeyboardInterrupt:
        sys.exit()
    except:
        print "An Unknown Error when getting a single user's commits"


def detect_suspicious_user(html_url):
    print "---- detect_suspicious_user ----"
    try:
        # in case rate limit
        check_rate_limit_remaining()
        user_html_response = requests.get(html_url, headers=headers)
        # 404 - True, 200 - False, others - None
        if user_html_response.status_code == 404:
            return True
        elif user_html_response.status_code == 200:
            return False
    except requests.exceptions.ConnectionError:
        print "ConnectionError when detecting suspicious user -- please wait 3 seconds"
        time.sleep(3)
    except requests.exceptions.Timeout:
        print "Timeout when detecting suspicious user -- please wait 3 seconds"
        time.sleep(3)
    except KeyboardInterrupt:
        sys.exit()
    except:
        print "An Unknown Error when detecting suspicious user"

def get_single_user_info(id, follow):
    print "---- get_single_user_info ----"
    user = get_single_user_profile_by_id(id)
    # if id doesn't exist, return None
    if not user:
        return
    # if id is suspicious, flag
    user['is_suspicious'] = detect_suspicious_user(user['html_url'])
    if user['is_suspicious'] == True:
        return user
    elif user['is_suspicious'] == None:
        return

    repos_list = get_single_user_detailed_list(user['repos_url'])
    if repos_list == None or len(repos_list) != user['public_repos']:
        return
    user['repos_list'] = repos_list

    if follow:
        followers_list = get_single_user_detailed_list(user['followers_url'])
        following_list = get_single_user_detailed_list(user['following_url'])
        if followers_list == None or len(followers_list) != user['followers'] or following_list == None or len(following_list) != user['following']:
            return
        user['followers_list'] = followers_list
        user['following_list'] = following_list
    return user

def randomly_select_users(needed_users, follow=False, start_id=1, end_id=39610000):
    cur = 0
    path = 'data'
    existing = load_data.load_existing(path)
    while cur < needed_users:
        print "---- randomly_select_users ----"
        id = random.randint(start_id, end_id)
        if id in existing:
            continue
        user_info = get_single_user_info(id, follow)
        # in case: id doesn't exist or the information is not integrated
        if not user_info:
            continue
        existing.append(id)
        # write file
        f = open(path, 'a+')
        f.flush()
        #f.write(json.dumps(user_info,indent=4)+'\n') # with indent
        f.write(json.dumps(user_info) + '\n')
        f.close()
        # rate limit
        time.sleep(random.randint(3,4))
        cur += 1
        print cur, "users got"
    print "total users:", len(existing)

if __name__ == '__main__':
    print "Start At: ", datetime.datetime.now()
    randomly_select_users(2, True)
    print "End At: ", datetime.datetime.now()
