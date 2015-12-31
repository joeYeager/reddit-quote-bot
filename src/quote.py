class Quote:
    def __init__(self):
        pass
    
    # the load_quotes function takes two arguments
    # The first argument is the file path of the file to load
    # The second arugment is the list in which you wish to store the lines
    # This fucntion will read in the file line by line 
    # and then store each line in the list as a quote. 
    # So the quotes should be seperated by a newline
    def load_quotes(fileToLoad, fileContainer):
        try:
            print("Loading: " + fileToLoad)
            quote_file = open(fileToLoad, 'r')
            for i in quote_file:
                fileContainer.append(i)
            quote_file.close()
        except IOError:
            log_write("Failed to open quotes file, closing program.")
            log_file.close()
            sys.exit(0)


    # Generates and returns the quote string used in the process queue function 
    def generate_quote(quote_list):
        quote = "##Forefathers quote:##\n\n >"

        randomNum = random.randint(0,len(quote_list)-1)
        to_split = str(quote_list[randomNum])
        split_str = to_split.split("@")
        quote += split_str[0] + "\n"
        quote += '#####' + splitStr[1] + '#####'

        quote += "\n\n*****"
        quote += "\n\n^^***If*** ^^***you*** ^^***would*** ^^***like*** ^^***to*** "
        quote += "^^***add*** ^^***a*** ^^***quote***, ^^***please*** ^^***contact*** "
        quote += "^^***my*** ^^***owner:*** ^^/u/NeverForgetY2K"
        return quote