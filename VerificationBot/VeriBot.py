# funny bot
import discord
from discord.ext import commands
from MaxEmbeds import EmbedBuilder
import asyncio
import os
import random
import json
import time

TOKEN = open('Token.txt', 'r').read()
#mcol = discord.Color.from_rgb(64, 77, 94)
intents = discord.Intents().all()
Bot = commands.Bot(command_prefix='v!', intents=intents)
STRING_FRUIT = ['🍎', '🍌', '🍇', '🍊', '🍋', '🍑', '🍈', '🍒']
global CHOICE_FRUIT
CHOICE_FRUIT = "blah"
FRUIT_NAME = ['Apple', 'Banana', 'Grape', 'Orange', 'Lemon', 'Peach', 'Melon', 'Cherry']
FRUIT_THEM = []
FRUIT_ME = []
FRUIT_IDS = []
# =================================================================================================================
# ================================================= ON READY ======================================================
# =================================================================================================================


@Bot.event
async def on_ready():
    print('Logged in as: ' + Bot.user.name)
    await Bot.change_presence(status=discord.Status.online, activity=discord.Game('v!help for help'))

Bot.remove_command('help')


# =================================================================================================================
# ============================================== ANNOYING SHIT ====================================================
# =================================================================================================================


@Bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content != '':
        FRUIT_THEM.clear()
        FRUIT_ME.clear()
        # deletes the message
        await message.delete()
        # role to delete
        role = discord.utils.get(Bot.get_guild(917029556882382850).roles, name="Test")
        await message.author.add_roles(role)
        with open('./Config/ReCount', 'r') as f:
            ReCount = f.read()

        for x in range(0, int(ReCount)):
            random_fruit = random.randint(0, 7)
            react = await message.channel.send(f'{message.author.mention} Please wait...')
            FRUIT_ME.append(STRING_FRUIT[random_fruit])
            for m in STRING_FRUIT:
                fruit = await react.add_reaction(m)

            await react.edit(content=f'{message.author.mention} you must verify first!\nPlease select the **{FRUIT_NAME[random_fruit]}** {x+1}/{ReCount}')
            # https://stackoverflow.com/questions/70660987/discord-py-wait-for-message-or-reaction
            await asyncio.wait([
                Bot.loop.create_task(Bot.wait_for('reaction_add', check=lambda reaction, user: user == message.author)),
            ], return_when=asyncio.FIRST_COMPLETED)
            await react.delete()
        if FRUIT_ME == FRUIT_THEM:
            await message.channel.send(f'{message.author.mention} you are verified!')
            await message.author.remove_roles(role)
        else:
            await message.channel.send(f'{message.author.mention} you are not verified!')
    else:
        await Bot.process_commands(message)


@Bot.event
async def on_reaction_add(reaction, user):
    if user != Bot.user:
        for x in STRING_FRUIT:
            if str(reaction.emoji) == x:
                global CHOICE_FRUIT
                CHOICE_FRUIT = x
                FRUIT_THEM.append(CHOICE_FRUIT)






# run the bot from TOKEN
Bot.run(TOKEN)