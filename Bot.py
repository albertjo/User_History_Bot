import praw
import time
from reddit_classes import User
from config import config

REDDIT_INTERFACE = None
USER_AGENT = config['user_agent'] 
REDDIT_USERNAME = config['reddit_username']
REDDIT_PASSWORD = config['reddit_password']
BAN_MESSAGE = "User_History_Bot has been banned from this subreddit"

#
def parse_comment_text(text):
        string_list = text.split()
        username, special = None, None
        if len(string_list) > 1:
                if (((string_list[0]).lower()).strip() == "/u/user_history_bot"):
                        username = (string_list[1]).strip()
                        if len(string_list) > 2:
                                special = string_list[2]
        return username, special

def process_message(username, special):
        if not (username is None):
                try: 
                        user = User(username, REDDIT_INTERFACE)
                        user.process_comments()
                        comment_statistics = user.get_comment_statistics()
                        print("comment statistics successfully retrieved")
                        return comment_statistics
                except: 
                        print("remeber to log error that comment failed")
        print("Username is none")       
        return None

def reply(message, reply_object):
        if not (reply_object is None):
                try:
                    message.reply(reply_object)
                except:
                    REDDIT_INTERFACE.send_message(message.author, 
                            subject= BAN_MESSAGE, message = reply_object)

# parse a message string and do appropriate
def launch_response(message):
    username, special = parse_comment_text(message.body)
    reply_object = process_message(username, special)
    reply(message, reply_object)
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
                time.sleep(10)


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
