import discord
from discord.ext.commands import Cog
from main import client


class ReactionRoles(Cog):

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = client.get_guild(796139098086703145)
        if payload.message_id == 812829587582615574:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)
            await payload.member.add_roles(role)
        elif payload.message_id == 817272465285709844:
            if payload.emoji.name == "🎉":
                await payload.member.add_roles(discord.utils.get(guild.roles, name="Announcements"))
            elif payload.emoji.name == "🤖":
                await payload.member.add_roles(discord.utils.get(guild.roles, name="Bump"))
    
    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = client.get_guild(796139098086703145)
        if payload.message_id == 812829587582615574:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)
            member = discord.utils.get(guild.members, id=payload.user_id)
            await member.remove_roles(role)
        elif payload.message_id == 817272465285709844:
            if payload.emoji.name == "🎉":
                member = discord.utils.get(guild.members, id=payload.user_id)
                await member.remove_roles(discord.utils.get(guild.roles, name="Announcements"))
            elif payload.emoji.name == "🤖":
                member = discord.utils.get(guild.members, id=payload.user_id)
                await member.remove_roles(discord.utils.get(guild.roles, name="Bump"))


def setup(client):
    client.add_cog(ReactionRoles(client))