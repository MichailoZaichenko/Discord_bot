import discord # Подключаем библиотеку
from discord.ext import commands
from tk import token
import random

intents = discord.Intents.default() # Подключаем "Разрешения"
intents.message_content = True
# add prefix
PREFIX = '>'
# Задаём префикс и интенты
bot = commands.Bot(command_prefix= PREFIX , intents=intents) 
bot.remove_command("help")
# lists for commands
hello_words = ['hello', 'hi', ' privet', 'ky', "привет", "здарова"]
yaki_ti_Woddy = ['bot', 'lox', 'pidr', 'shluxa']
# Announsment about connecting bot to server
@bot.event
async def on_ready():
    print('Bot connected')

# С помощью декоратора создаём первую команду
@bot.command(pass_context = True)
async def botic(ctx, arg):
    try:
        author = ctx.message.author
        # response_text = f'{author.mention} + arg бот!!' * 10
        # response_text = f'{author.mention}' + arg
        random_option = random.choice(yaki_ti_Woddy)
        response_text = f'{arg} {random_option}!! \n'
    except TypeError:
        response_text = 'Введи текст після команди >botic'
    for i in range(10):
        await ctx.send(response_text)

# @bot.event
# async def on_message(message):
#     msg = message.content.lower()
#     if msg in hello_words:
#         await message.channel.send('Hi. What do you want?')

# help command
@bot.command(pass_context = True)
async def help(ctx):
    emb = discord.Embed(title = "Navigation be commands")

    emb.add_field(name='{}hello'.format( PREFIX ), value = 'If you write greetings into chat it will answer')
    emb.add_field(name='{}clear'.format( PREFIX ), value ="Chat clear")
    emb.add_field(name='{}kick'.format( PREFIX ), value ="Kick from the server")
    emb.add_field(name='{}ban'.format( PREFIX ), value = ' Ban from server')
    emb.add_field(name='{}unban'.format( PREFIX ), value = 'Unban')
    emb.add_field(name='{}botic'.format( PREFIX ), value = "Shits some one you write")

    await ctx.send( embed = emb)

# Del messages
@bot.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def clear(ctx, amount=100):
    await ctx.channel.purge(limit = amount)

# Hello to user
@bot.command(pass_context =True)
async def hello(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)

    author = ctx.message.author
    await ctx.send(f'Hello {author.mention}')

# Ban
@bot.command(pass_context = True)
@commands.has_permissions(administrator = True)

async def ban(ctx, member: discord.Member, *, reason = None):
    await ctx.channel.purge(limit = 1)
    await member.ban(reason=reason)
    await ctx.send(f'ban user {member.mention}')

# UnBan
@bot.command(pass_context = True)
@commands.has_permissions(administrator = True)

async def unban(ctx, *, member):
    await ctx.channel.purge(limit = 1)
    # banned users list
    banned_users = await ctx.guild.bans()
    # user from list
    for ban_entry in banned_users:
        user = ban_entry.user
        # unban user
        await ctx.guild.unban(user)
        await ctx.send(f'unban user {member.mention}')
        return

# Kick
@bot.command(pass_context = True)
@commands.has_permissions(administrator = True)

async def kick(ctx, member: discord.Member, *, reason = None):
    await ctx.channel.purge(limit = 1)
    await member.kick(reason=reason)
    await ctx.send(f'kick user {member.mention}')


bot.run(token)