import telebot
import requests

BOT_TOKEN = "8200935468:AAEUrC0uc7yHbNodiQV09uarsai_fiIio4o"
API_KEY = "c8WRmO3Z0h79o4Vq2ENbMYtgFKnLrfPA65vkaGdXTlDiCHsI1QkVYeBC8RJXNiqPTQZbImFzEjtKWcaG"

CHANNEL = "@techtrickindia"
YOUTUBE_LINK = "https://youtube.com/@techtrickindia9?si=Rpy7JUHkD24g2c0W"
CHANNEL_LINK = "https://t.me/+L_vMv9fxx5ExMDU1"

bot = telebot.TeleBot(BOT_TOKEN)

# -------- JOIN CHECK --------
def joined(user_id):
    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member","administrator","creator"]
    except:
        return False

# -------- START --------
@bot.message_handler(commands=['start'])
def start(message):

    if not joined(message.from_user.id):

        markup = telebot.types.InlineKeyboardMarkup()

        markup.add(
            telebot.types.InlineKeyboardButton(
                "📺 YouTube Subscribe", url=YOUTUBE_LINK)
        )

        markup.add(
            telebot.types.InlineKeyboardButton(
                "📢 Join Telegram Channel", url=CHANNEL_LINK)
        )

        # VERIFY dabate hi channel khulega
        markup.add(
            telebot.types.InlineKeyboardButton(
                "✅ VERIFY", url=CHANNEL_LINK)
        )

        bot.send_message(
            message.chat.id,
            "🚫 Bot use karne se pehle:\n\n"
            "1️⃣ YouTube channel subscribe karo\n"
            "2️⃣ Telegram channel join karo\n"
            "3️⃣ VERIFY button dabao",
            reply_markup=markup
        )
        return

    bot.send_message(message.chat.id,"✅ Access Granted! Ab bot use kar sakte ho.")

# -------- SMS COMMAND --------
@bot.message_handler(commands=['sms'])
def sms(message):

    if not joined(message.from_user.id):
        bot.reply_to(message,"❌ Pehle verification complete karo /start")
        return

    try:
        data = message.text.split(" ",2)
        number = data[1]
        msg = data[2]

        requests.post(
            "https://www.fast2sms.com/dev/bulkV2",
            json={
                "sender_id":"FSTSMS",
                "message":msg,
                "language":"english",
                "route":"q",
                "numbers":number
            },
            headers={"authorization":API_KEY}
        )

        bot.reply_to(message,"✅ SMS Sent Successfully!")

    except:
        bot.reply_to(message,"Use:\n/sms number message")

bot.infinity_polling()


