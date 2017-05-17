print("Loading imports")
import discord
#import nltk
import configparser
from pyteaser import Summarize
from newspaper import Article

config = configparser.ConfigParser()
client = discord.Client()

'''
    -Add a blacklist
        amazon.com
        youtube.com
        giphy.com
        imgur.com
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
    
    #TODO: message.contains

    if message.content.startswith('http://') or message.content.startswith('https://'):
        await client.send_message(message.channel, "Im reading, give me a second")
        #TODO: Sanitize this
        #TODO: Write own html scraper
        print("Parsing: " + message.content.split(' ')[0])
        article = Article(message.content.split(' ')[0])
        article.download()
        article.parse()

        #TODO: Write own summary function
        summary = "".join(Summarize(article.title, article.text))
        await client.send_message(message.channel, "\n\nSummary:\n " + summary)

   # if message.content.

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

print("Loading config")
config.read("bot.config")
client.run(config.get("bot","token"))
