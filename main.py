import os
import json
import telebot
from telebot import types

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)

# Add command hints in Telegram
bot.set_my_commands([
    types.BotCommand("add_to", "Add a user to a group"),
    types.BotCommand("remove_from", "Remove a user from a group"),
    types.BotCommand("ping", "Mention all users in a group"),
    types.BotCommand("help", "Show how to use the bot")
])

# Load or create group data
try:
    with open("groups.json", "r") as f:
        groups = json.load(f)
except FileNotFoundError:
    groups = {}


def save_groups():
    with open("groups.json", "w") as f:
        json.dump(groups, f)


@bot.message_handler(commands=["add_to"])
def add_to_group(message):
    try:
        _, group_name, username = message.text.split()
        if group_name not in groups:
            groups[group_name] = []
        if username not in groups[group_name]:
            groups[group_name].append(username)
            save_groups()
            bot.reply_to(message, f"✅ {username} added to {group_name}")
        else:
            bot.reply_to(message, f"{username} is already in {group_name}")
    except:
        bot.reply_to(message, "Usage: /add_to group_name @username")


@bot.message_handler(commands=["remove_from"])
def remove_from_group(message):
    try:
        _, group_name, username = message.text.split()
        if group_name in groups and username in groups[group_name]:
            groups[group_name].remove(username)
            save_groups()
            bot.reply_to(message, f"❌ {username} removed from {group_name}")
        else:
            bot.reply_to(message, f"{username} not found in {group_name}")
    except:
        bot.reply_to(message, "Usage: /remove_from group_name @username")


@bot.message_handler(commands=["ping"])
def ping_group(message):
    try:
        _, group_name = message.text.split()
        if group_name in groups:
            mentions = " ".join(groups[group_name])
            bot.send_message(message.chat.id, f"🔔 {mentions}")
        else:
            bot.reply_to(message, f"Group {group_name} not found")
    except:
        bot.reply_to(message, "Usage: /ping group_name")


@bot.message_handler(commands=["help"])
def help_command(message):
    help_text = (
        "🛠 *Group Tagging Bot Help*\n\n"
        "Use this bot to manage and tag custom user groups:\n\n"
        "➕ `/add_to group_name @username` – Add a user to a group\n"
        "➖ `/remove_from group_name @username` – Remove a user from a group\n"
        "📣 `/ping group_name` – Mention all users in a group\n\n"
        "_Example:_\n"
        "`/add_to dev_team @alice`\n"
        "`/ping dev_team`\n→ `@alice @bob @carol`\n\n"
        "📝 Only usernames (`@name`) can be stored.\n🔒 The bot must be in the same chat as the users you mention."
    )
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")


print("Bot is running...")
bot.polling()
