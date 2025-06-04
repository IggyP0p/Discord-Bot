import sqlite3 # importing database
import aiosqlite

# This is a simple database to save your bot informations and fetch them when turn on the bot
# The main info saved in this database are:
#
# GUILD ID
# WELCOME CHANNEL ID
# BAN CHANNEL ID
# DEFAULT ROLE ID
# PROHIBITED WORD: LIST
# WARNS: DICT

# FALTA TRANSICIONAR DO SQLITE3 PARA AIOSQLITE

# Method used to create the connection with the database
def getConnection() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    # CREATNG CONNETION WITH THE DATABASE
    conn = sqlite3.connect('db.sqlite3')

    # OBJECT USED TO INTERACT WITH THE DATABASE
    cursor = conn.cursor()

    return conn, cursor

#Method used in the bot initialization to create the Tables needed
def initialize():

    try:
        conn, cursor = getConnection()

        # SUPORT FOR FOREIGN KEYS
        conn.execute("PRAGMA foreign_keys = ON")

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS guild (
            guild_id INTEGER PRIMARY KEY,
            welcome_channel INTEGER DEFAULT 0,
            ban_channel INTEGER DEFAULT 0,
            default_role INTEGER DEFAULT 0
        )
        '''
        )

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS prohibited_words (
            word_id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER,
            word TEXT,
            UNIQUE(guild_id, word)
            FOREIGN KEY (guild_id) REFERENCES guild(guild_id)
        )
        '''
        )

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS warns (
            warn_id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER,
            user_id INTEGER,
            quantity INTEGER,
            UNIQUE(guild_id, user_id, quantity)
            FOREIGN KEY (guild_id) REFERENCES guild(guild_id)
        )
        '''
        )

        conn.commit()
        conn.close()

    except sqlite3.Error as error:
        print("Error: ", error)


"""""

SETTERS

"""""
# Method to add a new guild into the database
def new_guild(guild_id:int):

    try:
        conn, cursor = getConnection()

        cursor.execute("INSERT INTO guild (guild_id) VALUES (?)", (guild_id,))

        conn.commit()
        conn.close()

    except sqlite3.Error as error:
        print("Error: ", error)


# Method to set the id of welcome channel
def set_welcome_channel(guild_id:int, channel_id:int):

    try:
        conn, cursor = getConnection()

        cursor.execute("UPDATE guild SET welcome_channel = ? WHERE guild_id = ?", (channel_id, guild_id))

        conn.commit()
        conn.close()

    except sqlite3.Error as error:
        print("Error: ", error)


# Method to set the id of ban channel
def set_ban_channel(guild_id:int, channel_id:int):

    try:
        conn, cursor = getConnection()

        cursor.execute("UPDATE guild SET ban_channel = ? WHERE guild_id = ?", (channel_id, guild_id))

        conn.commit()
        conn.close()

    except sqlite3.Error as error:
        print("Error: ", error)


# Method to set the default_role for new members
def set_default_role(guild_id:int, role_id:int):

    try:
        conn, cursor = getConnection()

        cursor.execute("UPDATE guild SET default_role = ? WHERE guild_id = ?", (role_id, guild_id))

        conn.commit()
        conn.close()

    except sqlite3.Error as error:
        print("Error: ", error)


# Method to ban bad words from the guild
def new_prohibited_word(guild_id:int, new_word:str):

    try:
        conn, cursor = getConnection()

        cursor.execute(f"INSERT INTO prohibited_words (guild_id, word) VALUES(?, ?)", (guild_id, new_word))

        conn.commit()
        conn.close()

    except sqlite3.Error as error:
        print("Error: ", error)


# Method to have the warnings of the guild
def new_warns(guild_id:int, user_id:int, quantity:int):

    try:
        conn, cursor = getConnection()

        cursor.execute(f"INSERT INTO warns (guild_id, user_id, quantity) VALUES(?, ?, ?)", (guild_id, user_id, quantity))

        conn.commit()
        conn.close()

    except sqlite3.Error as error:
        print("Error: ", error)


"""""

GETTERS

"""""
def fetch_welcome(guild_id:int) -> int:

    try:
        conn, cursor = getConnection()

        # USING SQL TO SELECT THE INFO I WANT
        cursor.execute("SELECT welcome_channel FROM guild WHERE guild_id = ?", (guild_id,))

        if cursor.fetchall():

            welcome = cursor.fetchone()
            conn.close()
            return welcome
        
        else:
            conn.close()
            return 0

    except sqlite3.Error as error:
        print("Error: ", error)

        return 0


def fetch_ban(guild_id:int) -> int:

    try:
        conn, cursor = getConnection()

        # USING SQL TO SELECT THE INFO I WANT
        cursor.execute("SELECT ban_channel FROM guild WHERE guild_id = ?", (guild_id,))

        if cursor.fetchall():

            ban = cursor.fetchone()
            conn.close()
            return ban
        
        else:
            conn.close()
            return 0

    except sqlite3.Error as error:
        print("Error: ", error)

        return 0
    

# Method used at bot initialization for getting the data
def fetch_role(guild_id:int) -> int:

    try:
        conn, cursor = getConnection()

        # USING SQL TO SELECT THE INFO I WANT
        cursor.execute("SELECT default_role FROM guild WHERE guild_id = ?", (guild_id,))

        if cursor.fetchall():

            role = cursor.fetchone()
            conn.close()
            return role
        
        else:
            conn.close()
            return 0

    except sqlite3.Error as error:
        print("Error: ", error)

        return 0


def fetch_words(guild_id:int) -> list:

    try:
        conn, cursor = getConnection()

        # GETTING A LIST OF THE PROHIBITED WORDS
        cursor.execute("SELECT word FROM prohibited_words WHERE guild_id = ?", (guild_id,))

        if cursor.fetchall():

            words_list: list = [word[0] for word in cursor.fetchall()]
            conn.close()
            return words_list 
        
        else:
            conn.close()
            return []
    
    except sqlite3.Error as error:
        print("Error: ", error)
        return []


def fetch_warns(guild_id:int) -> dict:
    
    try:
        conn, cursor = getConnection()

        # GETTING A DICT OF THE WARNS
        cursor.execute("SELECT user_id, quantity FROM warns WHERE guild_id = ?", (guild_id,))

        if cursor.fetchall():

            warns_dict: dict = {user_id:quantity for user_id, quantity in cursor.fetchall()}
            conn.close()
            return warns_dict
        
        else:
            conn.close()
            return {}
    
    except sqlite3.Error as error:
        print("Error: ", error)
        return {}
    

# Clean the database
def RESET():
    
    try:
        conn, cursor = getConnection()

        cursor.execute("DROP TABLE IF EXISTS guild")
        cursor.execute("DROP TABLE IF EXISTS prohibited_words")
        cursor.execute("DROP TABLE IF EXISTS warns")
        print("The data delete was succesfull!")

        conn.commit()
        conn.close()

    except sqlite3.Error as error:
        print("Error: ", error)

