import user_crawler

def check_rate_limit_remaining_test():
    user_crawler.check_rate_limit_remaining()

def get_single_user_profile_by_id_test():
    id = 0
    user = user_crawler.get_single_user_profile_by_id(id)
    assert user == None

    id = 26807252
    login = 'landiveo'
    user = user_crawler.get_single_user_profile_by_id(id)
    assert user['login'] == login

def get_single_user_detailed_list_test():
    url = 'https://api.github.com/users/landiveo/repos'
    num = 2
    repos = user_crawler.get_single_user_detailed_list(url, num)
    assert len(repos) == num

def detect_suspicious_user_test():
    url = 'https://github.com/elloyb41'
    is_suspicious = user_crawler.detect_suspicious_user(url)
    assert is_suspicious == True

    url = 'https://github.com/landiveo'
    is_suspicious = user_crawler.detect_suspicious_user(url)
    assert is_suspicious == False

def get_single_user_info_test():
    id = 1
    user = user_crawler.get_single_user_profile_by_id(id)
    user_info = user_crawler.get_single_user_info(id, False)
    assert len(user_info['repos_list']) == user['public_repos']

def load_users_test():
    users = user_crawler.load_users('data')
    assert len(users) == 2

if __name__ == '__main__':
    check_rate_limit_remaining_test()
    get_single_user_profile_by_id_test()
    get_single_user_detailed_list_test()
    detect_suspicious_user_test()
    get_single_user_info_test()

