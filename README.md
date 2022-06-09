# SubredditScraper
A class to aid in scraping posts from a subreddit using the Reddit praw python package

# Usage

To start you'll first need to get setup with the reddit api get your reddit api credentials and store them in .ini file called praw.ini (there's a template file in this repo)

Once this is done you should be able to use the `get_posts` method to query the reddit api for the given parameters.

To get the first 20 hot posts on the front page (sub='all'),  and write them to file:

```python
SubredditScraper(sub='all',
                  search=None,
                  sort='hot',
                  lim=20,
                  mode='w',
                  get_comments=False,
                  replace_more_limit=10).get_posts()```
                  
                  

