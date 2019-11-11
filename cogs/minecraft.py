import discord
import mcstatus
from discord import Embed
from discord.ext import commands
import re
import core.util.HelpEntries as HE
import socket

class Minecraft(commands.Cog):
    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot
        print("Minecraft cog loaded")

    @commands.command(pass_context=True)
    async def jping(self, ctx: discord.ext.commands.Context, url: str):
        server = mcstatus.MinecraftServer.lookup(url)
        status = server.status()
        e = Embed()
        e.title = url
        e.description = re.sub("§.", "", status.description)
        e.add_field(name="Players", value=str(status.players.online) + "/" + str(status.players.max))
        e.add_field(name="Ping", value=str(status.latency))
        e.add_field(name="Version", value=status.version.name)
        e.add_field(name="Protocol", value="v" + str(status.version.protocol))
        await ctx.send(embed=e)

    @commands.command(pass_context=True)
    async def bping(self, ctx: discord.ext.commands.Context, url: str, port: int):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(bytearray.fromhex(
                "0100000000003c6d0d00ffff00fefefefefdfdfdfd12345678"), (url, port))
            data, addr = sock.recvfrom(255)
            status = data[35::].decode("ISO-8859-1").split(";")
            e = Embed()
            e.title = url
            e.description = re.sub("[§Â].", "", status[1])
            e.add_field(name="Players", value=status[4] + "/" + status[5])
            e.add_field(name="Version", value=status[3])
            e.add_field(name="Protocol", value="v" + status[2])
            e.add_field(name="World Name",value=re.sub("§.", "", status[7]))
            e.add_field(name="Default Gamemode",value=status[8])
            await ctx.send(embed=e)
        except:
            await ctx.send("Error")


def setup(bot):
    bot.add_cog(Minecraft(bot))
    HE.HelpEntries.register("jping", ["%jping server","%jping server:port"], "Pings a java server")
    HE.HelpEntries.register("bping", "%bping server port", "Pings a bedrock server")
