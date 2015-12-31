import time, praw, requests, sys

class Client:
    def __init__(self, useragent, summon_string, queue, logger):
        self.summon = summon_string
        self.reddit = praw.Reddit(useragent)
        self.processed_comments = []
        self.queue = queue
        self.logger = logger

    # Login to the server using the credentials provided in the praw.ini file
    # If the server is unable to be reached, the exception will be caught
    # and it will continue to reattempt connection every two seconds until
    # it is successful.
    def connect(self, username, password):
        try:
            self.logger.write("Attempting to connect to server.....")
            self.reddit.login(username, password)
            self.logger.write("Server Connection successful!")
            print "Connected successfully"
        except requests.exceptions.ConnectionError:
            print "Connection failed, retrying."
            self.logger.write("Server Connection Failed, retrying in 2 seconds...")
            time.sleep(2)

    # This function manages the list that holds the last 1000 ids of processed comments
    # If there are 1000 ids aready in the list, it will pop the first item and then append
    # the item that is passed to it.
    def mark_processed(self, commentID):
        if(len(self.processed_comments) > 999):
            self.processed_comments.pop(0)
        self.processed_comments.append(commentID)

    # Fetches comments and then parses them looking for summon commands
    def process_comments(self, subreddits, comment_limit):
        try:
            for comment in praw.helpers.comment_stream(reddit,'all',limit=comment_limit): # Parse all of the comments fetched
                if comment.id not in processed_comments: # The comment has not been processed yet
                    comment_words = comment.body.lower().split() #split the comment into lowercase words
                    if summon_word in comment_words: # Comment contains the summon command
                        self.reply(comment, "message")

        except praw.errors.RedirectException:
            self.logger.write("Unexpected redirect..")

    def reply(self, comment, message):
        try:
            mark_processed(comment.id)
            comment.reply(message)

        except praw.errors.RateLimitExceeded:
            self.logger.write("RateLimitExceeded, will attempt again later")
            self.queue.add(comment.id,comment.permalink)

    # Processes and replys to the comment queue
    # If a rate limit is hit, that comment is skipped and the next in queue is attempted
    # This happens because the rate limit might not apply to the subreddit that the next
    # comment it line is.
    # If the comment is successfully replied to, it is removed from all nessecary queues
    def process_queue(self):
        comment_queue = self.queue.get()
        if len(comment_queue) == 0:
            return  # Nothing to process, exit function

        for comment in comment_queue:
            submission = reddit.get_submission(comment[1])      

            try:
                queued_comment = submission.comments[0]
                queued_comment.reply(generate_quote(normal_quotes))

                print "\nReplying to: " , queued_comment.id
                self.queue.remove(comment[0])

            except praw.errors.RateLimitExceeded:
                self.logger.write("RateLimitExceeded, will attempt again later")

            except IndexError: # comment has been deleted
                dequeue(comment[0])
