import discord
from discord.app_commands.commands import describe  # Подключаем библиотеку
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
    'мудозвон',
    'ебал'
]


# Announsment about connecting bot to server
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(name=f'/help | Serving in {len(bot.guilds)} servers!'))
    application = await bot.application_info()

    # Update the bot's description if it has one, otherwise set it
    updated_description = "СПРОБУЙТЕ МОЇ КОМАНДИ\n/imagine\n/describe\n/blend\n/settings\n/info"
    if hasattr(bot, 'description') and bot.description:
        bot.description += updated_description
    else:
        bot.description = updated_description

    slash_commands = [f"/{i.name}" for i in bot.tree.get_commands()]
    if slash_commands:
        bot.description += f" Available slash commands: {', '.join(slash_commands)}"

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
          description=
          f'Користувач ``{member.display_name}``, Запригує до нас!',
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

# Slash commands
# help command
@bot.tree.command(name='help', description="Discribs all command on server")
async def hlep(interaction: discord.Interaction):
    emb = discord.Embed(title="Navigation by commands", color=discord.Color.blue())
    
    commands_list = {
        'hello': 'If you write greetings into chat it will answer.',
        'clear [number]': 'Clears a specified number of messages in the chat.',
        'kick [@user] [reason]': 'Kicks a user from the server.',
        'ban [@user] [reason]': 'Bans a user from the server.',
        'unban [user#discrim]': 'Unbans a user (e.g., user#1234).',
        'mute [@user] [reason]': 'Gives mute role to a user.',
        'unmute [@user]': 'Removes mute role from a user.',
        'botic [name]': 'Shits someone you write.',
        'announce [title] [url] [img_url] [description]': 'Makes an announcement for the server.',
        'private': 'Send details about your Discord account in a private message.',
        'anonymous_whisper [@user] [message]': 'Send an anonymous private message to a user.',
        'chat [message]': 'Bots will talk with you in chat.'
    }

    for cmd, desc in commands_list.items():
        emb.add_field(name=f'/{cmd}', value=desc, inline=False)

    await interaction.response.send_message(embed=emb)

# polling 
@bot.tree.command(name="poll", description="Creates a poll with up to 5 options. (Requires Manage Messages Permission)")
@app_commands.checks.has_permissions(manage_messages=True)
@app_commands.describe(question="What is the question the poll is gonna be asking?", option1="1st option that can be chosen", option2="2nd option that can be chosen", option3="3rd option that can be chosen", option4="4th option that can be chosen",option5="5th option that can be chosen", role="Which role to ping in the pole?")
async def poll(interaction: discord.Interaction, question: str, option1: str, option2: str, option3:str=None, option4:str=None, option5:str=None, role:discord.Role=None):
    await interaction.response.send_message("Creating poll...", ephemeral=True)
    try:
        listen = [option1, option2, option3, option4, option5]
        yonice = []
        for i in listen:
            if i != None:
                yonice.append(i)
        if role == None:
            if len(yonice) == 2:
                emb=discord.Embed(color=discord.Colour.blurple(), title=f"{question}", description=f"Option 1: {yonice[0]}\nOption 2: {yonice[1]}")
                msg=await interaction.channel.send(embed=emb)
                await msg.add_reaction("1️⃣")
                await msg.add_reaction("2️⃣")
            elif len(yonice) == 3:
                emb=discord.Embed(color=discord.Colour.blurple(), title=f"{question}", description=f"Option 1: {yonice[0]}\nOption 2: {yonice[1]}\nOption 3: {yonice[2]}")
                msg=await interaction.channel.send(embed=emb)
                await msg.add_reaction("1️⃣")
                await msg.add_reaction("2️⃣") 
                await msg.add_reaction("3️⃣")
            elif len(yonice) == 4:
                emb=discord.Embed(color=discord.Colour.blurple(), title=f"{question}", description=f"Option 1: {yonice[0]}\nOption 2: {yonice[1]}\nOption 3: {yonice[2]}\nOption 4: {yonice[3]}")
                msg=await interaction.channel.send(embed=emb)
                await msg.add_reaction("")
                await msg.add_reaction("2️⃣") 
                await msg.add_reaction("3️⃣")
                await msg.add_reaction("4️⃣")
            elif len(yonice) == 5:
                emb=discord.Embed(color=discord.Colour.blurple(), title=f"{question}", description=f"Option 1: {yonice[0]}\nOption 2: {yonice[1]}\nOption 3: {yonice[2]}\nOption 4: {yonice[3]}\nOption 5: {yonice[4]}")
                msg=await interaction.channel.send(embed=emb)
                await msg.add_reaction("1️⃣")
                await msg.add_reaction("2️⃣") 
                await msg.add_reaction("3️⃣")
                await msg.add_reaction("4️⃣")
                await msg.add_reaction("5️⃣")     
        else:
            if len(yonice) == 2:
                emb=discord.Embed(color=discord.Colour.blurple(), title=f"{question}", description=f"Option 1: {yonice[0]}\nOption 2: {yonice[1]}")
                msg=await interaction.channel.send(f"{role.mention}", embed=emb)
                await msg.add_reaction("1️⃣")
                await msg.add_reaction("2️⃣")
            elif len(yonice) == 3:
                emb=discord.Embed(color=discord.Colour.blurple(), title=f"{question}", description=f"Option 1: {yonice[0]}\nOption 2: {yonice[1]}\nOption 3: {yonice[2]}")
                msg=await interaction.channel.send(f"{role.mention}", embed=emb)
                await msg.add_reaction("1️⃣")
                await msg.add_reaction("2️⃣") 
                await msg.add_reaction("3️⃣")
            elif len(yonice) == 4:
                emb=discord.Embed(color=discord.Colour.blurple(), title=f"{question}", description=f"Option 1: {yonice[0]}\nOption 2: {yonice[1]}\nOption 3: {yonice[2]}\nOption 4: {yonice[3]}")
                msg=await interaction.channel.send(f"{role.mention}", embed=emb)
                await msg.add_reaction("1️⃣")
                await msg.add_reaction("2️⃣") 
                await msg.add_reaction("3️⃣")
                await msg.add_reaction("4️⃣")
            elif len(yonice) == 5:
                emb=discord.Embed(color=discord.Colour.blurple(), title=f"{question}", description=f"Option 1: {yonice[0]}\nOption 2: {yonice[1]}\nOption 3: {yonice[2]}\nOption 4: {yonice[3]}\nOption 5: {yonice[4]}")
                msg=await interaction.channel.send(f"{role.mention}", embed=emb)
                await msg.add_reaction("1️⃣")
                await msg.add_reaction("2️⃣") 
                await msg.add_reaction("3️⃣")
                await msg.add_reaction("4️⃣")
                await msg.add_reaction("5️⃣")
        await interaction.delete_original_response()
    except Exception as e:
        print(e)
        await interaction.delete_original_response()
        await interaction.followup.send("An error occured, try again later.", ephemeral=True)

# Botic
@bot.tree.command(name="botic", description="Shits someone you want")
@app_commands.describe(who = "Who you want to shit")
async def botic(interaction: discord.Interaction, who: str):
  try:
    random_option = random.choice(yaki_ti_Woddy)
    if who.lower() in [
      'micha', 'миша', 'misha', 'міша', 'm1sha', 'мішаня', 'mishanya',
      'mishaloh', 'mishaBomjik', 'mishapozornik', 'mishalosharik'
    ]: 
      who = "Бодя"
    response_text = f'{who} {random_option}!! \n'
  except TypeError:
    response_text = 'Введи текст після команди /botic'
  await interaction.response.send_message(response_text*5)

# Del messages
# The following transformed code with slash commands:
@bot.tree.command(name='clear', description="Clears messages in the quantity you want")
@app_commands.describe(amount="Number of messages to delete")
@app_commands.checks.has_permissions(administrator=True)
async def clear(interaction: discord.Interaction, amount: int):
    await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(embed=discord.Embed(description=f"Cleared {amount} messages"), ephemeral=True)

# Shows current anounsment
@bot.tree.command(name='announce', description="Make an announcement for whole server")
@app_commands.describe(
  u_title="Your title",
  u_url="The URL you want to share",
  img_url="The image URL you want to display",
  u_description="Your description"
)
async def announce(
        interaction: discord.Interaction,
        u_title: str = "You title",
        u_url: str = 'https://www.youtube.com/watch?v=y25k0SImB8Y&ab_channel=Villeza',
        img_url: str = 'https://c0.klipartz.com/pngpicture/744/783/gratis-png-cara-del-reloj-cuarto-s.png',
        u_description: str = "Your description"):
    try:
        emb = discord.Embed(title=f"{u_title}",
                            description=f'{u_description}',
                            colour=discord.Color.green(),
                            url=str(u_url))

        emb.set_author(name=bot.user.name, icon_url=bot.user.avatar)
        emb.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar)
        emb.set_thumbnail(url=str(img_url))

        now_date = datetime.datetime.now()
        emb.add_field(name="Time", value='Time : {}'.format(now_date))

        await interaction.response.send_message(embed=emb)
    except Exception as e:
        emb = discord.Embed(title='Error',
                            description="Read the command description again and try to write the command correctly",
                            colour=discord.Color.red(),
                            url=str(u_url))
        emb.set_author(name=bot.user.name, icon_url=bot.user.avatar)
        emb.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar)
        emb.set_thumbnail(
            url=
            'https://www.elegantthemes.com/blog/wp-content/uploads/2020/08/000-http-error-codes.png'
        )
        await interaction.response.send_message(embed=emb)

# Hello to user
@bot.tree.command(name='hello', description="Greats anyone")
@app_commands.describe(amount="The number of messages to delete")
async def hello(interaction: discord.Interaction, amount: int = 1):
    await interaction.channel.purge(limit=amount)
    
    author = interaction.user
    await interaction.response.send_message(f'Hello {author.mention}')


# Send an anonymous private message author
@bot.tree.command(name='private', description="Send private information to author")
async def private(interaction: discord.Interaction):
  author = interaction.user
  embed = discord.Embed(title="Private Information", color=discord.Color.blue())
  embed.add_field(name="Name", value=author.name, inline=True)
  embed.add_field(name="Discriminator", value=author.discriminator, inline=True)
  embed.add_field(name="User ID", value=author.id, inline=True)
  embed.add_field(name="Joined at", 
                  value=author.joined_at.strftime("%d/%m/%Y %H:%M:%S"), 
                  inline=True)
  embed.add_field(name="Account created at", 
                  value=author.created_at.strftime("%d/%m/%Y %H:%M:%S"), 
                  inline=True)
  embed.add_field(name="Current server", value=author.guild.name, inline=True)
  await interaction.response.send_message(embed=embed, ephemeral=True)


# Send an anonymous private message to a member with embed
@bot.tree.command(name='anonymous_whisper', description="Send private message to a member")
@app_commands.describe(member="The member to send the message to", message="The message to send")
async def anonymous_whisper(interaction: discord.Interaction, member: discord.Member, message: str = "Hello"):
    try:
        embed = discord.Embed(title="Anonymous Message", description=message, color=discord.Color.blue())
        await member.send(embed=embed)
        await interaction.channel.purge(limit=1)
    except discord.Forbidden:
        await interaction.response.send_message("I do not have permission to send direct messages to this user.")


# Ban
@bot.tree.command(name='ban', description="Ban a member")
@app_commands.describe(member='The member to ban', reason='The reason for the ban')
@app_commands.default_permissions(administrator=True)
@app_commands.guild_only()
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    emb = discord.Embed(title="BAN", color=discord.Color.red())

    await member.ban(reason=reason)

    emb.set_author(name=member.name, icon_url=member.avatar.url)
    emb.set_thumbnail(url='https://cdn3.emoji.gg/emojis/2793_BAN.png')
    now_date = datetime.datetime.now()
    emb.add_field(name="Banned",
                  value='On {}:'.format(now_date.strftime("%Y-%m-%d %H:%M:%S")) +
                  "banned user: {}".format(member.mention))
    await interaction.response.send_message(embed=emb)


# Unban
# @bot.command(pass_context=True)
# @commands.has_permissions(administrator=True)
# async def unban(ctx, *, member):
#   banned_users = await ctx.guild.bans()
#   member_name, member_discriminator = member.split('#')

#   for ban_entry in banned_users:
#     user = ban_entry.user

#     if (user.name, user.discriminator) == (member_name, member_discriminator):
#       await ctx.guild.unban(user)
#       await ctx.send(f'Unbanned user {user.mention}')
#       return

#   await ctx.send(f'User {member} is not in the ban list!')


# Kick with embed
@bot.tree.command(name='kick', description="Kick a member")
@app_commands.describe(member="Member to kick", reason="Reason for kicking")
@app_commands.default_permissions(administrator=True)
@app_commands.guild_only()
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    await member.kick(reason=reason)
    
    embed = discord.Embed(title="Kick",
                          description=f"{member.mention} has been kicked.",
                          color=discord.Color.red())
    embed.add_field(name="Reason", value=reason, inline=False)
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar)
    embed.set_thumbnail(url=member.display_avatar)
    embed.timestamp = datetime.datetime.utcnow()

    await interaction.response.send_message(embed=embed)


# Mute
@bot.tree.command(name='mute', description="Mute a member")
@app_commands.describe(member="Member to mute", reason="Reason for muting")
@app_commands.default_permissions(administrator=True)
async def mute(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    mute_role = discord.utils.get(interaction.guild.roles, name='Muted')

    # If the Muted role doesn't exist, create it
    if not mute_role:
        mute_role = await interaction.guild.create_role(name='Muted')
        for channel in interaction.guild.channels:
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
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
    embed.set_thumbnail(url=member.avatar)
    embed.timestamp = discord.utils.utcnow()

    await interaction.response.send_message(embed=embed)


# To unmute the user
@bot.tree.command(name='unmute', description="Unmute a member")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(member="Member to unmute", reason="Reason for unmuting")
async def unmute(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    mute_role = discord.utils.get(interaction.guild.roles, name='Muted')

    if mute_role in member.roles:
        await member.remove_roles(mute_role, reason=reason)
        # Create an embed message for unmuting
        embed = discord.Embed(title="Unmute",
                              description=f"{member.mention} has been unmuted.",
                              color=discord.Color.green())
        embed.add_field(name="Reason",
                        value=reason if reason else "No reason provided",
                        inline=False)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar)
        embed.set_thumbnail(url=member.display_avatar)
        embed.timestamp = discord.utils.utcnow()

        await interaction.response.send_message(embed=embed)
    else:
        # Send a message that the user is not muted
        embed = discord.Embed(
            title="Unmute",
            description=f"The user {member.mention} is not muted.",
            color=discord.Color.red())
        await interaction.response.send_message(embed=embed)

# Chat GPT
@bot.tree.command(name='chat', description="Chat with the CHAT GPT")
@app_commands.describe(message="Enter the message you want to chat about.")
@app_commands.default_permissions(administrator=True)
async def chat(interaction: discord.Interaction, message: str):
    user_id = interaction.user.id  # Assuming you have a specific user ID to respond to

    if user_id != user_id:  # This comparison does not make sense; needs a valid condition
        embed = discord.Embed(color=discord.Color.red())
        embed.add_field(name="Error", value="This bot is not for public but private use only.")
        await interaction.response.send_message(embed=embed)
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
        await interaction.response.send_message(embed=embed)




# User card with fetched user data
@bot.tree.command(name='card_user', description="Get a user card information")
@app_commands.describe(member="The member you want to view information of")
async def card_user(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user  # Default to the interaction user if no member is provided
    embed = discord.Embed(title=f"{member}'s User Card",
                          color=discord.Color.blue())
    embed.set_thumbnail(url=member.display_avatar.url)
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
    await interaction.response.send_message(embed=embed)

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
