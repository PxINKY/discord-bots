import asyncio
import time
import discord
from discord.ext import commands
from MaxEmbeds import EmbedBuilder
import requests
from discord.utils import get
from PIL import Image
import zipfile
import imageio
import os

dirs = ["Zip", "Export", "Overflow", "PFP", "Resources"]
for x in dirs:
    try:
        os.mkdir(""+x)
        print("made: " + x)
    except FileExistsError:
        print("already exists")

os.chdir("PFP")
if not os.path.exists("image_name.png"):
    img_data = requests.get("https://cdn.discordapp.com/icons/991276314885636206/27eabcdc454934e4d4a4af8c8bc3d85d.png?size=1024").content
    with open('image_name.png', 'wb') as handler:
        handler.write(img_data)
    handler.close()
    print("made: image_name.png")
os.chdir("../")
os.chdir("Resources")
for x in ["dodofard.png", "horny.png"]:
    img_data = requests.get("https://cdn.discordapp.com/attachments/991404765265264711/991404986091188315/horny.png").content
    with open(f'{x}', 'wb') as handler:
        handler.write(img_data)
    handler.close()
    print("made: " + x)
os.chdir("../")
intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='pink', intents=intents, activity=discord.Activity(type=discord.ActivityType.watching, name="Over Pink Penthouse"), )
mcol = discord.Color.from_rgb(250, 144, 255)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}#{bot.user.discriminator}')

@bot.command(help="Prints details of Server")
async def info(ctx):
    owner = str(ctx.guild.owner)
    guild_id = str(ctx.guild.id)
    memberCount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon.url)
    desc = ctx.guild.description
    date_format = "%a, %b %d, %Y @ %I:%M %p"
    embed = discord.Embed(
        title=ctx.guild.name + " Server Information",
        description=desc,
        color=mcol
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=guild_id, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)

    l = []
    z = []
    for member in ctx.guild.members:
       l.append(member.id)

    for x in l:
        usr = ctx.guild.get_member(x)
        z.append(f'{usr.name}#{usr.discriminator} - {usr.joined_at}')

    #for i in z:

    z.sort(key=lambda x: x.split(' - ')[1])
    for x in z:
        z[z.index(x)] = x.split(' - ')[0]
    embed.add_field(name="First 10 Members", value='\n'.join(z[:10]), inline=True)
    await ctx.send(embed=embed)

    embed = EmbedBuilder(title=f'**More information on {ctx.guild.owner.name}**',
                         description=f'**__Name:__** {ctx.guild.owner.name}#{ctx.guild.owner.discriminator}\n**__ID:__** {ctx.guild.owner.id}\n**__Created on:__** {ctx.guild.owner.created_at.strftime(date_format)}\n**__Joined on:__** {ctx.guild.owner.joined_at.strftime(date_format)}',
                         thumbnail=f'{ctx.guild.owner.avatar.url}',
                         color=mcol).build()
    await ctx.send(embed=embed)


@bot.command(help="new channel")
async def comm(ctx, user: discord.User):
    role = bot.get_guild(ctx.guild.id).get_role(991286366728093746)
    if role in ctx.author.roles:
        guild = ctx.guild
        # 993319126703554630
        Comm = bot.get_channel(993319126703554630)
        CommChannel = await guild.create_text_channel(name=user.name, category=Comm)
        await CommChannel.set_permissions(user, view_channel=True)
        await CommChannel.send(user.mention)
        embed = EmbedBuilder(title=f"{ctx.author}'s Commission",
                             description=f"Want to know if i own an asset?\nTry: **pinkgumroad [link to asset]**\n> Adding accessories will be a base of 2$\n"
                                         f"> Clothing items are 5$ each if owned\n> If i do not own the asset it'll cost the price of the asset + 2$ to add it\n> If i do not own the model, you can buy it for me and in exchange i will provide the commission for free (if its simple enough)\n\n\n**What i can do:**\nRetexturing\nUnity Setup\nQuest + PC uploads"
                                         f"\nVery Very Basic Blender\n\n\n**Prices:**\n__Retexturing:__\nBasic recolor - $20\nSemi-Complex Designs - $35\nComplex Designs - $50\nExtremely Complex Designs - $70+"
                                         f"\n\n__Unity:__\nSimple Upload - 10$\nToggles - 2$ Per (Discounts On Larger Amounts)\nQuest Upload - 10$\nCustom Logic - 5$"
                                         f"\n\n**Payment methods i accept:**\n[PayPal](https://paypal.me/pxinky?country.x=CA&locale.x=en_US)\nPxINKY.business@gmail.com\n[Ko-fi](https://ko-fi.com/pxinky)"
                                         f"\n\n\n**PLEASE SPECIFY EVERYTHING YOU WANT BEFORE WE START, AS WHEN THE PRICE IS PLACED I WILL NOT BE ADDING MORE UNLESS ADDITIONAL PAYMENT IS PROVIDED**\n(Touch-ups and mistakes caused by me will be free to fix)",
                             color=mcol,
                             footer=[f"Commission for {user}"],
                             thumbnail=ctx.author.avatar.url
                             ).build()
        await CommChannel.send(embed=embed)
    else:
        await ctx.send("You do not have permission to use this command")

@bot.command(help="gumroad link")
async def gumroad(ctx, link):
    gum = []
    owned = False
    os.chdir("Resources")
    with open('gumroad.txt', 'r') as handler:
        for x in handler.readlines():
            gum.append(x.strip("\n"))
    if "?" in link:
        link = link.split("?")[0]
    for x in gum:
        if x is link or x in link:
            owned = True
        else:
            pass
    if owned:
        await ctx.send("Asset is owned!")
    else:
        await ctx.send("Asset unowned :<")
    os.chdir("../")


@bot.command(help="review")
async def review(ctx, user: discord.User):
    role = bot.get_guild(ctx.guild.id).get_role(991286366728093746)
    if role in ctx.author.roles:
        for channel in ctx.guild.channels:
            if channel.id == 1003036881916805260:
                reviewChannel = channel
        questions = []
        qts = []
        os.chdir("Resources")
        with open('questions', 'r') as handler:
            for x in handler.readlines():
                qts.append(x.strip("\n"))
        answers = []
        for i in range(0, 7):
            temp = EmbedBuilder(title=f"Question {i + 1}",
                                description=f"{qts[i]}",
                                color=mcol,
                                thumbnail=bot.user.avatar.url
                                ).build()
            questions.append(temp)

        alla = []
        # check for permission to send direct message
        try:
            await user.send(f"Hello I Will ask you 7 questions!\nPlease be aware each question will have a 3 minute timer on it\nValid answers for 0-5 questions are the following:\n```0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5```\n0 Being the worst and 5 Being the best")
        except discord.Forbidden:
            await ctx.send(
                ctx.author.mention + ", I don't have permission to DM you!\nTo fix this go into\nServer Settings > Server Privacy > Allow Direct Messages from server members",
                delete_after=30)
            await ctx.message.delete()
            return
        # Send intro + question 1
        time.sleep(1)
        # try / except statement for timeout and verification fail
        try:
            for i in range(len(questions)):
                await user.send(embed=questions[i])
                time.sleep(1)
                temp = await bot.wait_for('message', check=lambda message: message.author == user and message.guild is None, timeout=180.0)
                alla.append(temp.content)
        except asyncio.TimeoutError:
            await ctx.message.delete()
            return

        if int(alla[0]) == 1:
            alla[0] = "PxINKY"
        elif int(alla[0]) == 2:
            alla[0] = "Arktiss"
        else:
            alla[0] = "Arktiss and PxINKY"

        star = '<:star:1003038760033861693>'
        halfstar = '<:halfstar:1003038772813901984>'
        ratings = ["hold", "hold", "hold", "hold", "hold"]
        for i in range(1, 5):
            temp = float(alla[i])
            temp = temp * 2
            print(temp)
            ratings[i] = ""
            if temp % 2 == 1:
                temp -= 1
                for x in range(0, int(temp / 2)):
                    ratings[i] += star
                ratings[i] += halfstar
            else:
                for x in range(0, int(temp / 2)):
                    ratings[i] += star
        finalEmbed = EmbedBuilder(title=f"{user.name}'s **Review**",
                                  description=f"**Commission done by: {alla[0]}**\n"
                                  f"**Communication:**\n{ratings[1]}\n"
                                  f"**Price:**\n{ratings[2]}\n"
                                  f"**Result:**\n{ratings[3]}\n"
                                  f"**Overall:**\n{ratings[4]}\n"
                                  f"\n**Would you consider commissioning again?**:\n{alla[5]}\n"
                                  f"\n**Additional feedback:**\n{alla[6]}",
                                  color=mcol,
                                  thumbnail=user.avatar.url,
                                  footer=[f"{user} - {user.id}"]
        ).build()

        await reviewChannel.send(embed=finalEmbed)
        os.chdir("../")
    else:
        await ctx.send(ctx.author.mention + ", you do not have permission to use this command!")
        await ctx.message.delete()


@bot.command(help="Prints details of User")
async def who(ctx, *arg):
    if len(arg) == 0:
        user = ctx.author.id
    else:
        user = arg[0]


    user = ''.join(c for c in str(user) if c.isdigit())

    try:
        usr = await bot.fetch_user(user)
    except:
        await ctx.send("Invalid parameter")
        return

    store = ""
    guilds = bot.guilds
    for guild in guilds:
        guild = bot.get_guild(guild.id)
        for member in guild.members:
            if member.id == usr.id:
                store = member

    try:
        game = store.activity.name
    except:
        game = "None"

    try:
        status = store.status
    except:
        status = "None"

    try:
        nick = store.nick
    except:
        nick = "None"

    try:
        banner = f"**[Banner]({usr.banner.url})**"
    except:
        banner = "No Banner"

    try:
        pfp = f"**[Avatar]({usr.avatar.url})**"
    except:
        pfp = "No Avatar"

    try:
        thumb = usr.avatar.url
    except:
        thumb = "https://shop.yungcz.com/wp-content/uploads/2020/12/app-icons-discord.png"

    embed = EmbedBuilder(title=f'**{usr.name}#{usr.discriminator}**',
                            description=f'**ID:** {usr.id}\n**Nickname:** {nick}\n**Status:** {status}\n**Activity:** {game}\n{pfp}\n{banner}',
                            thumbnail=f'{thumb}',
                            footer=[f'Account created on: {usr.created_at.strftime("%a, %b %d, %Y @ %I:%M %p")}'],
                            color=mcol).build()
    await ctx.send(embed=embed)


@bot.command(help="Purge")
async def purge(ctx, limit: int):
    role = bot.get_guild(ctx.guild.id).get_role(991286366728093746)
    if role in ctx.author.roles:
        await ctx.channel.purge(limit=limit)
        await ctx.message.delete()
        await ctx.send('Purge requested by {}'.format(ctx.author.mention))
    else:
        await ctx.send("You do not have permission to use this command")


@bot.command(help="Generate custom icon")
async def hornify(ctx, *message):
    channel = ctx.channel
    member = ctx.author
    ava = False
    try:
        ctx.message.attachments[0].url
    except:
        ava = True
    if ava:
        try:
            user = await bot.fetch_user(message[0])
        except:
            user = await bot.fetch_user(member.id)
        try:
            PFPUrl = user.avatar.url
            img_data = requests.get(PFPUrl).content
            os.chdir("PFP")
            with open('image_name.png', 'wb') as handler:
                handler.write(img_data)
            handler.close()
            img2 = Image.open(r"image_name.png")
            os.chdir("../")
            os.chdir("Resources")
            img1 = Image.open(r"horny.png")
            os.chdir("../")
        except:
            print("Brokie")
    else:
        try:
            os.chdir("Resources")
            img1 = Image.open(r"horny.png")
            os.chdir("../")
            img_data = requests.get(ctx.message.attachments[0].url).content
            os.chdir("PFP")
            with open('image_name.png', 'wb') as handler:
                handler.write(img_data)
            handler.close()
            img2 = Image.open(r"image_name.png")
            os.chdir("../")
        except:
            print("shitcoder")
    try:
        img2 = img2.resize((140, 140))
        img1.paste(img2, (53, 139))
        os.chdir("Resources")
        img1.save("dodofard.png")
        os.chdir("../")
    except:
        print("somtingwong")
    os.chdir("Resources")
    await channel.send(file=discord.File(r"dodofard.png"))
    os.chdir("../")

@bot.command(help="Dumps users info and pfp into .zip")
async def dump(ctx, userid):
    user = await bot.fetch_user(userid)
    banner = True
    date_format = "%a, %b %d, %Y @ %I:%M %p"
    os.chdir("Zip")
    for x in os.listdir("."):
        os.remove(f"{x}")
    try:
        game = user.activity.name
    except:
        game = "None"

    try:
        status = user.status
    except:
        status = "None"

    try:
        bannerURL = user.banner.url
    except:
        bannerURL = "No Banner"

    try:
        pfp = user.avatar.url
    except:
        pfp = "No Avatar"

    try:
        with open('info.txt', 'w') as handler:
            handler.write(f"info for {user}\n\n"
                          f"Name: {user.name}\n"
                          f"Discriminator : {user.discriminator}\n"
                          f"Avatar URL: {pfp}\n"
                          f"Banner URL: {bannerURL}"
                          f"Account created on: {user.created_at.strftime(date_format)}\n"
                          f"Status: {status}\n"
                          f"Activity: {game}")
        handler.close()
    except:
        print("pyshit dev")

    try:
        banner_url = user.banner.url  # The URL of the banner
    except:
        await ctx.send("No banner")
        banner = False
    pfp_url = user.avatar.url
    if banner:
        img_data = requests.get(banner_url).content
        with open('banner.gif', 'wb') as handler:
            handler.write(img_data)
        handler.close()
        with open('banner.png', 'wb') as handler:
            handler.write(img_data)
        handler.close()
    img_data = requests.get(pfp_url).content
    with open('avatar.gif', 'wb') as handler:
        handler.write(img_data)
    handler.close()
    with open('avatar.png', 'wb') as handler:
        handler.write(img_data)
    handler.close()
    os.chdir("../")
    os.chdir("Export")
    zf = zipfile.ZipFile(f"{user.name}.zip", "w")
    os.chdir("../")
    for dirname, subdirs, files in os.walk("Zip"):
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
    zf.close()
    try:
        os.chdir("Export")
        await ctx.send(file=discord.File(rf"{user.name}.zip"))
        os.chdir("../")
    except:
        os.chdir("Export")
        await ctx.send("File size exceedes 8MB, Backed up to overflow")
        # cp for linux | copy for windows
        os.popen(f'cp {user.name}.zip ..\\Overflow\\{user.name}.zip')
        os.chdir("../")


@bot.command(help="checkin")
async def verify(ctx, member: discord.Member=None):
    role = bot.get_guild(ctx.guild.id).get_role(991400941012131950)
    message = await ctx.send("verifying...")
    if role in ctx.author.roles:
        await message.edit(content="You are already verified!")
        return
    else:
        await ctx.author.add_roles(role)
        await message.edit(content="Verified!")


# this command will remove the users ability to access the channel it was typed in
@bot.command(help="Close a Commission Channel")
async def close(ctx, user: discord.Member=None):
    role = bot.get_guild(ctx.guild.id).get_role(991286366728093746)
    if role in ctx.author.roles:
        await ctx.channel.set_permissions(user, view_channel=False)
        await ctx.send("Removed access to channel")
        # get vaulted categroy
        category = bot.get_guild(ctx.guild.id).get_channel(999858545380044903)
        await ctx.channel.edit(name=f"{ctx.channel.name} - Closed", category=category)
    else:
        await ctx.send("You do not have permission to use this command")


@bot.command(help="Request 18+ role")
async def nsfw(ctx):
    role = bot.get_guild(ctx.guild.id).get_role(1008245887438430328)
    channel = bot.get_guild(ctx.guild.id).get_channel(1008472518270668820)
    if role in ctx.author.roles:
        await ctx.send("You already have the role")
        return
    else:
        await channel.send(f"{ctx.author.mention} wants the 18+ role")


@bot.command(help="Request 18+ role")
async def nsfwplus(ctx):
    role = bot.get_guild(ctx.guild.id).get_role(1008647849162063892)
    role2 = bot.get_guild(ctx.guild.id).get_role(1008245887438430328)
    channel = bot.get_guild(ctx.guild.id).get_channel(1008472518270668820)
    if role in ctx.author.roles:
        await ctx.send("You already have the role")
        return
    elif role2 in ctx.author.roles:
        #assign role to user
        await ctx.author.add_roles(role)
    else:
        await channel.send(f"{ctx.author.mention} wants the **18+PLUS** role")


@bot.command(help="bals")
async def check(ctx):
    await ctx.send(os.listdir())


@bot.event
async def on_member_join(member):
    guild = bot.get_guild(991276314885636206)
    channel = guild.get_channel(991276867334189096)
    os.chdir("PFP")
    for x in os.listdir("."):
        os.remove(x)
    try:
        user = await bot.fetch_user(member.id)
        PFPUrl = user.avatar.url
        img_data = requests.get(PFPUrl).content
        with open('image_name.png', 'wb') as handler:
            handler.write(img_data)
        handler.close()
    except:
        print("Brokie")
    img2 = Image.open(r"image_name.png")
    os.chdir("../")
    os.chdir("Resources")
    img1 = Image.open(r"horny.png")
    os.chdir("../")
    try:
        img2 = img2.resize((140, 140))

        os.chdir("PFP")
        img1.paste(img2, (53, 139))
        img1.save("dodofard.png")
        os.chdir("../")
    except:
        print("somtingwong")
    os.chdir("PFP")
    await channel.send(f"{member.mention}\n```Welcome to the Pink Penthouse\nDont forget to grab your member card!\nRemember to enjoy your stay ;3```", file=discord.File(r"dodofard.png"))
    os.chdir("../")






if __name__ == "__main__":
    bot.run("Token Here")