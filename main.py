import discord
from discord.ext.commands import Bot
import aiosqlite # For repl
import uvloop
uvloop.install()
from tortoise import Tortoise, run_async
import config
import os
import aerich

client = Bot(command_prefix = "g!", intents = discord.Intents().all())


async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "models"
    await Tortoise.init(
        
        db_url=f'sqlite://{config.db}',
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas()
    
@client.event
async def on_ready():
    print(client.user)
    await init()

# Add in all cogs
for f in os.listdir("cogs"):
    if not f.startswith("_") or f.startswith("."):
        path = "cogs." + f.replace(".py", "")
        print("Discord: Loading " + f.replace(".py", "") + " with path " + path)
        client.load_extension(path)

if __name__ == "__main__":
    client.run(config.token)