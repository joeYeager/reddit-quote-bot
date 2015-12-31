import time, sys

class Logger:
    def __init__(self, filename):
        try:
            self.log_file = open(filename, 'a')
        except IOError:
            print "Failed to open log file, closing program."
            sys.exit(1)

    # This function takes a message as arugment and then adds some
    # formatting and generates a log message.
    # The message takes the format "Sat, 03 May 2014 05:55:28 : Message"
    # Once the message is generated, and wrote, it is flushed to the log_file
    # This prevents having to wait for the log file to be closed for the messages to be 
    # written  
    def write(self,msg):
        timestamp = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        self.log_file.write( timestamp + ": " + msg + "\n")
        self.log_file.flush()

    def fail(self, msg):
        self.write(msg)
        self.close()
        
    def close(self):
        self.log_file.close()
