import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import insta_downloader as indo
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home():
    return "Bot is alive"

def run():
    app.run(host='0.0.0.0', port=3000)

def keep_alive():
    t = Thread(target=run)
    t.start()

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "https://www.instagram.com/" in message.content:
        # await message.channel.send(f"instagram {message.content}")
        postcode = indo.url_to_postcode(message.content)
        if postcode:
            try:
                path = indo.download_post(postcode)
                print(f"downloaded : {path}-----------")
                if path and os.path.exists(path):
                    await message.channel.send(f"{message.author.mention}", file = discord.File(path))
                    print(f"uploaded----------")
                    indo.delete_post(postcode)
                else:
                    await message.channel.send(f"{message.author.mention} Failed to download Instagram post. It might be private or unavailable.")
            except Exception as e:
                print(f"error : {e}")
                await message.channel.send(f"{message.author.mention} Error downloading post: {str(e)}")
        else:
            await message.channel.send(f"{message.author.mention} worng url or post is unavailable")



    await bot.process_commands(message)

keep_alive()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
