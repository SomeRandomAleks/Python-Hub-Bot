import discord
from discord.ext import commands
from discord.ext.commands import Cog
import datetime
import pytz

intents = discord.Intents.all()
intents.members = True
intents.reactions = True

client = commands.Bot(command_prefix="!", intents=intents)
python_hub = "https://cdn.discordapp.com/attachments/814986274158805033/814986385429758012/Python_Hub_1.png"
tz = pytz.timezone('EST')
datetime_now = datetime.datetime.now(tz)
current_time = datetime_now.strftime("%H:%M")

log_channel = 818568955010613299
start_stop = True


async def get_category(guild, category) -> discord.CategoryChannel:
    return discord.utils.get(guild.categories, name=category)


async def get_text_channel(guild, channel) -> discord.TextChannel:
    return discord.utils.get(guild.channels, name=channel)


async def get_voice_channel(guild, channel) -> discord.TextChannel:
    return discord.utils.get(guild.channels, name=channel)

async def get_lowest_occupied_channel(guild) -> discord.TextChannel:
	occupied_category = discord.utils.get(guild.categories, name="Help: Occupied")
	return occupied_category.channels[-1]

async def get_lowest_available_position(guild) -> discord.TextChannel:
	available_category = discord.utils.get(guild.categories, name="Help: Occupied")
	return available_category.channels[-1]

bad_words_list = ["ass", "shit", "bitch", "fuck", "porn", "pussy", "butt", "son of a", "dating"]



    



