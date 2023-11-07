import discord
from discord.ext import commands
from tk import token

# Указываем интенты для вашего бота
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

# Создаем экземпляр клиента бота
bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} подключился к Discord!')
    
# @bot.event
# async def on_message(message):
#     print(f'Received message: {message.content}')  # Add this line for debugging
#     if message.content.startswith('!'):
#         text = message.content[1:]
#         response_text = f'{text} бот ' * 10
#         await message.channel.send(response_text)
#     await bot.process_commands(message)

# @bot.command(pass_context = True)
# async def on_message(message):
#     print(f'Received message: {message.content}')
#     response_text = f'{message.content} бот!! ' * 10
#     await message.channel.send(response_text)

@bot.event
async def hello(ctx):
    print(f'Received message: {ctx.content}')
    await ctx.send('hello')

# Токен вашего бота, который нужно получить на https://discord.com/developers/applications
bot.run(token)
