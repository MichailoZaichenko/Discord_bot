import discord
from discord.ext import commands
from token.py import token as tk

# Указываем интенты для вашего бота
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

# Создаем экземпляр клиента бота
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} подключился к Discord!')
    
# @bot.event
# async def on_message(message):
#     print(f'Received message: {message.content}')  # Add this line for debugging
#     if message.content.startswith('!'):
#         text = message.content[1:]
#         if text.startswith('[') and text.endswith(']'):
#             text_inside_brackets = text[1:-1]
#             response_text = f'{text_inside_brackets} бот!! ' * 10
#             await message.channel.send(response_text)
#     await bot.process_commands(message)

@bot.command()
async def on_message(message):
    print(f'Received message: {message.content}')
    response_text = f'{message.content} бот!! ' * 10
    await message.channel.send(response_text)

# Токен вашего бота, который нужно получить на https://discord.com/developers/applications
token = tk

# Запускаем бота
bot.run(token)
