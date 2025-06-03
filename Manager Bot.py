#Discord bot for server managing, with this bot you will be able automatize your server, creating
#rooms, creating polls, creating nicknames, creating roles, banning users, banning words, moving menbers
#and even more.
#Created by Igor Barbosa de Sousa in 31/05/2025
#libraries
import discord
from discord.ext import commands
from discord import Permissions
from discord.utils import get
import os
from dotenv import load_dotenv

load_dotenv()
#INSERT HERE YOUR BOT ID
Client_id = os.getenv('DISCORD_TOKEN')

#Using intents we can tell discord which informations our bot need to work
intents = discord.Intents.default()
intents.message_content = True  # manually activation needed
intents.members = True # manually activation needed

# creating the bot
bot = commands.Bot(command_prefix="!", intents=intents)

#global variables
welcome_channel_id = 0
ban_channel_id = 0
default_role:discord.Role
prohibited_words = []
warns = {}


"""""

EVENTS

"""""


@bot.event
async def on_ready():
    print("Bot succesfully initialized!")


# Method to greet new members
@bot.event
async def on_member_join(member:discord.Member):
    guild = member.guild

    #Check if the welcome channel exists
    if(welcome_channel_id == 0):
        return

    canal = member.guild.get_channel(welcome_channel_id)
    if canal:
        await canal.send(f"{member.mention} has entered the guild!")
    else:
        print(f"Something went wrong trying to mention the greetings!")

    # adding the default_role to this new member
    if(default_role):
        await member.add_roles(default_role)


# Ban and unban alerts
@bot.event
async def on_member_ban(guild:discord.Guild, member:discord.Member):

    #Check if the ban channel exists
    if(ban_channel_id == 0):
        return

    canal = guild.get_channel(ban_channel_id)
    if canal:
        await canal.send(f"{member.mention} has been BANED from the guild!")
    else:
        print(f"Something went wrong trying to mention the ban!")


@bot.event
async def on_member_unban(guild:discord.Guild, member:discord.Member):

    #Check if the ban channel exists
    if(ban_channel_id == 0):
        return

    try:
        await member.send(f"📬 Mensagem do servidor {guild.name}:\nCongratulations! You have been unbanned!")
    except:
        print("It was not possible to send the unban message...")

    canal = guild.get_channel(ban_channel_id)

    if canal:
        await canal.send(f"{member.mention} has been UNBANED from the guild!")
    else:
        print(f"Something went wrong trying to mention the ban!")


#@bot.event
#async def on_message(message):
#
#    if message.author.bot:
#        return
#
#    for word in prohibited_words:
#        if word in message.content.lower():
#            await message.delete()
#            await message.channel.send(f"{message.author.mention}, linguagem inaproprida!")
#
#            warns[message.author.id] += 1
#            await punish(message.author)
#            return
        

"""""

Channel Commands

"""""

# Command for creating a channel
@bot.command()
async def create_channel(ctx:commands.Context, channel_name:str):
    guild = ctx.guild
    
    # Verifying if the channel already exists
    existing_channel = get(guild.text_channels, name=channel_name)
    
    if existing_channel:
        await ctx.send(f"⚠️ O canal `{channel_name}` já existe: {existing_channel.mention}")
        return

    # Try to create the channel, if the error occur it throws it
    try:
        new_channel = await guild.create_text_channel(channel_name)
        await ctx.send(f"✅ Canal criado: {new_channel.mention}")
    except:
        await ctx.send("❌ I do not have permission to manage channels here!")


# Command for deleting a channel
@bot.command()
async def delete_channel(ctx:commands.Context, channel_name:str):
    guild = ctx.guild

    # Verifying if the channel exists
    existing_channel = get(guild.text_channels, name=channel_name)

    if not existing_channel:
        await ctx.send(f"⚠️ O canal `{channel_name}` não existe")
        return
    
    try:
        await existing_channel.delete()
        await ctx.send(f"✅ Canal `{channel_name}` deletado com sucesso!")
    except:
        await ctx.send("❌ I do not have permission to manage channels here!")


# Sets the channel in which new members will receive welcome messages
@bot.command()
async def set_welcome_channel(ctx:commands.Context):
    global welcome_channel_id

    welcome_channel_id = ctx.channel.id
    await ctx.send("The channel was succesfully chosen as the welcome channel!")


# Sets the channel in which ban and unban alerts will occur
@bot.command()
async def set_ban_channel(ctx:commands.Context):
    global ban_channel_id

    ban_channel_id = ctx.channel.id
    await ctx.send("The channel was succesfully chosen as the ban channel!")


# Command to create a new invite to members
@bot.command()
async def create_invite(ctx):
    invite = await ctx.channel.create_invite(max_uses=100, unique=True)
    await ctx.send(f"Aqui está seu convite: {invite.url}")


"""""

Role Commands

"""""

# command to create a new role
@bot.command()
async def create_role(ctx, role_name:str, role_color:discord.Colour):
    guild = ctx.guild

    try:
        await guild.create_role(name=role_name, colour=role_color)
        await ctx.send(f"Role `{role_name}` succesfully created!")
    except:
        await ctx.send(f"It was not possible to create the role `{role_name}`\nCheck the permissions and mark 'manage roles'")


# Method responsible for deleting a role from the guild
@bot.command()
async def erase_role(ctx, role:discord.Role):
    name = role.name

    try:
        await role.delete()
        await ctx.send(f"{name} role was succesfully deleted")
    except:
        await ctx.send(f"It was not possible to delete the role `{name}`\nCheck the permissions and mark 'manage roles'")


# Method responsible for adding a role to a member
@bot.command()
async def assign_role(ctx, member:discord.Member, role:discord.Role):

    try:
        await member.add_roles(role)
        await ctx.send(f"Member {member.nick} was assigned as {role.name}")
    except:
        await ctx.send(f"It was not possible to assign the role {role.name}\nCheck the permissions and mark 'manage roles'")       


# Method responsible for removing a role from a member of the guild
@bot.command()
async def remove_member_role(ctx, member:discord.Member, role:discord.Role):

    try:
        await member.remove_roles(role)
        await ctx.send(f"Member {member.nick} has lost the role of a {role.name}")
    except:
        await ctx.send(f"It was not possible to remove the role {role.name} from {member.nick}\nCheck the permissions and mark 'manage roles'")       


# Method responsible for listing all the roles in the guild
@bot.command()
async def list_roles(ctx):

    try:
        all_roles = ctx.guild.roles
        names = [all_roles.name for role in all_roles if all_roles.name != "@everyone"]
        await ctx.send("Roles:\n" + "\n".join(names))
    except:
        await ctx.send("It was not possible to list the roles")
    

"""""

Pre-set guild Commands

"""""

# If you just created a guild you can automatically create text-channels, categorys and roles
# with this method
@bot.command()
async def generate_guild_pre_set(ctx:commands.Context):
    global welcome_channel_id, ban_channel_id, default_role, prohibited_words
    guild = ctx.guild

    #creating the categories and text channels of the guild
    first_category = await guild.create_category("Text Channels")
    #assigning the welcome channel
    welcome = await guild.create_text_channel("welcome", category=first_category)
    welcome_channel_id = welcome.id

    await guild.create_text_channel("general", category=first_category)
    #assigning the ban channel
    ban = await guild.create_text_channel("bans", category=first_category)
    ban_channel_id = ban.id
    #creating voice channels
    second_category = await guild.create_category("Voice Channels")
    await guild.create_voice_channel("General", category=second_category)

    #Giving permissions
    beginner_permissions = Permissions(False)
    advanced_permissions = Permissions(False)
    admin_permissions = Permissions(False)

    beginner_permissions.update(send_messages=True, read_messages=True)
    advanced_permissions.update(send_messages=True, read_messages=True, mention_everyone=True)
    admin_permissions.update(administrator=True)

    #creating roles for the members
    default_role = await guild.create_role(name='beginner', permissions=beginner_permissions, colour=discord.Colour.green())
    await guild.create_role(name='intermediate', permissions=beginner_permissions, colour=discord.Colour.blue())
    await guild.create_role(name='advanced', permissions=advanced_permissions, colour=discord.Colour.red())
    await guild.create_role(name='admin', permissions=admin_permissions, colour=discord.Colour.yellow())

    
    # Adding the prohibited words of the users
    prohibited_words = "fuck"



"""""

adding commands

"""""

@bot.command()
async def add_prohibited_word(ctx, prohibited:str):
    global prohibited_words

    prohibited_words.append(prohibited.lower())
    await ctx.send("the word was added with success!")


@bot.command()
async def remove_prohibited_word(ctx, prohibited:str):
    global prohibited_words
    word = prohibited.lower()

    if word in prohibited_words:
        prohibited_words.remove(word)
        await ctx.send("This word was removed with success!")
    else:
        await ctx.send("word not found!")


"""""

Own methods

"""""

async def punish(user:discord.Member):
    guild = user.guild

    #Check for punish role
    punish_role = get(guild.roles, name="offender")

    if not punish_role:
        punish_role = await guild.create_role(name="offender")
        for channel in guild.channels:
            await channel.set_permissions(punish_role, speak=False, send_messages=False)

    # the punishing method will count until 3 then ban the user
    if(warns[user.id] < 3):
        await user.add_roles(punish_role)
    else:
        await user.ban(reason="Said 3 prohibited words in the chat of the guild")

bot.run(Client_id)