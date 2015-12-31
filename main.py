from src import queue, client, logger, quote

owner_name = "NeverForgetY2K"
username = ""
user_agent = "forefathersBot by u/NeverForgetY2K v0.2.0"
user_agent += " Comes when summoned and provides a quote from one of America\'s forefathers."
summon_string = "forefathersbot"


log = logger.Logger("logs/log.txt")
quo = quote.Quotes(owner_name, log)
q = queue.Queue(log)
q.connect("localhost","forefathersbot","password","forefathersbot", "queue")
c = client.Client(user_agent, summon_string, q, log)

# # Run the bot
# while True:
#     try:
#         process_comments()

#     except KeyboardInterrupt:
#         print "\nKeyboardInterrupt, saving state and exiting program...."
#         db.commit()
#         log_file.close()
#         sys.exit(0)

#     except requests.exceptions.ConnectionError:
#         log_write("Connection to Server lost!!!")
#         connect_to_server() 