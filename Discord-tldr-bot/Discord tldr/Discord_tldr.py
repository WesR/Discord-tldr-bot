print("Loading imports")
import discord
#import nltk
import configparser
import datetime
import logging
#import markovify
from pyteaser import Summarize
from newspaper import Article

client = discord.Client()

'''
    -admin creds for users
    -autogenerate config file
    -fix webpage exploit
    -write my own scraper
        Reddit support
        If under certin length, do not post
    -Output cleaning
        soundcloud
        reddit support

'''

@client.event
async def on_message(message):
    
    if message.content.startswith('<@' + client.user.id + ">"):
        command = message.content.split('<@' + client.user.id + ">")[1].strip().rstrip()
        if command[0:len('blacklist')] == 'blacklist':#Command: Blacklist
            blacklistURL = command[len('blacklist'):len(command)].strip()#Remove the blacklist command
            if blacklistURL.find("://") != -1:#If its not a clean url, remove the http and trailing address
                blacklistURL = blacklistURL[(blacklistURL.find("://")+3):blacklistURL.find("/",blacklistURL.find("://")+3)]#Find whats inbetween :// and the next /

            if blacklistURL.find(".") != blacklistURL.rfind("."):
                blacklistURL = blacklistURL[blacklistURL.rfind(".", 0, blacklistURL.rfind("."))+1:len(blacklistURL)]#removes the subdomains
            
            blacklistFile = open("blacklist", "a")
            blacklistFile.write("\n" + blacklistURL)#Write to disk
            blacklistFile.close()
            blacklist.append(blacklistURL)#Write to ram
            await client.send_message(message.channel, blacklistURL + " has now been blacklisted")#feedback
            logInfo(blacklistURL + " has now been blacklisted by " + message.author.name + " " + message.author.id)

        elif command[0:len('show')] == 'show':
            await client.send_message(message.channel, "show")

        elif command[0:len('shorten')] == 'shorten':
            if 'http://' in message.content:#If its http, use use that url, else https
                url = message.content[message.content.find('http://'):len(message.content)].split(' ')[0]
            else:
                url = message.content[message.content.find('https://'):len(message.content)].split(' ')[0]
            await shorten(message, url)#shorten the link

        elif command[0:len('help')] == 'help':
            await client.send_message(message.channel, "use @" + client.user.name + " to use a command\nblacklist <url> to blacklist a site\nshow <config> or <blacklist> to show the lists\nshorten <url> ro force shorten a url")
        else:
            await client.send_message(message.channel, "Whats up?")
        return

    if 'http://' in message.content:#for http links
        url = message.content[message.content.find('http://'):len(message.content)].split(' ')[0]
        if blacklisted(url) == False:
            await shorten(message, url)#sends the message object, and the url
        return

    if 'https://' in message.content:#for https links
        url = message.content[message.content.find('https://'):len(message.content)].split(' ')[0]
        if blacklisted(url) == False:
            await shorten(message, url)
        return

@client.event
async def on_ready():
    '''
    #I need a way to update everything
    if config.get("update","nltk") == "true":
        logInfo("Updating nltk")
        #nltk.
        logInfo("nltk updated")
    '''
    logInfo()
    logInfo("Logged in as " + client.user.name)
    logInfo("ID: " + client.user.id)
    logInfo('------------')


def blacklisted(url = 'wesring.com'):
    rootUrl = url[(url.find("://")+3):url.find("/",url.find("://")+3)]#Find whats inbetween :// and the next /
    rootUrl = rootUrl[rootUrl.rfind(".", 0, rootUrl.rfind("."))+1:len(rootUrl)]#removes the subdomains
    
    #logInfo("Root: " + rootUrl)
    #logInfo("Blacklist " + str(blacklist)) 
    for i in range(0,len(blacklist)):#check to see if its in the blacklist
        if blacklist[i].rstrip() == rootUrl:
            logInfo("Blacklisted URL ignored: " + rootUrl)#url match
            return True
    return False#url is not blacklisted

async def shorten(message, url = 'wesring.com'):#I am the error page
    await client.send_message(message.channel, "Im reading, give me a second")
    #TODO: Write own html scraper
    logInfo("Parsing: " + url)
    article = Article(url)
    article.download()
    article.parse()

    #TODO: Write own summary function
    summary = "".join(Summarize(article.title, article.text))
    await client.send_message(message.channel, "\n\nSummary:\n " + summary)
    logInfo("done")

'''
This just makes a markov chain of words. It works best with big texts

async def markov(message, url = 'wesring.com'):
    await client.send_message(message.channel, "Im reading, give me a second")
    await client.send_message(message.channel, "Note: I am using marcov chains")
    #TODO: Write own html scraper
    logInfo("Parsing: " + url)
    article = Article(url)
    article.download()
    article.parse()

    #TODO: Write own summary function
    summary = ""
    text_model = markovify.Text(article.text)
    for i in range(0,5):
        summary += str(text_model.make_sentence())
    await client.send_message(message.channel, "\n\nSummary:\n " + summary)
    logInfo("done")
'''

def logInfo(message = ""):#So we log to console and disk
    logging.info(message)
    print(message)

print("Loading config")
blacklistFile = open("blacklist", "r")#Open blacklist
blacklist = blacklistFile.readlines()
blacklistFile.close()#Close the blacklist
config = configparser.ConfigParser()#Load config
config.read("bot.config")
logging.basicConfig(filename="runninglog" + str(datetime.datetime.now()).replace(' ','').replace(':','-') + ".log", level=logging.INFO)
logging.info("Bot start: " + str(datetime.datetime.now()))
rawConfig = open("bot.config", "r")#Opening the config just to get the raw config file
logging.info("Config:" + str(rawConfig.readlines()))#Writing the config to log
rawConfig.close()
logging.info("Blacklist: " + str(blacklist) + "\n")
client.run(config.get("bot","token"))