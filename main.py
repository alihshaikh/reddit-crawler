import pprint
import config
import praw
import json
import re
import os
import requests
from bs4 import BeautifulSoup

UserSubreddit = input("Please enter a subreddit that you would like to crawl then press enter,"
                      " omit 'r/'. (For example if you want to crawl r/ucr, enter 'ucr'): ")
print("Crawling:", UserSubreddit)

# Acquiring reddit app credentials
reddit = praw.Reddit(
    client_id=config.clientID,
    client_secret=config.clientSecret,
    user_agent=config.clientSecret,
)

subreddit = reddit.subreddit(UserSubreddit)

data_size = 0
file_num = 1


save_dir = 'data'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
    
if not os.path.exists("post_0.json"):
    open(f"data/post_0.json", 'a')
    
i = 0
while(os.path.exists(f'data/post_{file_num}.json')):
    i+=1
    file_num+=1

file_num -=1
 

for post in subreddit.top(limit=None):
    commentString = ""

    post.comments.replace_more(limit=None)
    for comment in post.comments.list():
        commentString = commentString + comment.body
    
    text = post.selftext
    urls = re.findall('(https?://[^\s]+)', text)
    urlTitles = []

    for url in urls: 
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            print(f'The page {url} could not be found: {e}')
            continue
        except requests.exceptions.HTTPError as e:
            print(f'The page {url} has an HTTP error: {e}')
        except Exception as e:
            print(f'The page {url} has an error: {e}')
        
        soup = BeautifulSoup(response.content, 'html.parser')
        if soup and soup.title and soup.title.string:
            urlTitles.append(soup.title.string)

    data = ({
        "Post ID": post.id,
        "Post Title": post.title,
        "Post Body": post.selftext,
        "Post Score": post.score,
        "Post Upvote Ratio": post.upvote_ratio,
        "Post Permalink": post.permalink,
        "Post Number Of Comments": post.num_comments,
        "Comments": commentString,
        "HTML Urls:": urls,
        "HTML Titles": urlTitles
    })

    json_data = json.dumps(data, indent=4)

    
    filename = f'data/post_{file_num}.json'
    if (os.path.getsize(filename) / (1024*1024)) > 10:
        file_num+=1
        data_size = 0
    filename = f'data/post_{file_num}.json'
    if file_num > 50:
        break
  
    with open(filename,  'a') as f:
        f.write(json_data + '\n')
        data_size += len(json_data)

print("JSONS POPULATED")
print("DONE")
