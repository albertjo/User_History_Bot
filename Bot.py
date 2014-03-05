import praw
from reddit_classes import User


USER_AGENT = ("Reddit History Statistics")


if __name__ == '__main__':
	try:
		r = praw.Reddit(user_agent = USER_AGENT)	
	except:
		print("LOL")
	print("hello")
