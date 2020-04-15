import praw
from cogs import LoginsAndKeys as LaK

def main():
	"""Creates reddit object, then interate through list of subreddits, then iterate through the submissions on each subreddit.
	If the submission is not stickied, then add it to the empty list. Not all characters can be represented on a raspberry pi. 
	So I remove any character that has order higher than 65536"""
	reddit = praw.Reddit(client_id=LaK.api_keys["redditClient_id"],
	                     client_secret=LaK.api_keys["redditClient_secret"],
	                     username=LaK.logins["redditUsername"],
	                     password=LaK.logins["redditPasswd"],
	                     user_agent='my user agent',

	                     )
	reddit.read_only = True
	#write as many subreddits as you like, no more than 4 or the box becomes to big.
	subreddits = ["tifu", "lifeprotips", "boxoffice", "Coronavirus"]

	emptyList = []
	for subreddit in subreddits:
		for submission in reddit.subreddit(subreddit).hot(limit=3):
			if not submission.stickied:
				raw_post = str(submission.title) + " \u2191 " + str(submission.score) + "  r/" + str(subreddit)
				accepted = [raw_post[j] for j in range(len(raw_post)) if ord(raw_post[j]) < 65536]
				post=""
				for i in raw_post:
					post+= i 
				emptyList.append(post)
	return emptyList




