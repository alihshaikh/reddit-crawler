import pprint
import config
import praw
import json
import re

# Entering the json files' name into a string
JsonDataPostFileName = "data_file.json"

# Creating an empty Python list
ListObj = []

# Clear the json file before adding data
with open(JsonDataPostFileName, "w") as write_file:
    json.dump(ListObj, write_file, indent=4)

# Acquiring reddit app credentials
reddit = praw.Reddit(
    client_id=config.clientID,
    client_secret=config.clientSecret,
    user_agent=config.clientSecret,
)

# Seeing if we are on a read only instance
print("Is Read Only?: ", reddit.read_only)
print("\n")

# Retrieving subreddit information
SubredditToCrawl = reddit.subreddit("ucr").hot(limit=8)

# Iterating through posts(AKA Submissions) of the subreddit above^^
for post in SubredditToCrawl:
    # Getting posts author
    redditor1 = post.author

    """ console debugging 
    print("Post Identification:", post.id) # Submission id, will need for part B, do need
    print("Post Title:", post.title) # Title of submission, do need
    print("Post Body:", post.selftext) # Body of submission, do need
    print("Post Score:", post.score) # Submission upvotes, don't need but can be useful for determining weights for part B
    print("Post Upvote Rate:", post.upvote_ratio) # Upvote to downvote ratio of submission, don't need but can be useful for determining weights for part B
    # print("Post Image URL:", post.url) # Images in post, don't need
    print("Post URL Permalink:", post.permalink) # Url of post, don't need
    print("Post Number of Comments:", post.num_comments) # Number of comments under submission, don't need but can be useful for determining weights for part B
    """
    # Create an empty string to use for concatenating comments of a post
    commentString = ""

    # Iterate through ALL comments of a post
    post.comments.replace_more(limit=None)
    for comment in post.comments.list():
        commentString = commentString + comment.body

    # finds all HTML urls that may be inside each reddit post. This is useful for part B of the project.
    text = post.selftext
    urls = re.findall('(https?://[^\s]+)', text)

    # Entering data of a reddit post to a list
    ListObj.append({
        "Post ID": post.id,
        "Post Author": redditor1.name,
        "Post Title": post.title,
        "Post Body": post.selftext,
        "Post Score": post.score,
        "Post Upvote Ratio": post.upvote_ratio,
        "Post Permalink": post.permalink,
        "Post Number Of Comments": post.num_comments,
        "Comments": commentString,
        "HTML Links": urls
    })

    # Entering data from list into json file
    with open(JsonDataPostFileName, "w") as write_file:
        json.dump(ListObj, write_file, indent=4)

    """ More console debugging
    print("\n-------------------------------------------------------------------------------------------------------\n")

    # Just looking at the attributes of a submission
    pprint.pprint(vars(post))
    """