import praw
import time
import configparser
import re
import argparse
import setup
import logging

commented = set()
config = configparser.ConfigParser()
config.read("user.ini")
USERNAME = config["info"]["name"]
PASSWORD = config["info"]["password"]
r = praw.Reddit(user_agent="testing")
r.login(USERNAME, PASSWORD, disable_warning=True)

def main():
    data_extract = setup.Data_Extractor()
    subreddit = r.get_subreddit(config["info"]["subreddit"])
    comments = subreddit.get_comments(limit = 100)
    for comment in comments:
        if not is_command(comment.body):
            continue
        #do not reply to the bot itself
        if comment.author.name == USERNAME:
            continue
        profs = get_wanted_prof(comment.body)
        reply = ""
        if profs is not None:
            #revisit RateMyProfessor to update info
            data_extract.setup()
            for prof in profs:
                reply += data_extract.search_prof(prof) + "\n\n"
        else:
            reply = "wrong format\n\n"

        reply = reply + "\n\n" + get_usage_instruction()
        if comment.id not in commented:
            comment.reply(reply)
            print("replied")
            commented.add(comment.id)

#return a list of professors to be searched

def is_command(comment):
    argument_result = re.search("(?<=!prof)(.)*", comment)
    return not (argument_result is None)

def get_wanted_prof(comment):
    argument_result = re.search("(?<=!prof)(.)*", comment)
    if argument_result is None:
        return argument_result
    argument = argument_result.group(0)
    return parse_argument(argument.strip())

def parse_argument(arg):
    wanted = re.findall("\((.*?)\)", arg)
    return wanted

def get_usage_instruction():
    return "usage: !prof (prof1 name) (prof2 name) ... \n\n" + \
            "name can be in the format of (first last), (first initial last), (last first)"

if __name__ == "__main__":
    while True:
        try:
            main()
        except:
            logging.exception("bad stuff happened")
        #print("done cycle")
        time.sleep(5)
        #break