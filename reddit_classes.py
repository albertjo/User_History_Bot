import praw

MAX_SUBS = 80

class User:
        def __init__(self, username, r):
                self.r = r 
                self.user = (self.r).get_redditor(username)
                self.username = username
                self.submitted = User_Post()
                self.comments = User_Post()

        ## Following are Getters ##
        def get_username(self):
                return self.username

        def get_submitted(self):
                return self.submitted

        def get_comments(self):
                return self.comments

        def get_number_of_comments(self):
                return (self.comments).get_count()

        def get_number_of_submitted(self):
                return (self.submitted).get_count()

        ## Following are Setters ##
        def set_submitted(self, new_submitted):
                self.submitted = new_submitted

        def set_commented(self, new_comments):
                self.commented = new_comments

        ## Insertion Methods ##
        def insert_comment(self, comment):
                (self.comments).insert(comment)
        
        def insert_submitted(self, submitted):
                (self.submitted).insert(submitted)
        
        def get_comments_by_subreddit(self, subreddit):
                return (self.comments).get_subreddit_posts(subreddit)

        def get_submitted_by_subreddit(self, subreddit):
                return (self.submitted).get_subreddit_posts(subreddit)

        # get all commenets from the user
        def process_comments(self):
                comment_iter = (self.user).get_comments(limit=None)
                for comment in comment_iter:
                        (self.comments).insert(comment)

        # get all submissions from the user
        def process_submitted(self):
                submitted_iter = (self.user).get_submitted(limit=None)
                for submitted in submitted_iter:
                        (self.submitted).insert(submitted)

        # get a string of all of the user's comment statistics
        def get_comment_statistics(self):
                str_message = "Data for the last {} comments (MAX 1000)\n\n{:20}|{:20}|{:20}\n".format(
                        self.get_number_of_comments(), "Subreddit", "Posts" ,"Percentage")
                str_message += (("-"*20 + "|")*2 + "-"*20)+"\n"
                comment_dict = self.get_comments().get_posts()
                local_c = 0     #This is a counter to make sure no more than MAX_SUBS subreddits are accounted for

                for subreddit in sorted(comment_dict, key=lambda k: len(comment_dict[k]), reverse=True): 
                        num_posts = len(comment_dict[subreddit])
                        percentage = "{0:.2f}%".format(100 * num_posts/self.get_number_of_comments())
                        str_message += "/r/{:20}|{:20}|{:20}\n".format(subreddit, num_posts, percentage)
                        local_c+=1
                        if local_c == MAX_SUBS:
                            break
                
                str_message += "\n\n To summon this bot, the first line of your comment should be: /u/user_history_bot USERNAME"
                return str_message


class User_Post:
        def __init__(self):
                self.post_dict = {}     
                self.count = 0
        
        # This function takes a praw Comment object
        # and inserts it into the dictionary of comments,
        # comment_dict.
        def insert(self, post):
                subreddit = post.subreddit.display_name
                if subreddit not in self.post_dict:
                        self.post_dict[subreddit] = []
                self.post_dict[subreddit].append(post)
                self.count += 1

        # This function returns the total number of comments
        def get_count(self):
                return self.count
        
        # Get the Post Dictionary
        def get_posts(self):
                return self.post_dict

        # This function takes a subreddit (str) and returns
        # a list of comments posted by the user. If subreddit
        # is not found, it returns None.
        def get_subreddit_posts(self, subreddit):
                if subreddit in self.post_dict:
                        return self.post_dict[subreddit]
                return None


