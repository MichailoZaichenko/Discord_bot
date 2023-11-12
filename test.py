import discord # Подключаем библиотеку
from discord.ext import commands
from tk import token
import random

intents = discord.Intents.default() # Подключаем "Разрешения"
intents.message_content = True
# Задаём префикс и интенты
bot = commands.Bot(command_prefix='>', intents=intents) 

hello_words = ['hello', 'hi', ' privet', 'ky', "привет", "здарова"]
yaki_ti_Woddy = ['bot', 'lox', 'pidr', 'shluxa']

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

# Удоление сообщений
@bot.command(pass_context = True)
async def clear(ctx, amount=100):
    await ctx.channel.purge(limit = amount)

# Удаление команд
@bot.command(pass_context =True)
async def hello(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)

    author = ctx.message.author
    await ctx.send(f'Hello {author.mention}')

bot.run(token)