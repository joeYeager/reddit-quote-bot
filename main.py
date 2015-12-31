from src import queue, client


queue = queue.Queue("localhost", "forefathersbot","americaFuckYeah",
                        "forefathersbot", "queue")
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