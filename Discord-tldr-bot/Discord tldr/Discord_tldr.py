print("Loading imports")
import discord
#import nltk
import configparser
from pyteaser import Summarize
from newspaper import Article

client = discord.Client()

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
            print(blacklistURL + " has now been blacklisted by " + message.author.name + " " + message.author.id)

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
    #print("Blacklist " + str(blacklist)) 
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
blacklistFile = open("blacklist", "r+")
blacklist = blacklistFile.readlines()
blacklistFile.close()
config = configparser.ConfigParser()
config.read("bot.config")
client.run(config.get("bot","token"))
