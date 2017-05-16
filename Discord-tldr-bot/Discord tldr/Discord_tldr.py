print("Loading imports")
import discord
#import nltk
import configparser
from pyteaser import Summarize
from newspaper import Article

config = configparser.ConfigParser()
client = discord.Client()

@client.event
async def on_message(message):
    
    #TODO: message.contains

    if message.content.startswith('http://') or message.content.startswith('https://'):
        await client.send_message(message.channel, "Im reading, give me a second")
        #TODO: Sanitize this
        #TODO: Write own html scraper
        print("Parsing: " + message.content)
        article = Article(message.content)
        article.download()
        article.parse()

        #TODO: Write own summary function
        summary = "".join(Summarize(article.title, article.text))
        await client.send_message(message.channel, "\n\nSummary:\n " + summary)

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
