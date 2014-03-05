import praw
import time
from reddit_classes import User
from config import config

REDDIT_INTERFACE = None
USER_AGENT = config['user_agent'] 
REDDIT_USERNAME = config['reddit_username']
REDDIT_PASSWORD = config['reddit_password']

#
def parse_comment_text(text):
	string_list = text.split(" ")
	username, special = None, None
	if len(string_list) > 1:
		if ((string_list[0]).lower() == "/u/user_history_bot"):
			username = string_list[1]
			if len(string_list) > 2:
				special = string_list[2]
	return username, special

def process_message(username, special):
	if not (username is None):
		user = User(username, REDDIT_INTERFACE)
		if not (special is None):
			if (special == "submitted"):
				user.process_submitted()
			elif (special == "comments"):
				user.process_comments()
			else:
				user.process_comments()
				user.process_submitted()
		else:
			print("HERE")
			user.process_comments()
			comment_statistics = user.get_comment_statistics()
			return comment_statistics
			#user.process_submitted()
	return ""




# parse a message string and do appropriate
def launch_response(message):
	username, special = parse_comment_text(message.body)
	message.reply(process_message(username, special))
	message.mark_as_read()

def main():
	running = True
	while (running):
		try:
			unread_messages = REDDIT_INTERFACE.get_unread()
			for message in unread_messages:
				launch_response(message)
		except KeyboardInterrupt:
			running = False


if __name__ == '__main__':
	try:
		REDDIT_INTERFACE = praw.Reddit(user_agent = USER_AGENT)
		REDDIT_INTERFACE.login(REDDIT_USERNAME, REDDIT_PASSWORD) 

	except praw.errors.InvalidUser:
		print("remember to log error that user is invalid")	
	except praw.errors.InvalidUserPass:
		print("remember to log error that password is invalid")
	except:
		print()
	else:
		main()
