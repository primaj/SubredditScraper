from os.path import isfile
import praw
import pandas as pd
from time import sleep

# Get credentials from DEFAULT instance in praw.ini
reddit = praw.Reddit()


class SubredditScraper:
    def __init__(self,
                 sub, search, sort='new',
                 lim=900, mode='w',
                 get_comments=False, replace_more_limit=32):

        self.sub = sub
        self.search = search
        self.sort = sort
        self.lim = lim
        self.mode = mode
        self.get_comments = get_comments
        self.replace_more_limit = replace_more_limit

        print(f'SubredditScraper instance created with values:\n\t'
              f'sub = {sub}\n\t'
              f'sort = {sort}\n\t'
              f'lim = {lim}\n\t'
              f'mode = {mode}\n\t'
              f'search = {search}\n\t'
              f'get_comments = {get_comments}\n\t'
              f'replace_more_limit = {replace_more_limit}')

    def set_search(self):
        subreddit = reddit.subreddit(self.sub)
        init_sort = self.sort
        self.sort = self.sort if self.sort in ['new', 'top', 'hot'] else 'hot'
        if init_sort != self.sort:
            print('Sort method was not recognised, defaulting to hot.')

        # If we have a search term, use it
        if self.search is not None:
            return self.sort, subreddit.search(self.search, sort=self.sort,
                                               syntax='lucene', limit=self.lim)
        # Otherwise just use the specified sort mode
        else:
            # extract sort method from the subreddit class using the input sort string
            sort_mode = getattr(subreddit, self.sort)
            return self.sort, sort_mode(limit=self.lim)

    def get_posts(self):
        """Get unique posts from a specified subreddit."""
        # Initialise empty dictionary
        sub_dict = {'body': [], 'title': [], 'id': [], 'sorted_by': [],
                    'num_comments': [], 'score': [], 'ups': [], 'downs': [],
                    'upvote_ratio': [], 'created_utc': [], 'author': [], 'link_flair_text': []}

        if self.get_comments:
            sub_dict['comments'] = []

        csv = f'new_{self.sub}_posts.csv'

        # Attempt to specify a sorting method
        sort, subreddit = self.set_search()

        # Set csv_loaded to True if csv exists since you can't evaluate the
        # truth value of a DataFrame.
        df, csv_loaded = (pd.read_csv(csv), 1) if isfile(csv) else ('', 0)
        csv_loaded = 0 if self.mode == 'return' else csv_loaded

        print(f'csv = {csv}')
        print(f'After set_sort(), sort = {sort} and sub = {self.sub}')
        print(f'csv_loaded = {csv_loaded}')

        print(f'Collecting information from r/{self.sub}.')
        for post in subreddit:

            # Check if post.id is in df and set to True if df is empty.
            # This way new posts are still added to dictionary when df = ''
            unique_id = post.id not in tuple(df.id) if csv_loaded else True

            # Save any unique, non-stickied posts with descriptions to sub_dict.
            if unique_id:
                sub_dict['body'].append(post.selftext)
                sub_dict['title'].append(post.title)
                sub_dict['id'].append(post.id)
                sub_dict['sorted_by'].append(sort)
                sub_dict['num_comments'].append(post.num_comments)
                sub_dict['score'].append(post.score)
                sub_dict['ups'].append(post.ups)
                sub_dict['downs'].append(post.downs)
                sub_dict['upvote_ratio'].append(post.upvote_ratio)
                sub_dict['created_utc'].append(post.created_utc)
                sub_dict['author'].append(post.author)
                sub_dict['link_flair_text'].append(post.link_flair_text)

                if self.get_comments:
                    # Set the replace more limit
                    post.comments.replace_more(limit=self.replace_more_limit)
                    # Combine post comments, separated by full stops
                    sub_dict['comments'].append('.'.join([comment.body
                                                          for comment
                                                          in post.comments.list()
                                                          ]))

            # sleepy
            sleep(0.1)

        new_df = pd.DataFrame(sub_dict)

        # If in write mode, add new_df to df, if df exists, then save it to a csv
        if 'DataFrame' in str(type(df)) and self.mode == 'w':
            # noinspection PyTypeChecker
            pd.concat([df, new_df], axis=0, sort=0).to_csv(csv, index=False)
            print(f'{len(new_df)} new posts collected and added to {csv}')
        elif self.mode == 'w':
            new_df.to_csv(csv, index=False)
            print(f'{len(new_df)} posts collected and saved to {csv}')
        elif self.mode == 'return':
            # Return the dataframe
            print(f'{len(new_df)} posts collected, returning')
            return new_df
        else:
            print(f'{len(new_df)} posts were collected but they were not '
                  f'added to {csv} because mode was set to "{self.mode}"')


if __name__ == '__main__':
    SubredditScraper(sub='all',
                     search=None,
                     sort='hot',
                     lim=20,
                     mode='w',
                     get_comments=False,
                     replace_more_limit=10).get_posts()
