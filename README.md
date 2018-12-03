# Github_Crawler

A crawler used to retrieve the information of Github users using Github official APIs.

## Installation

we have tested our crawler on CentOS 7.3. Please make sure that you have installed Python2.7 and Requests (`pip install requests`).

## Usage

* Change directory to [crawler](https://github.com/landiveo/Github_Crawler/tree/master/crawler)

* Manually fill in the [authorization token](https://developer.github.com/v3/#authentication) in [config.py](https://github.com/landiveo/Github_Crawler/blob/master/crawler/config.py)

* Run crawler using bash command: `python main.py TOTAL_USER OUTPUT_PATH`

  `TOTAL_USER` is the total number of users you want to retrieve
  
  `OUTPUT_PATH` is the path where you want to store the data

  **Example:** `python main.py 10 data.txt`

## Data

The crawler will collect the following information:

* The basic information of the user by User API (https://api.github.com/user/:id)
* The detailed follower list of the user by [Follower API](https://developer.github.com/v3/users/followers/#list-followers-of-a-user)
* The detailed following list of the user by [Following API](https://developer.github.com/v3/users/followers/#list-users-followed-by-another-user)
* The repository list of the user by [Repository API](https://developer.github.com/v3/repos/#list-user-repositories)
* The commit logs of the user by [GitHub Search API](https://developer.github.com/v3/search/#search-commits)

## License

See the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).
