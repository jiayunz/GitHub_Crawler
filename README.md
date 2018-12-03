# GitHub Crawler

A crawler used to retrieve the information of GitHub users using GitHub official APIs.

## Installation

We have tested our crawler on macOS High Sierra 10.13.1. Please make sure that you have installed Python 3.6.7 and Requests (`pip install requests`).

## Usage

* Change directory to [crawler](https://github.com/landiveo/GitHub_Crawler/tree/master/crawler)

* Manually fill in the [authorization token](https://developer.github.com/v3/#authentication) in [config.py](https://github.com/landiveo/GitHub_Crawler/blob/master/crawler/config.py)

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

Each user entry is stored in JSON format.

## License

See the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).
