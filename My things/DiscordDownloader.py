import os

import discord
import requests

client = discord.Client()
guild = discord.Guild

SERVER_NAME = "Bad Ideas Zone"
CHANNEL_NAME = "ehemc-submissions"

PATH = "/EHEMC Tracks"


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    print("Download starting...")

    server = discord.utils.get(client.guilds, name=SERVER_NAME)
    if server is None:
        print("No server")
        return

    channel = discord.utils.get(server.channels, name=CHANNEL_NAME)
    if channel is None:
        print("No channel")
        return

    async for msg in channel.history(limit=10000):
        if msg.attachments:
            for att in msg.attachments:
                if ".Challenge.Gbx" in att.filename:
                    mapName = att.filename[:-14]
                    downloadLink = att.url
                    discordName = msg.author.name
                    if msg.edited_at is None:
                        date = msg.created_at
                    else:
                        date = msg.edited_at

                    fileName = f"""%{discordName}%{mapName}%{date.strftime("%m-%d_%H§%M")}%.Challenge.Gbx"""
                    if fileName not in os.listdir(PATH):
                        print(f"Downloading {mapName}")
                        r = requests.get(downloadLink)
                        with open(PATH+"/"+fileName, 'wb') as outfile:
                            outfile.write(r.content)
                        await msg.add_reaction("✅")
    print("Download ended")
    await(client.close())


def run():
    client.run("ODc4OTAzNjA1NzcwNDU3MTU4.YSH8xA.WjaVhfoFmgm7GJ661qGFq_xojuw")
