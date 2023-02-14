import logging
import time
import queue
from collections import defaultdict
from datetime import datetime, timedelta

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    """Send a message when the command /start is issued."""
    user = update.message.from_user
    update.message.reply_text(f'Hi {user.first_name}! I can help you keep track of your mood. '
                              f'To add a mood entry, simply send me a message with your current mood. '
                              f'For example: "Feeling great today!"')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('To add a mood entry, simply send me a message with your current mood. '
                              'For example: "Feeling great today!"')


def mood(update, context):
    """Add a mood entry to the database."""
    user = update.message.from_user
    text = update.message.text
    mood_entries[user.id].append((datetime.now(), text))
    update.message.reply_text(f'Thanks for sharing your mood, {user.first_name}! Your mood has been added to the database.')


def weekly_report(context):
    """Send a weekly report of the mood data to all users in the database."""
    for user_id, entries in mood_entries.items():
        user_entries = [entry for entry in entries if (datetime.now() - entry[0]).days < 7]
        num_entries = len(user_entries)
        if num_entries == 0:
            continue

        avg_mood = sum(entry[1].count('great') for entry in user_entries) / num_entries
        report = f'Weekly Mood Report\n\n'
        report += f'Number of Mood Entries: {num_entries}\n'
        report += f'Average Mood: {"Great" if avg_mood > 0.5 else "Not So Great"} ({avg_mood:.2f})\n\n'
        report += 'Detailed Mood Entries:\n'
        for entry in user_entries:
            report += f'{entry[0].strftime("%Y-%m-%d %H:%M:%S")}: {entry[1]}\n'

        context.bot.send_message(chat_id=user_id, text=report)


mood_entries = defaultdict(list)

update_queue = queue.Queue()

# Set up the Updater and add handlers for the commands
token = "5630575710:AAGoTBfUXYuBTF3MvBsXxGt632ycPmqg0YQ"

updater = Updater(token, update_queue=update_queue)
