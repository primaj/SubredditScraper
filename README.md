# SubredditScraper
A class to aid in scraping posts from a subreddit using the Reddit praw python package

# Usage

To get the first 20 hot posts on the front page (sub='all'),  and write them to file:

`SubredditScraper(sub='all',
                  search=None,
                  sort='hot',
                  lim=20,
                  mode='w',
                  get_comments=False,
                  replace_more_limit=10).get_posts()`
