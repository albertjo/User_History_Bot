import praw
from reddit_classes import User
from config import config


USER_AGENT = config['user_agent'] 
REDDIT_USERNAME = config['reddit_username']
REDDIT_PASSWORD = config['reddit_password']

if __name__ == '__main__':
	try:
		r = praw.Reddit(user_agent = USER_AGENT)
		r.login(REDDIT_USERNAME, REDDIT_PASSWORD) 
	except praw.errors.InvalidUser:
		print()
	except praw.errors.InvalidUserPass:
		print()
	except:
		print()
	
