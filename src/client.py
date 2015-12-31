import time, praw, requests, MySQLdb, random, sys
from datetime import date

class Client:
    """docstring for Client"""
    def __init__(self, username, password, useragent, summon_string):
        # 'forefathersBot by u/NeverForgetY2K v0.2.0' 
                        # 'Comes when summoned and provides a quote from one of America\'s Forefathers.
        self.username = username
        self.password = password
        self.summon = summon_string
        self.reddit = praw.Reddit(useragent)
        self.processed_comments = []

    # Login to the server using the credentials provided in the praw.ini file
    # If the server is unable to be reached, the exception will be caught
    # and it will continue to reattempt connection every two seconds until
    # it is successful.
    def connect():
        try:
            log_write("Attempting to connect to server.....")
            self.reddit.login("username", "password")
            log_write("Server Connection successful!")
            print "Connected successfully"
        except requests.exceptions.ConnectionError:
            print "Connection failed, retrying."
            log_write("Server Connection Failed, retrying in 2 seconds!")
            time.sleep(2)

    # This function manages the list that holds the last 1000 ids of processed comments
    # If there are 1000 ids aready in the list, it will pop the first item and then append
    # the item that is passed to it.
    def mark_processed(commentID):
        if(len(processed_comments) > 999):
            processed_comments.pop(0)
        processed_comments.append(commentID)

    # Fetches comments and then parses them looking for summon commands
    def process_comments():
        try:
            for comment in praw.helpers.comment_stream(reddit,'all',limit=1000): # Parse all of the comments fetched
                add_to_queue = False
                if comment.id not in processed_comments: # The comment has not been processed yet
                    comment_words = comment.body.lower().split() #split the comment into lowercase words
                    for word in comment_words:
                        if summon_word in word: # Comment contains the summon command
                            add_to_queue = True
                            break
                    try:
                        mark_processed(comment.id)
                        if add_to_queue:
                            comment.reply(generate_quote(normal_quotes))
                            print "\nReplying to: " , comment.id
                        
                    except praw.errors.RateLimitExceeded:
                        log_write("RateLimitExceeded, will attempt again later")
                        if add_to_queue:
                            enqueue(comment.id,comment.permalink,"Normal")

        except praw.errors.RedirectException:
            log_write("Unexpected redirect, attempting to load comments again")

    # Processes and replys to the comment queue
    # If a rate limit is hit, that comment is skipped and the next in queue is attempted
    # This happens because the rate limit might not apply to the subreddit that the next
    # comment it line is.
    # If the comment is successfully replied to, it is removed from all nessecary queues
    def process_queue():
        comment_queue = fetch_table('queue')
        if len(comment_queue) == 0:
            return  # Nothing to process, exit function

        for comment in comment_queue:
            submission = reddit.get_submission(comment[1])      

            try:
                queued_comment = submission.comments[0]
                queued_comment.reply(generate_quote(normal_quotes))

                print "\nReplying to: " , queued_comment.id
                dequeue(comment[0])

            except praw.errors.RateLimitExceeded:
                log_write("RateLimitExceeded, will attempt again later")

            except IndexError: # comment has been deleted
                dequeue(comment[0])
