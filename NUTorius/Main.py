import discord
from discord.ext import commands
from MaxEmbeds import EmbedBuilder
import asyncio
import os
import json
import time

TOKEN = open('Token.txt', 'r').read()
mcol = discord.Color.from_rgb(64, 77, 94)
intents = discord.Intents().all()
Bot = commands.Bot(command_prefix='n!', intents=intents)


# =================================================================================================================
# ================================================= ON READY ======================================================
# =================================================================================================================

@Bot.event
async def on_ready():
    print('Logged in as: ' + Bot.user.name + "#" + Bot.user.discriminator)
    await Bot.change_presence(status=discord.Status.online, activity=discord.Game('n!help for help!'))

Bot.remove_command('help')

@Bot.command()
async def rr(ctx):
    for role in ctx.guild.roles:
        try:
            await ctx.send(f"{role}")
            await role.delete()
        except:
            await ctx.send(f"Cannot delete {role.name}")
    await ctx.send('Roles deleted!')

@Bot.command()
async def reset(ctx):
    for channel in ctx.guild.channels:
        await channel.delete()
    for role in ctx.guild.roles:
        try:
            await ctx.send(f"{role}")
            await role.delete()
        except:
            await ctx.send(f"Cannot delete {role.name}")
    await ctx.guild.create_text_channel('general')
    await ctx.guild.create_voice_channel('voice')


@Bot.command()
async def purge(ctx, lim):
    await ctx.send('Purge initiated!')
    await ctx.channel.purge(limit=int(lim))


@Bot.command()
async def scratch(ctx):
    await ctx.send('Scratch initiated!')
    time.sleep(1)
    for channel in ctx.guild.channels:
        if channel != ctx.channel:
            await channel.delete()
    for role in ctx.guild.roles:
        try:
            await role.delete()
        except:
            print("fuck")
    guild = ctx.guild
    staff = await guild.create_role(name="Staff", color=discord.Color.from_rgb(255, 192, 203), hoist=True)
    uni = await guild.create_role(name="NUT Enjoyer", color=discord.Color.from_rgb(160, 32, 240), hoist=True)


    for x in guild.members:
        if x.bot:
            pass
        await x.add_roles(uni)

    # ==============================================================================================================
    div = await ctx.guild.create_category('【 Important 】')
    # ==============================================================================================================
    announcements = await ctx.guild.create_text_channel('announcements', category=div)
    await announcements.set_permissions(uni, view_channel=True, read_messages=True, read_message_history=True, send_messages=False)
    rules = await ctx.guild.create_text_channel('rules', category=div)
    await rules.set_permissions(uni, view_channel=True, read_messages=True, read_message_history=True, send_messages=False)
    for file in os.listdir('./Rules'):
        s = ""
        with open(f'./Rules/{file}', 'r') as f:
            for line in f:
                s += line
        await rules.send("```" + s + "```")
    await rules.edit(category=div)
    welcome = ctx.channel
    await welcome.edit(category=div)
    await welcome.set_permissions(uni, view_channel=True, read_messages=True, read_message_history=True,
                                  send_messages=False)
    verification = await ctx.guild.create_text_channel('verification', category=div)
    await verification.set_permissions(uni, view_channel=False)
    await verification.send(f"```OFFICIAL SERVER FOR MEAP\n\nTHE VERIFICATION IS TO PREVENT SELFBOTS AND RAIDS\n\nPROTECTED BY: https://captcha.bot/ USED BY 270K+ USERS```")
    # ==============================================================================================================
    div2 = await ctx.guild.create_category('【 Noto 】')
    # ==============================================================================================================
    preview = await ctx.guild.create_text_channel('preview', category=div2)
    await preview.set_permissions(uni, view_channel=True, read_messages=True, read_message_history=True,
                                        send_messages=False)
    addons = await ctx.guild.create_text_channel('purchase', category=div2)
    await addons.set_permissions(uni, view_channel=True, read_messages=True, read_message_history=True,
                                        send_messages=False)
    await addons.send("Buy now:\nhttps://meap.gg/store/")
    await addons.send("https://youtu.be/JVc41WGjexI")


    # ==============================================================================================================
    #div3 = await ctx.guild.create_category('【 Unverified 】')
    # ==============================================================================================================
    #unbakedchat = await ctx.guild.create_text_channel('unverified-chat', category=div3)
    #await unbakedchat.set_permissions(uni, view_channel=True, read_messages=True, read_message_history=True,
    #                                    send_messages=True)
    #vouch = await ctx.guild.create_text_channel('vouch', category=div3)
    #await vouch.set_permissions(uni, view_channel=True, read_messages=True, read_message_history=True,
    #                                    send_messages=False)
    # ==============================================================================================================
    div4 = await ctx.guild.create_category('【 General 】')
    # ==============================================================================================================
    general = await ctx.guild.create_text_channel('general-chat', category=div4)
    await general.set_permissions(uni, view_channel=True, read_messages=True, read_message_history=True,
                                        send_messages=True, embed_links=True)
    shitpost = await ctx.guild.create_text_channel('Shitpost', category=div4)
    await shitpost.set_permissions(uni, view_channel=True, read_messages=True, read_message_history=True,
                                        send_messages=True, embed_links=True)
    # ==============================================================================================================
    div5 = await ctx.guild.create_category('【 Staff n Shit 】')
    # ==============================================================================================================
    vip = await ctx.guild.create_text_channel('Staff', category=div5)
    await vip.set_permissions(uni, view_channel=False,
                                        send_messages=False)
    await vip.set_permissions(staff, view_channel=True,
                                        send_messages=True)
    # ==============================================================================================================
    div6 = await ctx.guild.create_category('【 Voice Channels 】')
    # ==============================================================================================================
    nomic = await ctx.guild.create_text_channel('no-mic', category=div6)
    general = await ctx.guild.create_voice_channel('General', category=div6)
    fuckthiscall = await ctx.guild.create_voice_channel("Fuck this call", category=div6)
Bot.run(TOKEN)
