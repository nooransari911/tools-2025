import webbrowser 
import praw

reddit = praw.Reddit(
    client_id = "",
    client_secret = "",
    password = "",
    user_agent = "",
    username = "",
)
post = praw.models.Submission (reddit=reddit, url="https://www.reddit.com/r/commandline/comments/13uz3z/how_can_i_download_a_page_of_reddit_and_extract/")
print (post.url)
