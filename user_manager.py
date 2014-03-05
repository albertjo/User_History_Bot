from reddit_classes import User 


def main():
    username = input("Enter username: ")
    user = User(username)
    user.process_comments()
    user.process_submitted()


if __name__ == '__main__':
    main()
