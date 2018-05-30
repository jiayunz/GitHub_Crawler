#coding:utf8
import requests
import time
import datetime
import random
import re
import json
import sys
import config

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
        print "RateLimit-Remaining: ", remaining

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
def get_single_user_detailed_list(url, num):
    #remove the suffix like: {/owner}{/repo}
    url = re.sub(r'{.*}$', "", url)
    page = 0
    detailed_list = []
    # detailed list should be integrated
    try:
        while len(detailed_list) < num:
            page += 1
            params = {"per_page": 100, "page": page}
            # in case rate limit
            check_rate_limit_remaining()
            # Array, each element is a dict
            detailed_list += requests.get(url, headers=headers, params=params).json()
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

def detect_suspicious_user(html_url):
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

    repos_list = get_single_user_detailed_list(user['repos_url'], user['public_repos'])
    if repos_list == None:
        return
    user['repos_list'] = repos_list

    if follow:
        followers_list = get_single_user_detailed_list(user['followers_url'], user['followers'])
        following_list = get_single_user_detailed_list(user['following_url'], user['following'])
        if followers_list == None or following_list == None:
            return
        user['followers_list'] = followers_list
        user['following_list'] = following_list
    return user

def randomly_select_users(needed_users, follow=False, start_id=1, end_id=39610000):
    cur = 0
    existing = []
    while cur < needed_users:
        id = random.randint(start_id, end_id)
        if id in existing:
            continue
        existing.append(id)
        user_info = get_single_user_info(id, follow)
        # in case: id doesn't exist or the information is not integrated
        if not user_info:
            continue
        # write file
        with open('data', 'a+') as f:
            # with indent
            #f.write(json.dumps(user_info,indent=4)+'\n')
            f.write(json.dumps(user_info) + '\n')
        # rate limit
        time.sleep(random.randint(3,4))
        cur += 1
        print cur, " users got"

def load_users(path):
    user = []
    with open(path, 'r') as f:
        for line in f.readlines():
            user.append(json.loads(line.strip()))
    return user

if __name__ == '__main__':
    print "Start At: ", datetime.datetime.now()
    randomly_select_users(10000, True)
    print "End At: ", datetime.datetime.now()
