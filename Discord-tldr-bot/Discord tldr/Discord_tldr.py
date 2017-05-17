print("Loading imports")
import discord
#import nltk
import configparser
from pyteaser import Summarize
from newspaper import Article

config = configparser.ConfigParser()
client = discord.Client()
blacklistFile = open("blacklist", "r+")

'''
    -autogenerate config file
    -fix webpage exploit
    -@botname blacklist whatever.com
    -write my own scraper
        Reddit support
        If under certin length, do not post
    -Add contains() support
    -Output cleaning
        soundcloud
        reddit support

'''

@client.event
async def on_message(message):
    
    if 'http://' in message.content:#for http links
        url = message.content[message.content.find('http://'):len(message.content)].split(' ')[0]
        if blacklisted(url) == False:
            await shorten(message, url)#sends the message object, and the url

    if 'https://' in message.content:#for https links
        url = message.content[message.content.find('https://'):len(message.content)].split(' ')[0]
        if blacklisted(url) == False:
            await shorten(message, url)

@client.event
async def on_ready():
    '''
    #I need a way to update everything
    if config.get("update","nltk") == "true":
        print("Updating nltk")
        #nltk.
        print("nltk updated")
    '''
    print()
    print("Logged in as ", end=""),
    print(client.user.name)
    print("ID: ", end=""),
    print(client.user.id)
    print('------------')


def blacklisted(url = 'wesring.com'):
    rootUrl = url[(url.find("://")+3):url.find("/",url.find("://")+3)]#Find whats inbetween :// and the next /
    rootUrl = rootUrl[rootUrl.rfind(".", 0, rootUrl.rfind("."))+1:len(rootUrl)]#removes the subdomains
    
    #print("Root: " + rootUrl)
    for i in range(0,len(blacklist)):#check to see if its in the blacklist
        if blacklist[i].rstrip() == rootUrl:
            print("Blacklisted URL ignored: " + rootUrl)#url match
            return True
    return False#url is not blacklisted

async def shorten(message, url = 'wesring.com'):#I am the error page
    await client.send_message(message.channel, "Im reading, give me a second")
    #TODO: Sanitize this
    #TODO: Write own html scraper
    print("Parsing: " + url)
    article = Article(url)
    article.download()
    article.parse()

    #TODO: Write own summary function
    summary = "".join(Summarize(article.title, article.text))
    await client.send_message(message.channel, "\n\nSummary:\n " + summary)
    print("done")

print("Loading config")
blacklist = blacklistFile.readlines()
config.read("bot.config")
client.run(config.get("bot","token"))
