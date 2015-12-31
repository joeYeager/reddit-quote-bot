import time, praw, requests, MySQLdb, random, sys
from datetime import date

class Logger:
    def __init__(self):
        try:
            log_file = open("log.txt", 'a')
        except IOError:
            print "Failed to open log file, closing program."
            sys.exit(0)

    # This function takes a message as arugment and then adds some
    # formatting and generates a log message.
    # The message takes the format "Sat, 03 May 2014 05:55:28 : Message"
    # Once the message is generated, and wrote, it is flushed to the log_file
    # This prevents having to wait for the log file to be closed for the messages to be 
    # written  
    def log_write(msg):
        timestamp = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        log_file.write( timestamp + ": " + msg + "\n")
        log_file.flush()