import telebot
import requests

BOT_TOKEN = "8200935468:AAHsRcYTfYy_3qmBQ6_McS3gkkaUaK4RI50
"

API_KEY = "c8WRmO3Z0h79o4Vq2ENbMYtgFKnLrfPA65vkaGdXTlDiCHsI1QkVYeBC8RJXNiqPTQZbImFzEjtKWcaG"

CHANNEL = "@techtrickindia"   # apna channel username
YOUTUBE_LINK = "https://youtube.com/@techtrickindia9?si=Rpy7JUHkD24g2c0W"

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
                "📺 YouTube Subscribe", url=YOUTUBE_LINK),
            telebot.types.InlineKeyboardButton(
                "✅ VERIFY", callback_data="verify")
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

# -------- VERIFY BUTTON --------
@bot.callback_query_handler(func=lambda call: call.data=="verify")
def verify(call):

    if joined(call.from_user.id):
        bot.edit_message_text(
            "✅ Verification Successful!\nAb bot use kar sakte ho.",
            call.message.chat.id,
            call.message.message_id
        )
    else:
        bot.answer_callback_query(
            call.id,
            "❌ Pehle Telegram channel join karo!"
        )

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
