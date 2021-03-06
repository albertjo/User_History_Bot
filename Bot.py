import praw
import time
import re
from config import config

REDDIT_INTERFACE = None
USER_AGENT = config['user_agent'] 
REDDIT_USERNAME = config['reddit_username']
REDDIT_PASSWORD = config['reddit_password']
BAN_MESSAGE = "User_History_Bot has been banned from this subreddit"
MAX = 90

def does_user_exist(user):
    try:
        for comment in user.get_comments(limit=1):
            pass
        return True
    except praw.errors.NotFound:
        return False


def get_comment_history(user):
    subreddits = [str(comment.subreddit.display_name) for comment in user.get_comments(limit=None)]
    str_message = "Data for the last {} comments for /u/{} (MAX 1000)\n\n{:20}|{:20}|{:20}\n".format(len(subreddits),str(user),
            "Subreddit","Posts","Percentage")
    str_message += (("-"*20 + "|")*2 + "-"*20)+"\n"
    subreddit_count = dict((subreddit, subreddits.count(subreddit)) for subreddit in subreddits)
    start = 0
    for subreddit in sorted(subreddit_count, key=lambda k:subreddit_count[k],reverse=True):
        count = subreddit_count[subreddit]
        percentage = "{0:.2f}%".format(float(100*count)/len(subreddits))
        str_message += "/r/{:20}|{:20}|{:20}\n".format(subreddit, count , percentage)
        start += 1
        if start == MAX:
            break
    str_message += "\n\n To summon this bot, the first line of your comment should be: /u/{} @USERNAME".format(REDDIT_USERNAME)
    return str_message


def generate_response(username):
    user = REDDIT_INTERFACE.get_redditor(username)
    if does_user_exist(user):
        return get_comment_history(user) 
    else:
        return '/u/{} is an invalid user!'.format(username)


def respond(msg_to_respond, response):
    if isinstance(msg_to_respond,praw.objects.Voteable):
        msg_to_respond.upvote()
    try:
        msg_to_respond.reply(response)
    except:
        REDDIT_INTERFACE.send_message(msg_to_respond.author,
                subject=BAN_MESSAGE, message=response)
    

def run_bot():
    unread_messages = REDDIT_INTERFACE.get_unread()
    for message in unread_messages:
        print "Recieved Message: ", str(message)
        usernames = re.findall('@[-\w]+', str(message).lower())
        for username in usernames:
            print username
            response = generate_response(username[1:])
            respond(message, response)
        print 'success'
        message.mark_as_read()


def main():
    running = True
    while (running):
        run_bot()       
        time.sleep(10)


if __name__ == '__main__':
    try:
        REDDIT_INTERFACE = praw.Reddit(user_agent = USER_AGENT)
        REDDIT_INTERFACE.login(REDDIT_USERNAME, REDDIT_PASSWORD) 
    except praw.errors.InvalidUser:
        print("remember to log error that user is invalid")     
    except praw.errors.InvalidUserPass:
        print("remember to log error that password is invalid")
    main()
