import os
import time
import discord
import asyncio
import json
import random
import requests
from colorama import init, Fore, Back, Style
init(convert=True)

#GET CONFIG

with open("config.json") as json_data_file:
        config = json.load(json_data_file)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

#var

clientGuildList = []
listener = False
Input = None

previousChannelToSend = None
previousUser = None
webhook = None

# func

def restart():
    exit()

def clear():
    os.system("cls")
    os.system("clear")
    

def ascii():

    print("""                         ___                   
                       /   | __  ___________ _
                      / /| |/ / / / ___/ __ `/
                     / ___ / /_/ / /  / /_/ / 
                    /_/  |_\__,_/_/   \__,_/ /{}""".format("kkk kkk"))

def hotbar(power):

    print("             ------------------------------------------")
    if power == True:
        print("             | " + Fore.BLUE + "Discord" + Fore.RESET + " Server Listener / Listener: " + Fore.GREEN + "ON" + Fore.RESET + " |")
    elif power == False:    
        print("             | " + Fore.BLUE + "Discord" + Fore.RESET + " Server Listener / Listener: " + Fore.RED + "OFF" + Fore.RESET + " |")
    print("             ------------------------------------------")

def listenPanel(Input, Outpout):
        print("\n\n   |" + Fore.RED + "\tTarget" + Fore.RESET + ":\n   |\t   > " + Input.object.name + "\n   |\n   |" + Fore.GREEN + "\tOutpout" + Fore.RESET + ":\n   |\t   > " + Outpout.object.name)

def guildPanel():
    text = " \n"
    for guild in clientGuildList:
        text = text + "             [" + Fore.RED + str(clientGuildList.index(guild)+1) + Fore.RESET + "] | " + Fore.YELLOW + str(guild.object.name)  + Fore.RESET + "\n"
    print(text)

#class

class syncedChannel():
    def __init__(self, dscObject):
        self.object = dscObject
        self.synced = None

    async def syncMeWithAnotherChannel(self, channelToSync):
        self.synced = channelToSync

    async def cloneAndSendTheMessageFromUser(self, message, channelToSend):
        global previousUser, previousChannelToSend, webhook
        user = message.author
        if previousChannelToSend and previousUser:
            if user.id != previousUser.id or channelToSend.id != previousChannelToSend.id:
                await webhook.delete()
                name = user.display_name + " | (" + user.name + ")"
                avatar = requests.get(user.avatar.url).content
                webhook = await channelToSend.create_webhook(name=name, avatar=avatar)
                await webhook.send(message.content)
                previousUser = user
                previousChannelToSend = channelToSend
            else:
                await webhook.send(message.content)
        else:
            name = user.display_name + " | (" + user.name + ")"
            avatar = requests.get(user.avatar.url).content
            webhook = await channelToSend.create_webhook(name=name, avatar=avatar)
            await webhook.send(message.content)
            previousUser = user
            previousChannelToSend = channelToSend

class thisGuild:
    def __init__(self, dscObject):
        self.object = dscObject
        self.myChannel = []
    
    async def cloneMeToAnotherGuild(self, Outpout):
        for channel in self.object.text_channels:
            if channel.category == None:
                thisChannel = await Outpout.object.create_text_channel(name=channel.name, position=channel.position)
                newChannel = syncedChannel(thisChannel)
                Outpout.myChannel.append(newChannel)
                newChannel = syncedChannel(channel)
                self.myChannel.append(newChannel)
        for category in self.object.categories:
            currentCategory = await Outpout.object.create_category(name=category.name)
            for channel in category.text_channels:
                thisChannel = await Outpout.object.create_text_channel(name=channel.name, category=currentCategory, position=channel.position)
                newChannel = syncedChannel(thisChannel)
                Outpout.myChannel.append(newChannel)
                newChannel = syncedChannel(channel)
                self.myChannel.append(newChannel)

    async def syncMeWithAnotherGuild(self, Outpout):
        for channel in Outpout.object.text_channels:
            if channel.category == None:
                if channel.name == self.myChannel[Outpout.object.text_channels.index(channel)].object.name:
                    self.myChannel[Outpout.object.text_channels.index(channel)].synced = channel
                    print("| " + Fore.GREEN + "Synced " + Fore.RESET + self.myChannel[Outpout.object.text_channels.index(channel)].object.name)
                    
        for category in Outpout.object.categories:
            for channel in category.text_channels:
                if channel.name == self.myChannel[Outpout.object.text_channels.index(channel)].object.name:
                    self.myChannel[Outpout.object.text_channels.index(channel)].synced = channel
                    print("| " + Fore.GREEN + "Synced " + Fore.RESET + self.myChannel[Outpout.object.text_channels.index(channel)].object.name)
                    
        

    async def clearGuild(self):
        for channel in self.object.channels:
            try:
                await channel.delete()
            except:
                pass
        
 
#script

@client.event
async def on_ready():
    global listener, Input
    for guild in client.guilds:
        currentGuild = client.get_guild(guild.id)
        currentGuild = thisGuild(currentGuild)
        clientGuildList.append(currentGuild)  

    clear()
    ascii()
    hotbar(False)
    guildPanel()
    print("\n| Choose 2 server too pair by their number. \n")
    firstServ = input("\t[Target > ")
    secondServ = input("\t[Outpout > ")

    firstServNumber = int(firstServ) - 1
    secondServNumber = int(secondServ) - 1
    clear()
    ascii()
    hotbar(False)
    if clientGuildList[firstServNumber] and clientGuildList[secondServNumber] and firstServNumber != secondServNumber:
            
            Input = clientGuildList[firstServNumber]
            Outpout = clientGuildList[secondServNumber]

            print("\n[SETUP]:\n")
            print("| "+ Fore.YELLOW + "Clearing " + Fore.RESET  + Outpout.object.name + "...")
            await Outpout.clearGuild()
            print("| Fully "+ Fore.GREEN + "cleared " + Fore.RESET  + Outpout.object.name + " !")
            time.sleep(1.5)
            print("| "+ Fore.YELLOW + "Cloning " + Fore.RESET  + Input.object.name + " on " + Fore.CYAN + str(Outpout.object.name) + Fore.RESET +  "...")
            await Input.cloneMeToAnotherGuild(Outpout)
            print("| " + Input.object.name + Fore.GREEN + " cloned " + Fore.RESET + "to " + Outpout.object.name + " !")
            time.sleep(1.5)
            clear()
            ascii()
            hotbar(False)
            print("\n[SYNC]:\n")
            time.sleep(0.5)
            await Input.syncMeWithAnotherGuild(Outpout)
            time.sleep(1.5) 
            listener = True
            clear()
            ascii()
            hotbar(True)
            time.sleep(0.5)
            listenPanel(Input, Outpout)

    else:
            restart()

@client.event
async def on_message(message):
    if listener:
        if message.guild.id == Input.object.id:
            for inputChannel in Input.myChannel:
                if message.channel.id == inputChannel.object.id:
                    await inputChannel.cloneAndSendTheMessageFromUser(message, inputChannel.synced)
    else:
        pass
    

    

print(Fore.GREEN + "Loading" + Fore.RESET)
client.run(config["TOKEN"])
