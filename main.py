import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import insta_downloader as indo
load_dotenv()
token  = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log',encoding='utf-8',mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot =  commands.Bot(command_prefix='!',intents=intents)

@bot.event
async def on_ready():
    print(f"Namaste, {bot.user.name}") 

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if "https://www.instagram.com/" in message.content:
        await message.channel.send(f"instagram {message.content}")
        postcode = indo.url_to_postcode(message.content)
        if postcode:
            try:
                path = indo.download_post(postcode)
                await message.channel.send(f"{message.author.mention}", file = discord.File(path,f"{postcode}.mp4"))
                indo.delete_post(postcode)
            except Exception as e:
                print(f"error : {e}")
        else:
            await message.channel.send(f"{message.author.mention} worng url or post is unavailable")
            
        
    
    await bot.process_commands(message)



bot.run(token,log_handler=handler,log_level=logging.DEBUG)