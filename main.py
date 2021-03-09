# DEFAULT IMPORTS
import random
import json
import time
import datetime
import os

# NON-DEFAULT IMPORTS
import discord
import asyncio
import typing
import threading
from bs4 import BeautifulSoup

# OTHER IMPORTS
from discord.ext import commands
from discord.ext.commands import Cog
try:
	from googlesearch import search
except ModuleNotFoundError:
	os.system('pip install google')

# FILE IMPORTS
from cogs.resources import *
import requests
import keep_alive

# BOT SETUP
intents = discord.Intents.all()
intents.members = True
intents.reactions = True

client = commands.Bot(command_prefix="!", intents=intents)
client.remove_command("help")

# COG EXTENSIONS
client.load_extension('cogs.rr')
client.load_extension('cogs.bump')





@client.event
async def on_ready():
	print("Bot is ready")
	guild = client.get_guild(796139098086703145)
	bot_dev = discord.utils.get(guild.channels, id=814981031236599838)
	msg = f"Bot is up! Watching {len(guild.members)} members\nTime: **{current_time}**"
	await client.get_channel(bot_dev.id).send(msg)
	announcements = discord.utils.get(guild.roles, name="Announcements")
	bump = discord.utils.get(guild.roles, name="Bump")
	while True:
		await asyncio.sleep(10)
		with open('spam.txt', 'r+') as f:
			f.truncate(0)
		disboard = discord.utils.get(guild.members, id=302050872383242240)
		members = discord.utils.get(guild.roles, name="Members")
		if disboard.status == discord.Status.offline:
			history = await client.get_channel(797342261507391488).history(limit=2).flatten()
			for message in history:
				if "Disboard is offline" in message.content:
					return
			await client.get_channel(797342261507391488).set_permissions(members, send_messages=False, read_messages=True)
			await client.get_channel(797342261507391488).send(f"{bump.mention} Disboard is offline, you will be notified when it is back online")
		else:
			history = await client.get_channel(797342261507391488).history(limit=2).flatten()
			for message in history:
				if "Disboard is offline" not in message.content:
					return
				await client.get_channel(797342261507391488).purge(limit=1)
				await client.get_channel(796206902895181844).send(f"{bump.mention} Disboard is back online")
				await client.get_channel(797342261507391488).set_permissions(members, send_messages=True, read_messages=True)


keep_alive.keep_alive()



@client.listen('on_message')
async def spam(message):
	moderation = discord.utils.get(message.guild.roles, name="Moderation")
	if moderation in message.author.roles:
		return
	if not start_stop:
		return
	counter = 0
	role = discord.utils.get(message.guild.roles, name="Muted")
	with open('spam.txt', 'r+') as file:
		for lines in file:
			if lines.strip('\n') == str(message.author.id):
				counter+=1
		
		file.write(f"{str(message.author.id)}\n")
		if counter >= 20:
			await message.author.add_roles(role)
			embed = discord.Embed(title=f"{message.author} has been muted", description="Reason: Spam\nThey will be unmuted in 30 seconds", color=0x1f4454)
			embed.set_thumbnail(url=message.author.avatar_url)
			embed.set_footer(text=time.ctime())
			user_msgs = await message.channel.history(limit=10).flatten()
			for msg in user_msgs:
				if msg.author.id == message.author.id:
					await msg.delete()
			await message.channel.send(embed=embed)
			await asyncio.sleep(30)
			await message.author.remove_roles(role)
			em = discord.Embed(title=f"{message.author} has been unmuted", description=f"Reason was: Spam", color=0x1f4454)
			em.set_thumbnail(url=message.author.avatar_url)
			em.set_footer(text=time.ctime())
			await message.channel.send(embed=em)






@client.listen('on_message')
async def ping(message):
	if not start_stop:
		return
	if f'<@!{client.user.id}>' in message.content:
		await message.channel.send(f"Hi {message.author.mention}! "
		f"I am **Python Hub**, the bot for the **Python Hub** server. You can find me on "
		f"GitHub if you want to check out my code."
		f"\nhttps://github.com/SomeRandomAleks/Python-Hub")





@client.listen('on_message')
async def help_rotate(message):
	if message.channel.id == 815030730211983361:
		return
	if message.author.bot:
		return
	if message.channel.category.id == 807121103993569321:
		await message.channel.edit(
			category=await get_category(message.guild, "Help: Occupied"),
			sync_permissions=True,
			position=0
		)
		await message.channel.send(f"""
	{message.author.mention}, you have claimed this channel!
Please give as much info as possible so we have the best chance of assisting you.
Also, please use codeblocks/fields to send code, if your code is too long then you can use hastebin/pastebin
or send half of your code, then send the other half.
Also be patient, if you haven't got a response for more than 1 hour then you can ping Coding Helpers""")
		next_channel = await get_lowest_occupied_channel(message.guild)
		await next_channel.edit(
			category=await get_category(message.guild, "Help: Available"),
			sync_permissions=True,
		)
		await next_channel.send("**This channel is now free for anyone to ask in!**")





@client.listen('on_message')
async def user_bump(message):
	if not start_stop:
		return
	if message.channel.id == 797342261507391488:
		return
	elif message.content == "!d bump":
		await message.delete()
	



@client.listen('on_message')
async def on_member_join(member):
	if not start_stop:
		return

	guild_id = member.guild
	channel = client.get_channel(804882935227744266)
	await channel.edit(name=f"Member Count: {guild_id.member_count}")




@client.listen('on_message')
async def on_member_remove(member):
	if not start_stop:
		return
	guild_id = member.guild
	channel = client.get_channel(804882935227744266)
	await channel.edit(name=f"Member Count: {guild_id.member_count}")



@client.listen('on_message')
async def not_verify(message):
	if not start_stop:
		return
	if message.channel.id == 803826776970231888:
		if message.author.id != 796195995284406292:
			await message.delete()
		else:
			return
	else:
		return


@client.command()
async def verify(ctx):
	if not start_stop:
		return
	msg = ctx.message
	if ctx.channel.id == 803826776970231888:
	
		await msg.delete()
		role = discord.utils.get(ctx.guild.roles, name="Members")
		await ctx.author.add_roles(role)
		await ctx.send(f"Granted access for {ctx.author.mention}")
	else:
		await msg.delete()
		fail = await ctx.send(f"{ctx.author.mention}, you cannot use that command here")
		await asyncio.sleep(4)
		await fail.delete()



@client.command()
@commands.has_role("Moderation")
async def say(ctx, *, reason):
	if not start_stop:
		return
	embed = discord.Embed(description=reason, color=0x1f4454)
	embed.set_footer(text=time.ctime())
	await ctx.send(embed=embed)

@client.command()
@commands.has_role("Moderation")
async def clear(ctx, amount):
	if not start_stop:
		return
	await ctx.channel.purge(limit=int(amount)+1)
	msg = await ctx.send(f"{ctx.author.mention} cleared {amount} messages")
	await asyncio.sleep(4)
	await msg.delete()

@client.command()
@commands.has_role("Moderation")
async def mute(ctx, member : discord.Member, *, reason):
	if not start_stop:
		return
	role = discord.utils.get(ctx.guild.roles, name="Muted")
	await member.add_roles(role)
	embed = discord.Embed(title=f"{member.name} has been muted", description=f"Reason: {reason}", color=0x1f4454)
	embed.set_thumbnail(url=member.avatar_url)
	await ctx.send(embed=embed)

@client.command()
@commands.has_role("Moderation")
async def unmute(ctx, member : discord.Member):
	if not start_stop:
		return

	role = discord.utils.get(ctx.guild.roles, name="Muted")

	if role in member.roles:
		await member.remove_roles(role)
		embed = discord.Embed(title=f"{member} was successfully unmuted", description=f"{ctx.author.mention} unmuted {member}", color=0x1f4454)
		embed.set_thumbnail(url=ctx.author.avatar_url)
		await ctx.send(embed=embed)

	else:
		await ctx.send(f"{member} is not already muted")



@client.command()
@commands.has_role("Moderation")
async def kick(ctx, member : discord.Member, *, reason=None):
	if not start_stop:
		return
	await member.kick(reason=reason)

	guild = client.get_guild(ctx.author.guild.id)
	embed = discord.Embed(title=f"{member} was kicked", description=f"{ctx.author.mention} has kicked {member}\nReason: {reason}", color=0x1f4454)
	embed.set_thumbnail(url=member.avatar_url)
	embed.set_footer(text=f"We are now at {guild.member_count} members")

	await ctx.send(embed=embed)



@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, reason=None):
	if not start_stop:
		return
	await member.ban(reason=reason)
	embed = discord.Embed(title='Member Banned', description=f'{member} has been banned by {ctx.author}', color=0x1f4454)
	embed.set_thumbnail(url=ctx.author.avatar_url)
	await ctx.send(embed=embed)



@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, user=None):
	if not start_stop:
		return

	try:
		user = await commands.converter.UserConverter().convert(ctx, user)
	except:
		await ctx.send("Error: user could not be found!")
		return

	try:
		bans = tuple(ban_entry.user for ban_entry in await ctx.guild.bans())
		if user in bans:
			await ctx.guild.unban(user, reason="Responsible moderator: "+ str(ctx.author))
		else:
			await ctx.send("User not banned!")
			return

	except discord.Forbidden:
		await ctx.send("I do not have permission to unban!")
		return

	except:
		await ctx.send("Unbanning failed!")
		return

	embed = discord.Embed(title="Unban", description=f"{user} was successfully unbanned by {ctx.author}", color=0x1f4454)
	embed.set_thumbnail(url=ctx.author.avatar_url)

	await ctx.send(embed=embed)



@client.command(aliases=['mod'])
async def moderation(ctx):
	if not start_stop:
		return
	embed = discord.Embed(title="Moderation", description=
	"""
	```
!clear <#>```
Clears messages
```!mute <@member> <reason>```
Mutes the member
```!unmute <@member>```
Unmutes the member
```!kick <@member> <reason>```
Kicks the member
```!ban <@member> <reason>```
Bans the member
```!unban <@member>```
Unbans the member
	""")
	embed.set_thumbnail(url=python_hub)
	await ctx.send(embed=embed)


@client.command()
async def help(ctx):
	if not start_stop:
		return
	embed = discord.Embed(title="Commands", description="""
	```!free```
	Gets an available python help channel
	```!other help```
	Info about help with languages other than python
	```!learning sources```
	Gives our recommended python learning sources
	```!google <message>```
	Searches Google for something""", inline=True)
	await ctx.send(embed=embed)


@client.listen('on_message')
async def ping(message):
	if not start_stop:
		return
	mention = '@Python Hub#8757 '
	if mention in message.content:
		await message.channel.send(f"Hi {message.author.mention}, I am"
		"{client.mention}! You can find me on Github, this is my repo:\n"
		"https://github.com/SomeRandomAleks/Python-Hub")

@client.command()
async def free(ctx):
	if not start_stop:
		return
	available = discord.utils.get(ctx.guild.categories, name="Help: Available")
	free_channels = []
	for channel in available.channels:
		if channel.id != 815030730211983361:
			free_channels.append(str(channel.id))
	await ctx.send(f"You can use this free python help channel below:\n" + client.get_channel(int(random.choice(free_channels))).mention)


@client.command()
async def other(ctx, help):
	if not start_stop:
		return
	if help != "help":
		return
	
	embed = discord.Embed(title="Not Python", 
	description=
	f"If the programming language you need help with is "
	f"not python, then you can ask for help in that language in "
	f"{client.get_channel(807336190796890162).mention} if it is not part of an "
	f"already exising help channel in **Other Help**")
	await ctx.send(embed=embed)

@client.command()
async def google(ctx, reason=None):
	if not start_stop:
		return
	if reason == None:
		await ctx.send("I didn't get a message to search for ```!google <message>```")
		return
	if any(word in reason for word in bad_words_list):
		await ctx.message.delete()
		return
	searching = discord.Embed(title="Google Search", description="Searching...")
	search_msg = await ctx.send(embed=searching)
	results = []
	for j in search(reason, tld="co.in", num=5, stop=5, pause=2):
		results.append(j)
	embed = discord.Embed(title="Google Search", description=f"Results for **{reason}**")
	iteration = 1
	for result in results:
		embed.add_field(name=f"Result {iteration}", value=result, inline=False)
		iteration += 1
	await search_msg.edit(embed=embed)

@client.command(name="resources")
async def resources(ctx, language):
	if not start_stop:
		return
	if language == "python" or language == "Python":
		embed = discord.Embed(title="Python Resources")
		embed.add_field(name="Youtube", value=
		"""[Corey Schafer](https://www.youtube.com/c/Coreyms/playlists)
		[Mosh](https://www.youtube.com/playlist?list=PLTjRvDozrdlxj5wgH4qkvwSOdHLOCx10f)
		[FreeCodeCamp](https://www.youtube.com/playlist?list=PLWKjhJtqVAbnqBxcdjVGgT3uVR10bzTEB)""", inline=False)
		embed.add_field(name="Books", value="[Automate the Boring Stuff with Python](https://automatetheboringstuff.com/2e/chapter0/)", inline=False)
		await ctx.send(embed=embed)




# BEING WORKED ON
@client.command()
async def googlesearchesing(ctx, reason):
	if not start_stop:
		return
	PATH = "C:\Program Files (x86)\chromedriver.exe"
	url = "https://google.com/search?q=" + reason
	headers = {"User Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"}


	embed = discord.Embed(title="Google Search", description=f"Showing results for **{reason}**")
	url = "https://google.com/search?q=" + reason



	r = requests.get(url, headers=headers)
	page = r.content

	soup = BeautifulSoup(page, 'html.parser')

	names = soup.find_all("h3", class_="LC20lb DKV0Md")
	names = names.find_all('span')
	print(names.text)



	for name in names:

		embed.add_field(name=name.text, value=name.text)
	await ctx.send(embed=embed)
# BEING WORKED ON


@client.command(aliases=['quit'])
@commands.has_role('Moderation')
async def q(ctx):
	await ctx.send("Bot is turned off")
	await client.logout()

	




client.run('')
