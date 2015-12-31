import random, sys

class Quotes:
    def __init__(self, owner, logger):
        self.owner = owner
        self.quote_list = []
        self.logger = logger
    # the load_quotes function takes two arguments
    # The first argument is the file path of the file to load
    # The second arugment is the list in which you wish to store the lines
    # This fucntion will read in the file line by line 
    # and then store each line in the list as a quote. 
    # So the quotes should be seperated by a newline
    def load(self, fileToLoad):
        try:
            print("Loading: " + fileToLoad)
            self.quote_file = open(fileToLoad, 'r')
            for i in self.quote_file:
                self.quote_list.append(i)
            self.quote_file.close()
        except IOError:
            self.logger.fail("Failed to open quotes file, closing program.")
            sys.exit(1)


    # Generates and returns the quote string used in the process queue function 
    def generate(self, header):
        quote = "##" + header + ":##\n\n >"

        randomNum = random.randint(0,len(quote_list)-1)
        to_split = str(self.quote_list[randomNum])
        split_str = to_split.split("@")
        quote += split_str[0] + "\n"
        quote += '#####' + splitStr[1] + '#####'

        quote += "\n\n*****"
        quote += "\n\n^^***If*** ^^***you*** ^^***would*** ^^***like*** ^^***to*** "
        quote += "^^***add*** ^^***a*** ^^***quote***, ^^***please*** ^^***contact*** "
        quote += "^^***my*** ^^***owner:*** ^^/u/" + self.owner
        return quote