import discord  # Подключаем библиотеку
from discord.ext import commands
import random
import keep_alive
import datetime
from tk import token
import g4f
from time import sleep
import requests
from PIL import Image, ImageFont, ImageDraw
from discord import app_commands

# add prefix
PREFIX = '>'
# Задаём префикс и интенты
bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())
bot.remove_command("help")
# lists for commands
hello_words = ['hello', 'hi', ' privet', 'ky', "привет", "здарова"]
yaki_ti_Woddy = [
    'bot', 'lox', 'pidr', 'shluxa', 'довбень', 'довбограй', 'уїбан', 'уйобище',
    'лошара', 'хуйло', 'хуйлуша', 'поїбанець', 'уйобок'
]
bad_words = [
    'fuck',
    'shit',
    'bitch',
    'ass',
    'pussy',
    'dick',
    'cunt',
    'pussy',
    'asshole',
    'assholes',
    'bitch',
    'fucker',
    'fuckers',
    'fucking',
    'fucks',
    'fucked',
    'fucked',
    # Ukrainian bad words
    'блядь',
    'хуй',
    'пизда',
    'сука',
    'шлюха',
    'дєбіл',
    'ідіот',
    'гандон',
    'сучара',
    'мудак',
    'заєбал',
    'срака',
    'підарас',
    'хуйло',
    'піздєц',
    'їбати',
    'курва',
    'пиздюк',
    'хер',
    'їбало',
    'залупа',
    'манда',
    'проститутка',
    'довбойоб',
    'нахуй',
    'єбут',
    'олень',
    'тупий',
    'підар',
    'лох',
    'розпиздяй',
    'засранець',
    'гівно',
    'гнида',
    'чмо',
    # Russian bad words
    'блять',
    'сука',
    'пизда',
    'хуй',
    'ебать',
    'ёб твою мать',
    'шлюха',
    'мудак',
    'идиот',
    'уебок',
    'гандон',
    'заебал',
    'долбаёб',
    'пидр',
    'ублюдок',
    'жопа',
    'хуесос',
    'выебон',
    'еблан',
    'пидарас',
    'манда',
    'залупа',
    'хер с ним',
    'ебало',
    'пиздюк',
    'нахуй',
    'охуел',
    'наебениться',
    'блядун',
    'заебись',
    'чмо',
    'говно',
    'дерьмо',
    'очко',
    'выебываться',
    'похуй',
    'мразь',
    'проебаться',
    'ссанина',
    'засранец',
    'мудозвон'
]


# Announsment about connecting bot to server
@bot.event
async def on_ready():
  print(f"Logged in as {bot.user.name}")

  await bot.change_presence(status=discord.Status.online,
                            activity=discord.Game(name='>help'))
  try:
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} commands")
  except Exception as e:
    print(f"Failed to sync commands: {e}")


# removes errors
@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    embed = discord.Embed(
        description="This command does not exist. Please use a valid command.",
        color=discord.Color.red())
  elif isinstance(error, commands.MissingRequiredArgument):
    embed = discord.Embed(
        description=
        "Missing a required argument. Please pass all the required arguments.",
        color=discord.Color.red())
  elif isinstance(error, commands.MissingPermissions):
    embed = discord.Embed(
        description=
        "You do not have the required permissions to execute this command.",
        color=discord.Color.red())
  elif isinstance(error, commands.CheckFailure):
    embed = discord.Embed(
        description=
        "You do not have the required role to execute this command.",
        color=discord.Color.red())
  elif isinstance(error, commands.CommandOnCooldown):
    embed = discord.Embed(
        description=
        f"This command is on cooldown. Please try again after {error.retry_after:.2f}s.",
        color=discord.Color.red())
  elif isinstance(error, commands.BadArgument):
    embed = discord.Embed(
        description="Invalid argument. Please provide a correct one.",
        color=discord.Color.red())
  elif isinstance(error, commands.CommandInvokeError):
    embed = discord.Embed(
        description="An error occurred while executing the command.",
        color=discord.Color.red())
  else:
    embed = discord.Embed(description="An unexpected error occurred.",
                          color=discord.Color.red())

  await ctx.send(embed=embed)


@bot.event
async def on_message(message):
  # Ensure the bot doesn't respond to itself
  if message.author == bot.user:
    return

  msg = message.content.lower()
  # Bad words detection
  if any(bad_word in msg for bad_word in bad_words):
    await message.delete()
    embed = discord.Embed(
        title="Inappropriate Language",
        description=f"{message.author.mention} Bad words are not allowed here!",
        color=discord.Color.red())
    warning_message = await message.channel.send(embed=embed)
    await asyncio.sleep(5)  # wait for 5 seconds before deleting the warning
    await warning_message.delete()

  await bot.process_commands(message)


# Del messages
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, amount: int):
  await ctx.channel.purge(limit=amount)


# Bot commands on join member
@bot.event
async def on_member_join(member):
  welcome_channel_id = 1173351967150575689  # ID of the welcome channel
  default_role_id = 1175087448464838666  # ID of the default role to assign

  # Fetch the channel and role using discord.py utility functions
  channel = bot.get_channel(welcome_channel_id)
  role = member.guild.get_role(default_role_id)

  if channel is not None and role is not None:
    try:
      await member.add_roles(role)
      embed = discord.Embed(
          description=f'Користувач ``{member.display_name}``, Запригує до нас!',
          color=0x00ff00)
      embed.set_thumbnail(url=member.avatar)
      # await clear(*, 1)
      await channel.send(embed=embed)
    except Exception as e:
      print(f"An error occurred while adding role or sending a message: {e}")
  else:
    if channel is None:
      print(f"Channel with ID {welcome_channel_id} not found.")
    if role is None:
      print(
          f"Role with ID {default_role_id} not found in guild {member.guild.name}."
      )


# help command
@bot.command(pass_context=True)
async def help(
    ctx
):  # Renamed the function to avoid conflict with the built-in help command
  emb = discord.Embed(title="Navigation by commands",
                      color=discord.Color.blue())

  commands_list = {
      'hello': 'If you write greetings into chat it will answer.',
      'clear [number]': 'Clears a specified number of messages in the chat.',
      'kick [@user] [reason]': 'Kicks a user from the server.',
      'ban [@user] [reason]': 'Bans a user from the server.',
      'unban [user#discrim]': 'Unbans a user (e.g., user#1234).',
      'mute [@user] [reason]': 'Gives mute role to a user.',
      'unmute [@user]': 'Removes mute role from a user.',
      'botic [name]': 'Shits some one you write.',
      'anounse [title] [url] [img_url] [description]':
      'Makes an announcement for the server.',
      'private':
      'Send details about your Discord account in a private message.',
      'anonymous_whisper [@user] [message]':
      'Send an anonymous private message to a user.',
      'chat [message]': 'Bots will talk with you in chat.'
  }

  for cmd, desc in commands_list.items():
    emb.add_field(name=f'{PREFIX}{cmd}', value=desc, inline=False)

  await ctx.send(embed=emb)


# botic
@bot.command(pass_context=True)
async def botic(ctx, arg):
  try:
    author = ctx.message.author
    # response_text = f'{author.mention} + arg бот!!' * 10
    # response_text = f'{author.mention}' + arg
    random_option = random.choice(yaki_ti_Woddy)
    if arg.lower() in [
        'micha', 'миша', 'misha', 'міша', 'm1sha', 'мішаня', 'mishanya',
        'mishaloh', 'mishaBomjik', 'mishapozornik', 'mishalosharik'
    ]:
      arg = "Бодя"
    response_text = f'{arg} {random_option}!! \n'
  except TypeError:
    response_text = 'Введи текст після команди >botic'
  for i in range(5):
    await ctx.send(response_text)


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


# Hello to user
@bot.command(pass_context=True)
async def hello(ctx, amount=1):
  await ctx.channel.purge(limit=amount)

  author = ctx.message.author
  await ctx.send(f'Hello {author.mention}')


# Send an anonymous private message author
@bot.command()
async def private(ctx):
  author = ctx.message.author
  embed = discord.Embed(title="Private Information",
                        color=discord.Color.blue())
  embed.add_field(name="Name", value=author.name, inline=True)
  embed.add_field(name="Discriminator",
                  value=author.discriminator,
                  inline=True)
  embed.add_field(name="User ID", value=author.id, inline=True)
  embed.add_field(name="Joined at",
                  value=author.joined_at.strftime("%d/%m/%Y %H:%M:%S"),
                  inline=True)
  embed.add_field(name="Account created at",
                  value=author.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                  inline=True)
  embed.add_field(name="Current server", value=author.guild.name, inline=True)
  await ctx.author.send(embed=embed)


# Send an anonymous private message to a member with embed
@bot.command()
async def anonymous_whisper(ctx,
                            member: discord.Member,
                            *,
                            message: str = "Hello"):
  try:
    embed = discord.Embed(title="Anonymous Message",
                          description=message,
                          color=discord.Color.blue())
    await member.send(embed=embed)
    await ctx.channel.purge(limit=1)
  except discord.Forbidden:
    await ctx.send(
        "I do not have permission to send direct messages to this user.")


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


# Unban
# Todo fix it
# @bot.command(pass_context=True)
# @commands.has_permissions(administrator=True)
# async def unban(ctx, *, member):
#   bans = await ctx.guild.bans()
#   member_name, member_discriminator = member.split('#')

#   for ban_entry in bans:
#     user = ban_entry.user

#     if (user.name, user.discriminator) == (member_name, member_discriminator):
#       await ctx.guild.unban(user)
#       await ctx.send(f'Unbanned user {user.mention}')
#       return

#   await ctx.send(f'User {member} is not in the ban list!')


# Kick with embed
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
  await ctx.channel.purge(limit=1)
  await member.kick(reason=reason)

  embed = discord.Embed(title="Kick",
                        description=f"{member.mention} has been kicked.",
                        color=discord.Color.red())
  embed.add_field(name="Reason", value=reason, inline=False)
  embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
  embed.set_thumbnail(url=member.avatar)
  embed.timestamp = datetime.datetime.utcnow()

  await ctx.send(embed=embed)


# Mute
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, *, reason="No reason provided"):
  mute_role = discord.utils.get(ctx.guild.roles, name='Muted')

  # If the Muted role doesn't exist, create it
  if not mute_role:
    mute_role = await ctx.guild.create_role(name='Muted')

    for channel in ctx.guild.channels:
      await channel.set_permissions(mute_role,
                                    speak=False,
                                    send_messages=False,
                                    read_message_history=True,
                                    read_messages=False)

  await member.add_roles(mute_role, reason=reason)
  # Using embed to send a message
  embed = discord.Embed(title="Mute",
                        description=f"{member.mention} has been muted.",
                        color=discord.Color.red())
  embed.add_field(name="Reason", value=reason, inline=False)
  embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
  embed.set_thumbnail(url=member.avatar)
  embed.timestamp = datetime.datetime.utcnow()

  await ctx.send(embed=embed)


# To unmute the user
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member, *, reason=None):
  mute_role = discord.utils.get(ctx.guild.roles, name='Muted')

  if mute_role in member.roles:
    await member.remove_roles(mute_role, reason=reason)
    # Create an embed message for unmuting
    embed = discord.Embed(title="Unmute",
                          description=f"{member.mention} has been unmuted.",
                          color=discord.Color.green())
    embed.add_field(name="Reason",
                    value=reason if reason else "No reason provided",
                    inline=False)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
    embed.set_thumbnail(url=member.avatar)
    embed.timestamp = datetime.datetime.utcnow()

    await ctx.send(embed=embed)
  else:
    # Send a message that the user is not muted
    embed = discord.Embed(
        title="Unmute",
        description=f"The user {member.mention} is not muted.",
        color=discord.Color.red())
    await ctx.send(embed=embed)


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def chat(ctx, *, message: str):
  user_id = ctx.author.id  # Assuming you have a specific user ID to respond to

  if ctx.message.author.id != user_id:
    embed = discord.Embed(color=discord.Color.red())
    embed.add_field(name="Error",
                    value="This bot is not for public but private use only.")
    await ctx.send(embed=embed)
  else:
    # Assuming g4f is a previously initialized API client for OpenAI or similar service
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": message
        }],
    )
    embed = discord.Embed(color=discord.Color.blue())
    embed.add_field(name="Response", value=response, inline=False)
    await ctx.send(embed=embed)


# User card with fetched user data
@bot.command(aliases=['user', 'I', 'profile', 'inform', 'info'])
async def card_user(ctx, *, member: discord.Member = None):
  member = member or ctx.author  # Default to the message author if no member is provided
  embed = discord.Embed(title=f"{member}'s User Card",
                        color=discord.Color.blue())
  embed.set_thumbnail(url=member.avatar.url)
  embed.add_field(name="Username", value=member.display_name, inline=True)
  embed.add_field(name="User ID", value=member.id, inline=True)
  embed.add_field(name="Account Created",
                  value=member.created_at.strftime('%B %d, %Y'),
                  inline=True)
  embed.add_field(name="Joined Server",
                  value=member.joined_at.strftime('%B %d, %Y'),
                  inline=True)
  embed.add_field(
      name="Top Role", value=member.top_role.name,
      inline=False)  # Changed inline to False for better readability
  await ctx.send(embed=embed)


@clear.error
async def clear_error(ctx, error):
  error_mapping = {
      commands.MissingRequiredArgument:
      'Please specify the number of messages to delete.',
      commands.MissingPermissions: 'You do not have the required permissions.',
      commands.BadArgument: 'Please specify a valid number.',
  }
  error_message = error_mapping.get(type(error),
                                    'An unknown error has occurred.')
  embed = discord.Embed(description=error_message, color=discord.Color.red())
  await ctx.send(embed=embed)


@ban.error
async def ban_error(ctx, error):
  error_mapping = {
      commands.MissingRequiredArgument: 'Please specify the user to ban.',
      commands.MissingPermissions: 'You do not have the required permissions.',
      commands.BadArgument: 'Please specify a valid user.',
      commands.UserNotFound: 'User not found.'
  }
  error_message = error_mapping.get(type(error),
                                    'An unknown error has occurred.')
  embed = discord.Embed(description=error_message, color=discord.Color.red())
  await ctx.send(embed=embed)


@kick.error
async def kick_error(ctx, error):
  error_mapping = {
      commands.MissingRequiredArgument: 'Please specify the user to kick.',
      commands.MissingPermissions: 'You do not have the required permissions.',
      commands.BadArgument: 'Please specify a valid user.',
      commands.UserNotFound: 'User not found.'
  }
  error_message = error_mapping.get(type(error),
                                    'An unknown error has occurred.')
  embed = discord.Embed(description=error_message, color=discord.Color.red())
  await ctx.send(embed=embed)


@mute.error
async def mute_error(ctx, error):
  error_mapping = {
      commands.MissingRequiredArgument: 'Please specify the user to mute.',
      commands.MissingPermissions: 'You do not have the required permissions.',
      commands.BadArgument: 'Please specify a valid user.',
      commands.UserNotFound: 'User not found.'
  }
  error_message = error_mapping.get(type(error),
                                    'An unknown error has occurred.')
  embed = discord.Embed(description=error_message, color=discord.Color.red())
  await ctx.send(embed=embed)


@unmute.error
async def unmute_error(ctx, error):
  error_mapping = {
      commands.MissingRequiredArgument: 'Please specify the user to unmute.',
      commands.MissingPermissions: 'You do not have the required permissions.',
      commands.BadArgument: 'Please specify a valid user.',
      commands.UserNotFound: 'User not found.'
  }
  error_message = error_mapping.get(type(error),
                                    'An unknown error has occurred.')
  embed = discord.Embed(description=error_message, color=discord.Color.red())
  await ctx.send(embed=embed)


keep_alive.keep_alive()

bot.run(token)
