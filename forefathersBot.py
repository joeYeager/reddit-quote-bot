#!/usr/bin/python
# ForefathersBot is a reddit bot that parses reddit comments and looks for the
# string "forefathersBot" the bot will then generate a comment

# Import all nessecary libs
import time, praw, requests, MySQLdb, random, sys
from datetime import date

# Set up the database connection
try:
	db = MySQLdb.connect(host="localhost",
			     user="forefathersbot",
			     passwd="password",
			     db="forefathersbot")

except:
	print "Failed to connect to database, exiting"
	sys.exit(0)

########## Set up praw and declare global vars ##########
reddit = praw.Reddit('forefathersBot by u/NeverForgetY2K v0.2.0' 
				'Comes when summoned and provides a quote from one of Americas Forefathers.')

normalQuotes, processedComments = [], []
summonWord = 'forefathersbot'
cur = db.cursor()

# Try to open the log file, if it does not exist, it will be created
# If an IOError is thrown the program will cease execution
try:
	logFile = open("log.txt", 'a')
except IOError:
	print "Failed to open log file, closing program."
	sys.exit(0)


########## Function Declarations ##########

# This function takes a message as arugment and then adds some
# formatting and generates a log message.
# The message takes the format "Sat, 03 May 2014 05:55:28 : Message"
# Once the message is generated, and wrote, it is flushed to the logFile
# This prevents having to wait for the log file to be closed for the messages to be 
# written  
def logWrite(msg):
	timestamp = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
	logFile.write( timestamp + ": " + msg + "\n")
	logFile.flush()

# the loadQuotes function takes two arguments
# The first argument is the file path of the file to load
# The second arugment is the list in which you wish to store the lines
# This fucntion will read in the file line by line 
# and then store each line in the list as a quote. 
# So the quotes should be seperated by a newline
def loadQuotes(fileToLoad, fileContainer):
	try:
		print("Loading: " + fileToLoad)
		quoteFile = open(fileToLoad, 'r')
		for i in quoteFile:
			fileContainer.append(i)
		quoteFile.close()
	except IOError:
		logWrite("Failed to open quotes file, closing program.")
		logFile.close()
		sys.exit(0)

# Login to the server using the credentials provided in the praw.ini file
# If the server is unable to be reached, the exception will be caught
# and it will continue to reattempt connection every two seconds until
# it is successful.
def connectToServer():
	while True:
		try:
			logWrite("Attempting to connect to server.....")
			reddit.login("username", "password")
			logWrite("Server Connection successful!")
			print "Connected successfully"
			break
		except requests.exceptions.ConnectionError:
			print "Connection failed, retrying."
			logWrite("Server Connection Failed, retrying in 2 seconds!")
			time.sleep(2)

# Database functions
def runQuery(query):
	cur.execute(query)
	db.commit()

def enqueue(idNum, url, commentType):
	query = "INSERT INTO queue SET ID=\'"+ str(db.escape_string(idNum)) + "\', URL=\'" 
	query += url + "\', type=\'" + commentType + "\';"
	runQuery(query)

def dequeue(idNum):
	query = "DELETE FROM queue WHERE ID=\'"+ str(db.escape_string(idNum))+ "\';"
	runQuery(query)

def fetchTable(tableName):
	query="SELECT * FROM " + tableName +";" 
	cur.execute(query)
	return cur.fetchall()

# This function manages the list that holds the last 1000 ids of processed comments
# If there are 1000 ids aready in the list, it will pop the first item and then append
# the item that is passed to it.
def markAsProcessed(commentID):
	if(len(processedComments) > 999):
		processedComments.pop(0)
	processedComments.append(commentID)

# Generates and returns the quote string used in the process queue function 
def generateQuote(quoteList):
	quote = "##Forefathers quote:##\n\n >"

	randomNum = random.randint(0,len(quoteList)-1)
	toSplit = str(quoteList[randomNum])
	splitStr = toSplit.split("@")
	print(splitStr)
	quote += splitStr[0] + "\n"
	quote += '#####' + splitStr[1] + '#####'

	quote += "\n\n*****"
	quote += "\n\n^^***If*** ^^***you*** ^^***would*** ^^***like*** ^^***to*** "
	quote += "^^***add*** ^^***a*** ^^***quote***, ^^***please*** ^^***contact*** "
	quote += "^^***my*** ^^***owner:*** ^^/u/NeverForgetY2K"
	return quote


# Processes and replys to the comment queue
# If a rate limit is hit, that comment is skipped and the next in queue is attempted
# This happens because the rate limit might not apply to the subreddit that the next
# comment it line is.
# If the comment is successfully replied to, it is removed from all nessecary queues
def processQueue():
	commentQueue = fetchTable('queue')
	if len(commentQueue) == 0:
		return  # Nothing to process, exit function

	for comment in commentQueue:
		submission = reddit.get_submission(comment[1])		

		try:
			queuedComment = submission.comments[0]
			queuedComment.reply(generateQuote(normalQuotes))

			print "\nReplying to: " , queuedComment.id
			dequeue(comment[0])

		except praw.errors.RateLimitExceeded:
			logWrite("RateLimitExceeded, will attempt again later")

		except IndexError: # comment has been deleted
			dequeue(comment[0])

# Fetches comments and then parses them looking for summon commands
def fetchAndParseComments():
	try:
		for comment in praw.helpers.comment_stream(reddit,'all',limit=1000): # Parse all of the comments fetched
			addToQueue = False
			if comment.id not in processedComments: # The comment has not been processed yet
				commentWords = comment.body.lower().split() #split the comment into lowercase words
				for word in commentWords:
					if summonWord in word: # Comment contains the summon command
						addToQueue = True
						break
				try:
					markAsProcessed(comment.id)
					if addToQueue:
						comment.reply(generateQuote(normalQuotes))
						print "\nReplying to: " , comment.id
					
				except praw.errors.RateLimitExceeded:
					logWrite("RateLimitExceeded, will attempt again later")
					if addToQueue:
						enqueue(comment.id,comment.permalink,"Normal")

	except praw.errors.RedirectException:
		logWrite("Unexpected redirect, attempting to load comments again")

# Setup the bot
loadQuotes("quotes.txt",normalQuotes)
connectToServer()

# Run the bot
while True:
	try:
		fetchAndParseComments()

	except KeyboardInterrupt:
		print "\nKeyboardInterrupt, saving state and exiting program...."
		db.commit()
		logFile.close()
		sys.exit(0)

	except requests.exceptions.ConnectionError:
		logWrite("Connection to Server lost!!!")
		connectToServer() 