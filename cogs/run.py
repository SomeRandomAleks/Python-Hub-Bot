import discord
from discord.ext import commands
from discord.ext.commands import Cog
from resources import *
from main import client


class Run(Cog):
	
	@Cog.command()
	@commands.has_role('Moderation')
	async def start(ctx):
		global start_stop
		if start_stop:
			await ctx.send("Bot is already on")
			return

		start_stop = True
		await ctx.send("Bot has been started")
		await client.get_channel(log_channel).send(f"{ctx.author.name} has used !start")
	
	@Cog.command()
	@commands.has_role('Moderation')
	async def stop(ctx):
		global start_stop
		if not start_stop:
			await ctx.send("Bot is already off")
			return

		start_stop = False
		await ctx.send("Bot has been stopped")
		await client.get_channel(log_channel).send(f"{ctx.author.name} has used !stop")


def setup(client):
	client.add_cog(Run(client))