import re
import random
import bot

def main():
    print "What is your first commandment?"

    while True:
        statement = raw_input("> ")
        print bot.analyze(statement)

        if statement == "quit":
            break


if __name__ == "__main__":
    main()
