from discord.ext.commands import Cog
import discord
import asyncio
from main import client



class BumpCog(Cog):
    @Cog.listener()
    async def on_message(self, message):
        disboard = discord.utils.get(message.guild.members, id=302050872383242240)

        if disboard.status == discord.Status.offline:
            return

        if message.channel.id != 797342261507391488:
            return

        if message.author.id == 796195995284406292:
            return

        if message.author.id != 302050872383242240:
            await message.delete()
            return
        
        embed_content = message.embeds[0].description
        bumping = discord.utils.get(message.guild.roles, id=803859911397474354)

        if "Bump done" in embed_content or "👍" in embed_content:
            await asyncio.sleep(2)
            await message.channel.purge(limit=2)
            embed = discord.Embed(title=f"Bump Success",
                                description=f"The server has been bumped! Next bump is in 2 hours\n",
                                color=0x1f4454)
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/796182201976356875/806529281232601107/pandaemoji_1.png')
            await client.get_channel(797342261507391488).send(embed=embed)
        else:
            print(embed_content)
            await message.delete()

def setup(client):
    client.add_cog(BumpCog(client))