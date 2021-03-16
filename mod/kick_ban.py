import discord
from discord.ext import commands
from discord.ext.commands import Cog
from main import client


class ModerationCog(Cog):

	@commands.command()
	@commands.has_role("Moderation")
	async def kick(self, ctx, member : discord.Member, *, reason=None):
		if not start_stop:
			return
		await member.kick(reason=reason)

		guild = client.get_guild(ctx.author.guild.id)
		embed = discord.Embed(title=f"{member} was kicked", description=f"{ctx.author.mention} has kicked {member}\nReason: {reason}", color=0x1f4454)
		embed.set_thumbnail(url=member.avatar_url)
		embed.set_footer(text=f"We are now at {guild.member_count} members")

		await ctx.send(embed=embed)

	@commands.command()
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, member : discord.Member, reason=None):
		if not start_stop:
			return
		await member.ban(reason=reason)
		embed = discord.Embed(title='Member Banned', description=f'{member} has been banned by {ctx.author}', color=0x1f4454)
		embed.set_thumbnail(url=ctx.author.avatar_url)
		await ctx.send(embed=embed)



	@commands.command()
	@commands.has_permissions(ban_members=True)
	async def unban(self, ctx, *, user_old=None):
		if not start_stop:
			return

		try:
			user = await commands.converter.UserConverter().convert(ctx, user_old)
		except:
			await ctx.send("Error: user could not be found!")
			return

		try:
			bans = tuple(ban_entry.user for ban_entry in await ctx.guild.bans())
			if user in bans:
				await ctx.guild.unban(user, reason="Responsible moderator: "+ str(ctx.author))
				await ctx.send(
					embed = discord.Embed(
						title="Unban",
						description=f"{ctx.author.mention} unbanned {user_old}",
						color=0xffffff
					)
				)
				await client.get_channel(logs_channel).send(
					embed = discord.Embed(
						title="Unban",
						description=f"{ctx.author.mention} unbanned {user_old}",
						color=0xffffff
					)
				)
			else:
				await ctx.send("User not banned!")
				return

		except discord.Forbidden:
			await ctx.send("I do not have permission to unban!")
			return

		except:
			await ctx.send("Unbanning failed!")
			return

def setup(client):
	client.add_cog(ModerationCog(client))

