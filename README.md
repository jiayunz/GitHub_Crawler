# Github_Crawler

A crawler used to retrieve the information of Github users using Github official APIs.

## Data

The crawler will collect the following information:

* The basic information of the user by [User API](https://api.github.com/user/26807252)
* The detailed follower list of the user by [Follower API](https://api.github.com/users/landiveo/followers)
* The detailed following list of the user by [Following API](https://api.github.com/users/landiveo/following)
* The repository list of the user by [Repository API](https://api.github.com/users/landiveo/repos)
* The commit logs of the user by [GitHub Search API](https://api.github.com/search/commit)

## Before Installation

we have tested our crawler on CentOS 7.3. Please make sure that you have installed Python2.7 and Requests (`pip install requests`).

## Usage:

* Change directory to [crawler](https://github.com/landiveo/Github_Crawler/tree/master/crawler)

* Manually fill in the authorization token in [config.py](https://github.com/landiveo/Github_Crawler/blob/master/crawler/config.py).

* Run crawler using bash command: `python main.py TOTAL_USER OUTPUT_PATH`

  `TOTAL_USER` the total number of users you want to retrieve
  
  `OUTPUT_PATH` the path where you want to store the data

  **Example:** `python main.py 10 data.txt`

## License

See the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).
