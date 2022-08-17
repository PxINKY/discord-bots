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
Bot = commands.Bot(command_prefix='m!', intents=intents)


# =================================================================================================================
# ================================================= ON READY ======================================================
# =================================================================================================================

@Bot.event
async def on_ready():
    print('Logged in as: ' + Bot.user.name)
    await Bot.change_presence(status=discord.Status.online, activity=discord.Game('m!help for help!'))

Bot.remove_command('help')

# =================================================================================================================
# ==================================================== HELP =======================================================
# =================================================================================================================

@Bot.command(help="List all commands and a short description")
async def help(ctx):
    embed = EmbedBuilder(title="**Command list:**",
                         description="**BASIC COMMANDS**:\n"
                                     "**m!help** - Shows this message\n"
                                     "**m!beta** - Shows all beta participants\n"
                                     "**m!whoami** - A brief detailing of myself (Muni Oku)\n"
                                     "\n**VERIFICATION COMMANDS:**\n"
                                     "**m!verify** - For server verification\n"
                                     "\n**INFORMATION COMMANDS**\n"
                                     "**m!mods** - Shows all mods\n"
                                     "**m!world** - Shows world ID and some other information\n"
                                     "**m!search [Arg 1] [Arg 2]** - Searches for a mod\n**>** Arg 1 = ['DID' / 'DTag' / 'VRCLink']\n**>** Arg 2 = [Discord ID / Discord Tag / VRChat Profile Link]\n"
                                     "**m!github** - Sends github link\n"
                                     "**m!dumpjson** - Sends moderators.json\n"
                                     "**m!jsonoutline** - Sends an outline of moderators.json\n",
                         color=mcol,
                         footer=["Bot Made By PxINKY#0001"]
                         ).build()
    await ctx.send(embed=embed)

# =================================================================================================================
# ============================================ GENERAL INFORMATION ================================================
# =================================================================================================================

@Bot.command(help='gives world ID')
async def world(ctx):
    embed = EmbedBuilder(title="Furry Island Resort",
                         description="Link: [Furry Island Resort](https://vrchat.com/home/world/wrld_6195502e-6462-4651-833a-662a408f616c)\n"
                                     "Creator: [Greg The Furry](https://vrchat.com/home/user/usr_d6f6171a-3b60-4da7-8de9-561734af45ae)\n",
                         color=mcol,
                         footer=["ID: wrld_6195502e-6462-4651-833a-662a408f616c\nArt by: Legenragon#9924"]
                         ).build()
    FIR = discord.File(r"./MuniOkuPhotos/Furry_Island_Announcement.png", filename="Furry_Island_Announcement.png")
    embed.set_image(url="attachment://Furry_Island_Announcement.png")
    await ctx.send(embed=embed, file=FIR)


@Bot.command(help="Sends a link to the github repo")
async def github(ctx):
    embed = EmbedBuilder(title="Github Repository",
                         description="Link: [Github](https://github.com/PxINKY/MuniOku)",
                         color=mcol,
                         thumbnail="https://cdn-icons-png.flaticon.com/512/25/25231.png"
                         ).build()
    await ctx.send(embed=embed)


@Bot.command(help="A little bit about me!")
async def whoami(ctx):
    embed = EmbedBuilder(title="Muni Oku",
                         description=f"Hello! im {Bot.user.name}!\nI'm the mascot for FIR\n(Furry Island Resort)\n",
                         color=mcol,
                         thumbnail=Bot.user.avatar_url,
                         footer=["WIP - NEED MORE INFO"]
                         ).build()
    await ctx.send(embed=embed)

# =================================================================================================================
# =============================================== MODERATOR LIST ==================================================
# =================================================================================================================

@Bot.command(help="A list of all moderators and there VRChat links")
async def mods(ctx):
    x = "./Settings/moderators.json"
    m = open(x, 'r')
    modsl = json.load(m)
    embed = EmbedBuilder(title="**All Moderators:**",
                         description="",
                         color=mcol,
                         footer=["WIP LIST"]
                         ).build()
    lissy = ""
    for i in modsl["Moderators"]:
        for x in i["members"]:
            lissy += f"**>** [{x['DiscordTag']}]({x['VRChatLink']})\n"

        if i["GroupName"] == "World Moderator":
            embed2 = EmbedBuilder(title=f"**{i['GroupName']}s**",
                                  description=f"{lissy}",
                                  color=mcol,
                                  footer=["WIP LIST"]
                                  ).build()
        else:
            embed.add_field(name=i["GroupName"], value=f"{lissy}", inline=(
                    i["GroupName"] != "Owner" and i["GroupName"] != "Co-Owner" and i[
                "GroupName"] != "Super Admin" and i["GroupName"] != "Executive Admin"))
        lissy = ""
    await ctx.send(embed=embed)
    if embed2:
        await ctx.send(embed=embed2)
    m.close()

# =================================================================================================================
# =================================================== SEARCH ======================================================
# =================================================================================================================

@Bot.command(help="search for mods")
async def search(ctx, arg):
    identifier = ""

    # arg scanner:

    # VRChat link / profile id
    if arg.startswith("https://"):
        identifier = "VRChatLink"
    elif arg.startswith("usr_"):
        identifier = "VRChatID"
    elif arg in "#":
        identifier = "DiscordTag"
    elif arg.isdecimal():
        identifier = "DiscordID"
    else:
        await ctx.send("Invalid Parameter")
        return

    M = open('./Settings/moderators.json', 'r')
    Mods = json.load(M)
    for i in Mods["Moderators"]:
        for x in i["members"]:
            if x[identifier] == arg:
                them = await Bot.fetch_user(x['DiscordID'])
                embed = EmbedBuilder(title=f"Info for {them.name}#{them.discriminator}",
                                     description=f"[VRChat link]({x['VRChatLink']})\nDiscord Tag: {them.name}#{them.discriminator}\nDiscord ID: {x['DiscordID']}",
                                     color=mcol,
                                     thumbnail=them.avatar_url,
                                     footer=["WIP"]
                                     ).build()
                await ctx.send(embed=embed)
                M.close()
                return
    await ctx.send("No user found or invalid/missing parameter")
    M.close()

# =================================================================================================================
# =============================================== VERIFICATION ====================================================
# =================================================================================================================

@Bot.command(help="Verify yourself to access the rest of the server!")
async def verify(ctx):
    # Channel to send the info to
    # read from Settings/config.json and grab the channel ID
    with open('Settings/config.json', 'r') as f:
        data = json.load(f)
        outputID = data["ModChannel"]
        # to use > inputID = data["VerifyChannel"]
    channel = Bot.get_channel(outputID)

    # Intro embed
    intro = EmbedBuilder(title="Verification",
                         description=f'Hello {ctx.author.name}!\n'
                                     f'Please answer the following 6 questions!\n'
                                     f'After doing so you will be reviewed by staff and allowed in based on application',
                         color=mcol,
                         thumbnail=Bot.user.avatar_url
                         ).build()

    # Verification fail embed
    veriFail = EmbedBuilder(title="Verification Failed!",
                            description=f'You took too long to answer!\nPlease re-apply to be verified!',
                            color=mcol,
                            thumbnail="attachment://error.png"
                            ).build()
    errorpng = discord.File(r"./Resources/error.png", filename="error.png")

    # Verification success embed
    veriComplete = EmbedBuilder(title="Verification sent for review!",
                                description=f'Thank you {ctx.author.name} for your time!\n'
                                            f'Your verification ticket has been successfully sent!\n'
                                            f'Please note that it may take up to 24 hours for staff to review your application',
                                color=mcol,
                                thumbnail="attachment://check.png"
                                ).build()
    complpng = discord.File(r"./Resources/check.png", filename="check.png")

    # load Settings/Questions and put the questions in a list
    ques = []
    allq = []
    f = open('Settings/Questions', 'r')
    for i in f:
        ques.append(i)

    for i in range(0, 6):
        temp = EmbedBuilder(title=f"Question {i + 1}",
                            description=f"{ques[i]}".replace('\\n', '\n'),
                            color=mcol,
                            thumbnail=Bot.user.avatar_url
                            ).build()
        allq.append(temp)

    alla = []
    # check for permission to send direct message
    try:
        await ctx.author.send(embed=intro)
    except discord.Forbidden:
        await ctx.send(
            ctx.author.mention + ", I don't have permission to DM you!\nTo fix this go into\nServer Settings > Server Privacy > Allow Direct Messages from server members",
            delete_after=30)
        await ctx.message.delete()
        return
    # Tell them to check dms
    await ctx.send(f'{ctx.author.mention} Please check your DM\'s!', delete_after=5)
    # Send intro + question 1
    time.sleep(1)
    # try / except statement for timeout and verification fail
    try:
        for i in range(len(allq)):
            await ctx.author.send(embed=allq[i])
            time.sleep(1)
            temp = await Bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60.0)
            alla.append(temp.content)
    except asyncio.TimeoutError:
        await ctx.author.send(embed=veriFail, file=errorpng)
        await ctx.message.delete()
        return

    # Verification success
    user = "NULL"
    icon = "NULL"
    joined = "NULL"
    # https://stackoverflow.com/questions/67469575/discord-py-how-to-get-info-when-member-registered-on-discord-and-joined-server
    date_format = "%a, %b %d, %Y @ %I:%M %p"

    try:
        usr = await Bot.fetch_user(ctx.author.id)
    except:
        pass
    try:
        icon = usr.avatar_url
    except:
        pass
    try:
        joined = ctx.author.joined_at.strftime(date_format)
    except:
        pass
    try:
        user = usr.created_at.strftime(date_format)
    except:
        pass

    veri = f"**Name(s):**\n{alla[0]}\n**Age:**\n{alla[1]}\n**Gender / Pronouns:**\n{alla[2]}\n**Hobbies:**\n{alla[3]}\n**How they found FIR:**\n{alla[4]}\n**Fact(s) about them:**\n{alla[5]}\n**Account Created on:**\n{user}\n**Joined Server on:**\n{joined}"
    veribuild = EmbedBuilder(title=f"Verification for {ctx.author}",
                             description=veri,
                             color=mcol,
                             thumbnail=icon
                             ).build()
    # TODO - Replace ctx.send with channel ID that can be set
    await channel.send("**[**<@&963843804086018099>**]**", embed=veribuild)
    # Alert user that there application was sent
    await ctx.author.send(embed=veriComplete, file=complpng)
    # delete the original message
    await ctx.message.delete()

# =================================================================================================================
# =================================================== UPDATE ======================================================
# =================================================================================================================

@Bot.command(help="Updates the json list with current usernames")
async def update(ctx):
    message = await ctx.send("Updating...")

    x = "./Settings/moderators.json"
    f = open(x, "r")
    data = json.load(f)
    f.close()
    for m in data["Moderators"]:
        for g in m["members"]:
            try:
                user = await Bot.fetch_user(int(g["DiscordID"]))
                g["DiscordTag"] = f'{user.name}#{user.discriminator}'
            except:
                print("User not found")
    # Write the updated json file
    f = open(x, "w")
    f.write(json.dumps(data, indent=4))
    f.close()
    await message.edit(content="Done!")

# =================================================================================================================
# ==================================================== JSON =======================================================
# =================================================================================================================

@Bot.command(help="Sends details on json file")
async def jsonoutline(ctx):
    x = "./Settings/moderators.json"
    f = open(x, "r")
    data = json.load(f)
    f.close()
    s = "[Moderators]\n ↑ [GroupName]\n ↑ [members]\n    ↑ [DiscordTag]\n    ↑ [DiscordID]\n    ↑ [VRChatLink]\n    ↑ [VRChatID]"

    embed = EmbedBuilder(title="JSON File",
        description=f'{s}',
        color=mcol,
        thumbnail="attachment://json.png"
        ).build()
    curl = discord.File(r"./Resources/json.png", filename="json.png")
    await ctx.send(embed=embed, file=curl)


@Bot.command(help="Dumps .json file")
async def dumpjson(ctx):
    x = "./Settings/moderators.json"
    await ctx.send(file=discord.File(x))

# =================================================================================================================
# ==================================================== MISC =======================================================
# =================================================================================================================

@Bot.command(help="Counts channel messages")
async def count(ctx):
    channel = ctx.channel
    await ctx.send(f"{channel.name} has {len(await channel.history(limit=None).flatten())} messages.")


@Bot.command(help="List all participants of beta")
async def beta(ctx):
    f = open('./Settings/beta', 'r')
    betausers = "\n**Beta Participants:**\n"
    for i in f:
        user = await Bot.fetch_user(int(i))
        betausers += f"💎 {user.name}#{user.discriminator} - {user.id}\n"
    f.close()
    embed = EmbedBuilder(title="**Big thanks to everyone who participated in the beta!**",
                         description=f"{betausers}",
                         color=mcol,
                         thumbnail=f"attachment://beta.png",
                         footer="Bot Made By PxINKY#0001"
                         ).build()
    betapng = discord.File(r"./Resources/beta.png", filename="beta.png")
    await ctx.send(embed=embed, file=betapng)


Bot.run(TOKEN)
