#coding:utf8
import requests
import time
import random
import re
import json

# add token
headers = {"Authorization": "token ..."}

def check_rate_limit_remaining():
    url = "https://api.github.com"
    try:
        response = requests.head(url=url,headers=headers).headers
        print "X-RateLimit-Remaining:", response['X-RateLimit-Remaining']
        if response['X-RateLimit-Remaining'] == 0:
            print "exceeds X-RateLimit-Remaining, print wait 5 minutes"
            time.sleep(300)
    except requests.exceptions.ConnectionError:
        print "ConnectionError -- please wait 3 seconds"
        time.sleep(3)
    except requests.exceptions.Timeout:
        print "Timeout -- please wait 3 seconds"
        time.sleep(3)
    except:
        print "An Unknown Error during the rate limit check"

def get_single_user_profile_by_id(id):
    url = 'https://api.github.com/user/' + str(id)
    try:
        user_profile_response = requests.get(url, headers=headers)
        # if d exists, return user profile, else return None
        if user_profile_response.status_code == 200:
            return user_profile_response.json()
    except requests.exceptions.ConnectionError:
        print "ConnectionError -- please wait 3 seconds"
        time.sleep(3)
    except requests.exceptions.Timeout:
        print "Timeout -- please wait 3 seconds"
        time.sleep(3)
    except:
        print "An Unknown Error when getting a single user's profile by id"
        # in case rate limit
        check_rate_limit_remaining()

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
            # Array, each element is a dict
            detailed_list += requests.get(url, headers=headers, params=params).json()
        return detailed_list
    except requests.exceptions.ConnectionError:
        print "ConnectionError -- please wait 3 seconds"
        time.sleep(3)
    except requests.exceptions.Timeout:
        print "Timeout -- please wait 3 seconds"
        time.sleep(3)
    except:
        print "An Unknown Error when getting a single user's detailed list"
        # in case rate limit
        check_rate_limit_remaining()

def detect_suspicious_user(html_url):
    try:
        user_html_response = requests.get(html_url, headers=headers)
        # 404 - True, 200 - False, others - None
        if user_html_response.status_code == 404:
            return True
        elif user_html_response.status_code == 200:
            return False
    except requests.exceptions.ConnectionError:
        print "ConnectionError -- please wait 3 seconds"
        time.sleep(3)
    except requests.exceptions.Timeout:
        print "Timeout -- please wait 3 seconds"
        time.sleep(3)
    except:
        print "An Unknown Error when detecting suspicious user"
        # in case rate limit
        check_rate_limit_remaining()

def get_single_user_info(id, follow):
    user = get_single_user_profile_by_id(id)
    # if id doesn't exist, return None
    if not user:
        return
    # if id is suspicious, flag
    is_suspicious = detect_suspicious_user(user['html_url'])
    if is_suspicious == True:
        user['is_suspicious'] = True
    elif is_suspicious == False:
        user['is_suspicious'] = False
    else:
        return

    repos_list = get_single_user_detailed_list(user['repos_url'], user['public_repos'])
    if not repos_list:
        return
    user['repos_list'] = repos_list

    if follow:
        followers_list = get_single_user_detailed_list(user['followers_url'], user['followers'])
        following_list = get_single_user_detailed_list(user['following_url'], user['following'])
        if not (followers_list and following_list):
            return
        user['followers_list'] = followers_list
        user['following_list'] = following_list
    return user

def randomly_select_users(needed_users, follow=False, total_github_users=39610000):
    cur = 0
    with open('data','w') as f:
        while cur < needed_users:
            id = random.randint(1, total_github_users)
            user_info = get_single_user_info(id, follow)
            # in case: id doesn't exist or the information is not integrated
            if not user_info:
                continue
            # write file
            f.write(json.dumps(user_info)+'\n')
            cur += 1

def load_users(path):
    user = []
    with open(path, 'r') as f:
        for line in f.readlines():
            user.append(json.loads(line.strip()))
    return user

if __name__ == '__main__':
    randomly_select_users(2)
