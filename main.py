from src import queue, client, logger, quote, config
import requests, sys

c = config.Config("config.json")

_logger = logger.Logger(c.log_file)
_quote = quote.Quotes(c.owner_name, _logger, c.header)
_queue = queue.Queue(_logger)
_client = client.Client(c.user_agent, c.summon_word, _queue, _quote, _logger)

_queue.connect(c.db_host, c.db_user, c.db_pw, c.db_name, c.db_table)
_client.connect(c.bot_name, c.password)
_quote.load(c.quote_file)

while True:
    try:
        _client.process_comments(c.subreddits,c.comment_limit)

    except KeyboardInterrupt:
        print "\nKeyboardInterrupt, saving state and exiting program...."
        _queue.close()
        _logger.close()
        sys.exit(0)

    except requests.exceptions.ConnectionError:
        _logger.write("Connection to Server lost!!!")
        _client.connect(c.bot_name, c.password)
