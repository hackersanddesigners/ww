import re
import random
import bot

def main():
    print "Hello. How are you feeling today?"

    while True:
        statement = raw_input("> ")
        print bot.analyze(statement)

        if statement == "quit":
            break


if __name__ == "__main__":
    main()
