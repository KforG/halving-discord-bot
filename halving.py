import discord
import requests

Token = ""
client = discord.Client()

BlockHalving = 1680000
BrHalving = 12.5
BrNow = BrHalving * 2
GetBlockURL = "https://ocm-backend.blkidx.org/info"

def getBlockCount():
    currentBlockHeight = requests.get(GetBlockURL).json()
    blocksRemain = BlockHalving - int(currentBlockHeight['backendTipHeight'])
    return blocksRemain

def getTimeLeft(blocksRemain):
    time = blocksRemain * 150
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    if day != 0:
        if day > 1:
            return "%d Days %d Hours %d Minutes %d Seconds" % (day, hour, minutes, seconds)
        return "%d Day(s) %d Hours %d Minutes %d Seconds" % (day, hour, minutes, seconds)
    elif day == 0 and hour != 0:
        if hour == 1:
            return "%dHour %dMinutes %dSeconds" % (hour, minutes, seconds)
        return "%dHours %dM %dS" % (hour, minutes, seconds)
    elif day == 0 and hour == 0 and minutes != 0:
            return "%dM %dS" % (minutes, seconds)
    else:
            return "%dS" % (seconds)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('?halving'):
        print("?halving command detected")
        blocksRemain = getBlockCount()

        if blocksRemain > 0:
            timeLeft = getTimeLeft(blocksRemain)
            send = "%s blocks remaining before halving! Estimated time before halving: %s" %(blocksRemain, timeLeft)
        else:
            send = "Vertcoin's blockreward has been halved from %s VTC to %s VTC" %(BrNow, BrHalving)

        await message.channel.send(send)
        print("Responded to command")

    if message.content.startswith('?whatishalving'):
        print("Question halving command detected")
        send = "On block %s Vertcoin's blockreward will be cut in half from %s VTC to %s VTC" %(BlockHalving, BrNow, BrHalving)
        await message.channel.send(send)
        print("Responded to command")

client.run(Token)