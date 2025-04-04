import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import dotenv_values, load_dotenv
load_dotenv("./.env")

intents = discord.Intents.all() #todas as permissoes
bot = commands.Bot(command_prefix=".", intents=intents)#bot recebe as permissoes

async def carregar_cogs():
    for arquivo in os.listdir('comandos'):
        if arquivo.endswith (".py"):
            await bot.load_extension(f"comandos.{arquivo[:-3]}")


@bot.event
async def on_ready(): #roda quando o bot estiver pronto
    await bot.tree.sync()
    await carregar_cogs()
    
    try : #Carrega os cogs
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)} Sincronizado")
    except Exception as e:
        print(f"ERRO: {e}")
    print("Bot on!!")


bot.run(os.getenv("BOT_TOKEN"))

