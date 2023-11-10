import discord # Подключаем библиотеку
from discord.ext import commands
from tk import token

intents = discord.Intents.default() # Подключаем "Разрешения"
intents.message_content = True
# Задаём префикс и интенты
bot = commands.Bot(command_prefix='>', intents=intents) 

hello_words = ['hello', 'hi', ' privet', 'ky', "привет", "здарова"]

@bot.event
async def on_ready():
    print('Bot connected')

# С помощью декоратора создаём первую команду
@bot.command(pass_context = True)
async def botic(ctx, arg):
    if arg:
        author = ctx.message.author
        # response_text = f'{author.mention} + arg бот!!' * 10
        # response_text = f'{author.mention}' + arg
        response_text = f'{arg} бот!! \n'
    else:
        response_text = 'Введи текст після команди >botic'
    for i in range(10):
        await ctx.send(response_text)

@bot.event
async def on_message(message):
    msg = message.content.lower()
    if msg in hello_words:
        await message.channel.send('Hi. What do you want?')

bot.run(token)