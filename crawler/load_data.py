# coding:utf8
import json
import random
import re

def load_users(path):
    users = []
    try:
        with open(path, 'r') as f:
            for line in f.readlines():
                users.append(json.loads(line.strip()))
    except IOError, err:
        print err
        user = []
    return users

def load_existing(path):
    existing = []
    try:
        with open(path, 'r') as f:
            for line in f.readlines():
                user = json.loads(line.strip())
                existing.append(user['id'])
    except IOError, err:
        print err
        existing = []
    return existing

def get_samples(path, n):
    users = []
    try:
        with open(path, 'r') as f:
            for line in f.readlines():
                users.append(json.loads(line.strip()))
    except IOError, err:
        print err
    for i in range(n):
        for key in users[i].keys():
            if re.match(r'.*_?url$', key):
                users[i].pop(key)

        with open('samples', 'a') as f:
            f.write(json.dumps(users[i])+'\n')

def data_processing(path):
    users = []
    with open(path, 'r') as f:
        for line in f.readlines():
            users.append(json.loads(line.strip()))
    for user in users:
        for user_key in user.keys():
            if re.match(r'.*_?url$', user_key):
                user.pop(user_key)
            # get repos_list/followers_list/following_list
            if re.match(r'.*_list$', user_key):
                for each_in_list in user[user_key]:
                    for key_of_each_in_list in each_in_list.keys():
                        # remove url in each repos_list/followers_list/following_list
                        if re.match(r'.*_?url$', key_of_each_in_list):
                            each_in_list.pop(key_of_each_in_list)
                        # remove owner info
                        if key_of_each_in_list == 'owner':
                            each_in_list.pop(key_of_each_in_list)

        with open('data_no_url', 'a') as f:
            f.write(json.dumps(user) + '\n')


if __name__ == '__main__':
    data_processing('data')

