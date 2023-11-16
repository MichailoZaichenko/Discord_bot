import discord  # Подключаем библиотеку
from discord.ext import commands
import random
import keep_alive
import datetime
from tk import token
import g4f

intents = discord.Intents.default()  # Подключаем "Разрешения"
intents.message_content = True
# add prefix
PREFIX = '>'
# Задаём префикс и интенты
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
bot.remove_command("help")
# lists for commands
hello_words = ['hello', 'hi', ' privet', 'ky', "привет", "здарова"]
yaki_ti_Woddy = [
    'bot', 'lox', 'pidr', 'shluxa', 'довбень', 'довбограй', 'уїбан', 'уйобище',
    'лошара', 'хуйло', 'хуйлуша', 'поїбанець', 'уйобок'
]


# Announsment about connecting bot to server
@bot.event
async def on_ready():
  print('Bot connected')


# С помощью декоратора создаём первую команду
@bot.command(pass_context=True)
async def botic(ctx, arg):
  try:
    author = ctx.message.author
    # response_text = f'{author.mention} + arg бот!!' * 10
    # response_text = f'{author.mention}' + arg
    random_option = random.choice(yaki_ti_Woddy)
    if arg.lower() in [
        'micha', 'миша', 'misha', 'міша', 'm1sha', 'мішаня', 'mishanya', 'mishaloh', 'mishaBomjik', 'mishapozornik', 'mishalosharik']:
      arg = "Бодя"
    response_text = f'{arg} {random_option}!! \n'
  except TypeError:
    response_text = 'Введи текст після команди >botic'
  for i in range(5):
    await ctx.send(response_text)


# @bot.event
# async def on_message(message):
#     msg = message.content.lower()
#     if msg in hello_words:
#         await message.channel.send('Hi. What do you want?')


# help command
@bot.command(pass_context=True)
async def help(ctx):
  emb = discord.Embed(title="Navigation be commands")

  emb.add_field(name='{}hello'.format(PREFIX),
                value='If you write greetings into chat it will answer')
  emb.add_field(name='{}clear'.format(PREFIX), value="Chat clear")
  emb.add_field(name='{}kick'.format(PREFIX), value="Kick from the server")
  emb.add_field(name='{}ban'.format(PREFIX), value=' Ban from server')
  emb.add_field(name='{}unban'.format(PREFIX), value=' Unban')
  emb.add_field(name='{}mute'.format(PREFIX), value='Gives mute role')
  emb.add_field(name='{}unmute'.format(PREFIX), value='Remuve mute role')
  emb.add_field(name='{}botic'.format(PREFIX),
                value="Shits some one you write")
  emb.add_field(
      name='{}anounse'.format(PREFIX),
      value=
      "Make anounsment for sever. \nHow to use:\n Write title, url to resurse you want, url on img(not file) and add your description"
  )
  await ctx.send(embed=emb)


# Shows current anounsment
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def anounse(
    ctx,
    u_title="You title",
    u_url='https://www.youtube.com/watch?v=y25k0SImB8Y&ab_channel=Villeza',
    img_url='https://c0.klipartz.com/pngpicture/744/783/gratis-png-cara-del-reloj-cuarto-s.png',
    u_description="Your description"):
  try:
    emb = discord.Embed(title=f"{u_title}",
                        description=f'{u_description}',
                        colour=discord.Color.green(),
                        url=str(u_url))

    emb.set_author(name=bot.user.name, icon_url=bot.user.avatar)
    emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar)
    # emb.set_image( url = 'https://magnit.rv.ua/upload/iblock/a82/a82054c2da691436ac03ee38d2c163c0.jpg' )
    emb.set_thumbnail(url=str(img_url))

    now_date = datetime.datetime.now()
    emb.add_field(name="Time", value='Time : {}'.format(now_date))

    await ctx.channel.purge(limit=1)
    await ctx.send(embed=emb)
  except Exception as e:
    emb = discord.Embed(title='Error',
                        description="Read " + '{}help'.format(PREFIX) +
                        " again and try to write command correctly",
                        colour=discord.Color.red(),
                        url=str(u_url))
    emb.set_author(name=bot.user.name, icon_url=bot.user.avatar)
    emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar)
    emb.set_thumbnail(
        url=
        'https://www.elegantthemes.com/blog/wp-content/uploads/2020/08/000-http-error-codes.png'
    )
    await ctx.channel.purge(limit=1)
    await ctx.send(embed=emb)


# Del messages
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=100):
  await ctx.channel.purge(limit=amount)


# Hello to user
@bot.command(pass_context=True)
async def hello(ctx, amount=1):
  await ctx.channel.purge(limit=amount)

  author = ctx.message.author
  await ctx.send(f'Hello {author.mention}')


# Ban
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
  emb = discord.Embed(title="BAN", color=discord.Color.red())
  await ctx.channel.purge(limit=1)

  await member.ban(reason=reason)

  emb.set_author(name=member.name, icon_url=member.avatar)
  emb.set_thumbnail(url='https://cdn3.emoji.gg/emojis/2793_BAN.png')
  now_date = datetime.datetime.now()
  emb.add_field(name="Banned",
                value='On {}:'.format(now_date) +
                "banned user: {}".format(member.mention))
  await ctx.send(embed=emb)


# UnBan
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
  await ctx.channel.purge(limit=1)
  member_name, member_discriminator = member.split('#')

  # Loop over the banned users asynchronously
  async for ban_entry in ctx.guild.bans():
    user = ban_entry.user

    if (user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      await ctx.send(f'Unbanned user {user.mention}')
      return

  # If the user was not found in the banned users list
  await ctx.send(f'User {member} is not in the ban list!')


# Kick
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
  await ctx.channel.purge(limit=1)
  await member.kick(reason=reason)
  await ctx.send(f'kick user {member.mention}')


# Mute
# Mute
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    mute_role = discord.utils.get(ctx.guild.roles, name='Muted')

    # If the Muted role doesn't exist, create it
    if not mute_role:
        mute_role = await ctx.guild.create_role(name='Muted')

        for channel in ctx.guild.channels:
            await channel.set_permissions(mute_role, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    await member.add_roles(mute_role, reason=reason)
    await ctx.send(f'Muted {member.mention} for reason: {reason}')

# To unmute the user
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member, *, reason=None):
    mute_role = discord.utils.get(ctx.guild.roles, name='Muted')
    
    if mute_role in member.roles:
        await member.remove_roles(mute_role, reason=reason)
        await ctx.send(f'Unmuted {member.mention}')
    else:
        await ctx.send(f'The user {member.mention} is not muted.')

# Answer any question(Chat GPT)
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def chat(ctx, *, message: str):
    user_id = ctx.author.id  # Assuming you have a specific user ID to respond to

    if ctx.message.author.id != user_id:
        await ctx.send("This bot is not for public but private use only.")
    else:
        # Assuming g4f is a previously initialized API client for OpenAI or similar service
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}],
        )
        await ctx.send(response)

keep_alive.keep_alive()

bot.run(token)