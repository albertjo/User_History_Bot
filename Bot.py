import praw
import time
from reddit_classes import User
from config import config


USER_AGENT = config['user_agent'] 
REDDIT_USERNAME = config['reddit_username']
REDDIT_PASSWORD = config['reddit_password']


# parse a message string and do appropriate
def appropriate_response(r, str_message):
	return None

if __name__ == '__main__':
	try:
		r = praw.Reddit(user_agent = USER_AGENT)
		r.login(REDDIT_USERNAME, REDDIT_PASSWORD) 
		unread_messages= r.get_unread()
		
		running = True
		while (running):
			try:
				unread_messages = r.get_unread()
				for message in unread_messages:
					text = message.body
					#do something with text
					#message reply
					message.mark_as_read()
					print("found message")	
			except KeyboardInterrupt:
				running = False

	except praw.errors.InvalidUser:
		print("remember to log error that user is invalid")	
	except praw.errors.InvalidUserPass:
		print("remember to log error that password is invalid")
	except:
		print()
	
