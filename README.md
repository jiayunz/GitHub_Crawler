# Github_Crawler

A crawler used to retrieve the information of Github users using Github official APIs.

## Before Installation

we have tested our crawler on CentOS 7.3. Please make sure that you have installed Python2.7 and Requests (`pip install requests`).

## Usage:

* Change directory to crawler

* Manually fill in the authorization token in config.py.

* Run crawler using bash command:`python main.py TOTAL_USER OUTPUT_PATH`

  `TOTAL_USER` the total number of users you want to retrieve
  
  `OUTPUT_PATH` the path where you want to store the data.

  **Example:** `python main.py 10 data.txt`

## License

See the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).
