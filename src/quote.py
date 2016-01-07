import random, sys, json

class Quotes:
    def __init__(self, owner, logger, header):
        self.owner = owner
        self.quote_list = []
        self.logger = logger
        self.header = header
    # the load_quotes function takes two arguments
    # The first argument is the file path of the file to load
    # The second arugment is the list in which you wish to store the lines
    # This fucntion will read in the file line by line 
    # and then store each line in the list as a quote. 
    # So the quotes should be seperated by a newline
    def load(self, quote_file):
        try:
            with open(quote_file) as quote_json:
                quotes = json.load(quote_json)

            self.quote_list = quotes.get("all", [])

        except IOError:
            self.logger.fail("Failed to open quotes file, closing program.")
            sys.exit(1)


    # Generates and returns the quote string used in the process queue function 
    def generate(self):
        quote = "##" + self.header + ":##\n\n >"

        randomNum = random.randint(0,len(self.quote_list)-1)
        raw_quote = self.quote_list[randomNum]
        quote += raw_quote.get("quote", None) + "\n"
        quote += '#####' + raw_quote.get("person", None) + '#####'

        quote += "\n\n*****"
        quote += "\n\n^^***If*** ^^***you*** ^^***would*** ^^***like*** ^^***to*** "
        quote += "^^***add*** ^^***a*** ^^***quote***, ^^***please*** ^^***contact*** "
        quote += "^^***my*** ^^***owner:*** ^^/u/" + self.owner
        return quote