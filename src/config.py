import json
class Config:
    def __init__(self,config_file):
        with open(config_file) as config_json:
            config = json.load(config_json)

        self.owner_name = config.get("owner_name", None)
        self.version = config.get("version", None)

        self.bot_name = config.get("bot_name", None)
        self.password = config.get("bot_pass", None)

        # A short description of what the bot does
        self.description = config.get("description", None)

        # The word you would like to cause the bot to trigger 
        self.summon_word = config.get("summon_word", None)

        # Relative file path to the logfile
        self.log_file = config.get("log_file", None)

        # Relative file path to the quote file
        self.quote_file = config.get("quote_file", None)

        # Comma sepearted list of the subreddits for the bot to operate in
        self.subreddits = config.get("subreddits", None)

        # How mant comments would you like the bot to stream at a time
        self.comment_limit = config.get("comment_limit", None)

        # Header string
        self.header = config.get("header", None)

        # Database settings
        db = config.get("db", None)
        self.db_host = db.get("host", None)
        self.db_user = db.get("username", None)
        self.db_pw = db.get("password", None)
        self.db_name = db.get("database", None)
        self.db_table = db.get("table", None)

        # The user agent string to be provided to reddit upon establishing a connection
        self.user_agent = "{} by u/{} v{} {}".format(bot_name, owner_name, version, description)