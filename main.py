
import logging
import schedule
import time
import threading
from datetime import datetime
from telegram import Bot
from telegram.ext import CommandHandler, Updater

TOKEN = "7839418740:AAEVKRSZwCFtXmp8n57gYQCvaKpWV8qbdoQ"
CHAT_ID = None  # Will be set on /start

# Daily Schedule Data
daily_schedule = {
    "Monday": {"subject": "DSA - Trees", "questions": ["LeetCode - Two Sum", "Codeforces - 1A Theatre Square", "CodeChef - FLOW001", "LeetCode - Tree Traversal", "GFG - Binary Tree Basics"]},
    "Tuesday": {"subject": "OS - Scheduling", "questions": ["HackerRank - Arrays", "TopCoder - SRM 821 Div2 250", "LeetCode - Add Two Numbers", "Codeforces - Beautiful Matrix", "GFG - Stack Applications"], "contest": "Codeforces Div 2 at 8 PM (Reminder at 6 PM)"},
    "Wednesday": {"subject": "DBMS - Normalization", "questions": ["LeetCode - Longest Substring", "CodeChef - INTEST", "Codeforces - Books", "HackerRank - Hash Tables", "GFG - Linked List"]},
    "Thursday": {"subject": "CN - OSI Model", "questions": ["HackerEarth - Graphs", "TopCoder - Div2 500", "LeetCode - DFS/BFS", "Codeforces - Varied Number", "GFG - Graph Traversal"]},
    "Friday": {"subject": "OOPs - Inheritance", "questions": ["LeetCode - Median", "Codeforces - Time Management", "Hackerrank Weekly", "GFG - Greedy", "CodeChef Practice"], "contest": "Hackerrank Weekly at 9 PM (Reminder at 7 PM)"},
    "Saturday": {"subject": "System Design / Aptitude", "questions": ["Codeforces - Watermelon", "TopCoder - Div2 1000", "LeetCode - DP", "HackerRank - DS", "CodeChef Long Challenge"]},
    "Sunday": {"subject": "Mock Test", "questions": ["LeetCode Biweekly", "Codeforces - XOR", "GFG - Mock Test", "CodeChef - Review", "Custom Contest"], "contest": "LeetCode Weekly at 8 AM (Reminder at 6 AM)"}
}

def send_message(bot, text):
    if CHAT_ID:
        bot.send_message(chat_id=CHAT_ID, text=text)

def create_message():
    today = datetime.now().strftime("%A")
    data = daily_schedule.get(today, {})
    msg = f"📅 *{today} Schedule*\n📘 {data.get('subject')}\n\n🧠 Questions:\n"
    for q in data.get("questions", []):
        msg += f"• {q}\n"
    if "contest" in data:
        msg += f"\n🏁 Contest: {data['contest']}"
    return msg

def schedule_jobs(bot):
    schedule.every().day.at("08:00").do(lambda: send_message(bot, create_message()))
    schedule.every().day.at("20:00").do(lambda: send_message(bot, create_message()))
    threading.Thread(target=lambda: [schedule.run_pending() or time.sleep(1) for _ in iter(int, 1)]).start()

def start(update, context):
    global CHAT_ID
    CHAT_ID = update.message.chat_id
    update.message.reply_text("✅ Daily Reminder Bot Activated!")
    schedule_jobs(context.bot)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
