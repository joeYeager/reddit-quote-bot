from src import queue, client, logger, quote
import requests, sys

# The owner name for the bot, displayed in the bots comment and provided in the user_agent
owner_name = "ProudBotOwner"

# The version number of the bot
version = "1.0.0"

# The bot's username and password combination
bot_name = "MyBotsUserName"
password = "password"

# A short description of what the bot does
description = "A short description of what my bot does"

# The word you would like to cause the bot to trigger 
summon_word = "word_in_comment_that_summons_bot"

# Relative file path to the logfile
log_file = "logs/log.txt"

# Relative file path to the quote file
quote_file = "quotes/quotes.txt"

# Comma sepearted list of the subreddits for the bot to operate in
subreddits = "all"

# How mant comments would you like the bot to stream at a time
comment_limit = 1000

# The user agent string to be provided to reddit upon establishing a connection
user_agent = "{} by u/{} v{} {}".format(bot_name, owner_name, version, description)

# Header string
header = "Comment header"

# Database settings
db_host = "localhost"
db_user = "database_username"
db_pw = "password"
db_name = "database_name"
db_table = "queue" # Do not change this if you built the table using the provided schema

_logger = logger.Logger(log_file)
_quote = quote.Quotes(owner_name, _logger, header)
_queue = queue.Queue(_logger)
_client = client.Client(user_agent, summon_word, _queue, _quote, _logger)

_queue.connect(db_host, db_user, db_pw, db_name, db_table)
_client.connect(bot_name, password)
_quote.load(quote_file)

while True:
    try:
        _client.process_comments(subreddits,comment_limit)

    except KeyboardInterrupt:
        print "\nKeyboardInterrupt, saving state and exiting program...."
        _queue.close()
        _logger.close()
        sys.exit(0)

    except requests.exceptions.ConnectionError:
        _logger.write("Connection to Server lost!!!")
        _client.connect(bot_name, password)