import sqlite3 # importing database
import aiosqlite
import asyncio # for debugging async functions

# This is a simple database to save your bot informations and fetch them when turn on the bot
# The main info saved in this database are:
#
# GUILD ID
# WELCOME CHANNEL ID
# BAN CHANNEL ID
# DEFAULT ROLE ID
# PROHIBITED WORD: LIST
# WARNS: DICT

#Method used in the bot initialization to create the Tables needed
async def initialize():

    try:
        db = await aiosqlite.connect("db.sqlite3")

        # SUPORT FOR FOREIGN KEYS
        await db.execute("PRAGMA foreign_keys = ON")

        await db.execute('''
        CREATE TABLE IF NOT EXISTS guild (
            guild_id INTEGER PRIMARY KEY,
            welcome_channel INTEGER DEFAULT 0,
            ban_channel INTEGER DEFAULT 0,
            default_role INTEGER DEFAULT 0
        )
        '''
        )

        await db.execute('''
        CREATE TABLE IF NOT EXISTS prohibited_words (
            word_id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER,
            word TEXT,
            UNIQUE(guild_id, word),
            FOREIGN KEY (guild_id) REFERENCES guild(guild_id)
        )
        '''
        )

        await db.execute('''
        CREATE TABLE IF NOT EXISTS warns (
            warn_id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER,
            user_id INTEGER,
            quantity INTEGER,
            UNIQUE(guild_id, user_id, quantity),
            FOREIGN KEY (guild_id) REFERENCES guild(guild_id)
        )
        '''
        )

        await db.commit()
        await db.close()

    except sqlite3.Error as error:
        print("Error: ", error)


"""""

SETTERS

"""""

# Method to add a new guild into the database
async def new_guild(guild_id:int):

    try:
        db = await aiosqlite.connect("db.sqlite3")

        cursor = await db.execute("INSERT INTO guild (guild_id) VALUES (?)", (guild_id,))

        await db.commit()
        
        await cursor.close()
        await db.close()

    except sqlite3.Error as error:
        print("Error: ", error)


# Method to set the id of welcome channel
async def set_welcome_channel(guild_id:int, channel_id:int):

    try:
        db = await aiosqlite.connect("db.sqlite3")

        cursor = await db.execute("UPDATE guild SET welcome_channel = ? WHERE guild_id = ?", (channel_id, guild_id))

        await db.commit()

        await cursor.close()
        await db.close()

    except sqlite3.Error as error:
        print("Error: ", error)


# Method to set the id of ban channel
async def set_ban_channel(guild_id:int, channel_id:int):

    try:
        db = await aiosqlite.connect("db.sqlite3")

        cursor = await db.execute("UPDATE guild SET ban_channel = ? WHERE guild_id = ?", (channel_id, guild_id))

        await db.commit()

        await cursor.close()
        await db.close()

    except sqlite3.Error as error:
        print("Error: ", error)


# Method to set the default_role for new members
async def set_default_role(guild_id:int, role_id:int):

    try:
        db = await aiosqlite.connect("db.sqlite3")

        cursor = await db.execute("UPDATE guild SET default_role = ? WHERE guild_id = ?", (role_id, guild_id))

        await db.commit()

        await cursor.close()
        await db.close()

    except sqlite3.Error as error:
        print("Error: ", error)


# Method to ban bad words from the guild
async def new_prohibited_word(guild_id:int, new_word:str):

    try:
        db = await aiosqlite.connect("db.sqlite3")

        cursor = await db.execute(f"INSERT INTO prohibited_words (guild_id, word) VALUES(?, ?)", (guild_id, new_word))

        await db.commit()

        await cursor.close()
        await db.close()

    except sqlite3.Error as error:
        print("Error: ", error)


# Method to have the warnings of the guild
async def new_warns(guild_id:int, user_id:int, quantity:int):

    try:
        db = await aiosqlite.connect("db.sqlite3")

        cursor = await db.execute(f"INSERT INTO warns (guild_id, user_id, quantity) VALUES(?, ?, ?)", (guild_id, user_id, quantity))

        await db.commit()
        
        await cursor.close()
        await db.close()

    except sqlite3.Error as error:
        print("Error: ", error)


"""""

GETTERS

"""""
async def fetch_welcome(guild_id:int) -> int:

    try:
        db = await aiosqlite.connect("db.sqlite3")

        # USING SQL TO SELECT THE INFO I WANT
        cursor = await db.execute("SELECT welcome_channel FROM guild WHERE guild_id = ?", (guild_id,))
        welcome = await cursor.fetchone() # Becomes a row

        await cursor.close()
        await db.close()

        if welcome and welcome[0] is not None:
            return int(welcome[0])
        
        else:
            return 0

    except sqlite3.Error as error:
        print("Error: ", error)

        return 0


async def fetch_ban(guild_id:int) -> int:

    try:
        db = await aiosqlite.connect("db.sqlite3")

        # USING SQL TO SELECT THE INFO I WANT
        cursor = await db.execute("SELECT ban_channel FROM guild WHERE guild_id = ?", (guild_id,))
        ban = await cursor.fetchone()

        await cursor.close()
        await db.close()


        if ban and ban[0] is not None:
            return int(ban[0])
        
        else:
            return 0

    except sqlite3.Error as error:
        print("Error: ", error)

        return 0
    

# Method used at bot initialization for getting the data
async def fetch_role(guild_id:int) -> int:

    try:
        db = await aiosqlite.connect("db.sqlite3")

        # USING SQL TO SELECT THE INFO I WANT
        cursor = await db.execute("SELECT default_role FROM guild WHERE guild_id = ?", (guild_id,))
        role = await cursor.fetchone()

        await cursor.close()
        await db.close()


        if role and role[0] is not None:
            return int(role[0])
        
        else:
            return 0

    except sqlite3.Error as error:
        print("Error: ", error)

        return 0


async def fetch_words(guild_id:int) -> list:

    try:
        db = await aiosqlite.connect("db.sqlite3")

        # GETTING A LIST OF THE PROHIBITED WORDS
        cursor = await db.execute("SELECT word FROM prohibited_words WHERE guild_id = ?", (guild_id,))
        words_list: list = [word[0] for word in await cursor.fetchall()]

        await cursor.close()
        await db.close()


        if words_list:
            return words_list
        
        else:
            return []
    
    except sqlite3.Error as error:
        print("Error: ", error)
        return []


async def fetch_warns(guild_id:int) -> dict:
    
    try:
        db = await aiosqlite.connect("db.sqlite3")

        # GETTING A DICT OF THE WARNS
        cursor = await db.execute("SELECT user_id, quantity FROM warns WHERE guild_id = ?", (guild_id,))
        warns_dict: dict = {user_id:quantity for user_id, quantity in await cursor.fetchall()}

        await cursor.close()
        await db.close()


        if warns_dict:
            return warns_dict
        
        else:
            return {}
    
    except sqlite3.Error as error:
        print("Error: ", error)
        return {}
    

# Clean the database
async def RESET():
    
    try:
        db = await aiosqlite.connect("db.sqlite3")

        await db.execute("DROP TABLE IF EXISTS guild")
        await db.execute("DROP TABLE IF EXISTS prohibited_words")
        await db.execute("DROP TABLE IF EXISTS warns")
        print("The data delete was succesfull!")

        await db.commit()
        await db.close()

    except sqlite3.Error as error:
        print("Error: ", error)


#asyncio.run(RESET())