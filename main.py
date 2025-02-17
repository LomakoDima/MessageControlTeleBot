import telebot
from config import *



bot = telebot.TeleBot(TOKEN)

# Словарь для хранения отправленных сообщений
sent_messages = {}

@bot.message_handler(commands=['send'])
def send_message(message):
    text = message.text[len("/send "):]  # Убираем команду из текста
    if not text:
        bot.reply_to(message, "Использование: /send ТЕКСТ")
        return
    sent_msg = bot.send_message(CHAT_ID, text)
    sent_messages[sent_msg.message_id] = sent_msg.text
    bot.reply_to(message, f"Сообщение отправлено в канал! ID: {sent_msg.message_id}")

@bot.message_handler(commands=['edit'])
def edit_message(message):
    parts = message.text.split(" ", 2)
    if len(parts) < 3:
        bot.reply_to(message, "Использование: /edit MESSAGE_ID НОВЫЙ ТЕКСТ")
        return
    msg_id, new_text = int(parts[1]), parts[2]
    try:
        bot.edit_message_text(new_text, CHAT_ID, msg_id)
        sent_messages[msg_id] = new_text
        bot.reply_to(message, "Сообщение обновлено!")
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

@bot.message_handler(commands=['delete'])
def delete_message(message):
    parts = message.text.split(" ")
    if len(parts) < 2:
        bot.reply_to(message, "Использование: /delete MESSAGE_ID")
        return
    msg_id = int(parts[1])
    try:
        bot.delete_message(CHAT_ID, msg_id)
        sent_messages.pop(msg_id, None)
        bot.reply_to(message, "Сообщение удалено!")
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

bot.polling(none_stop=True)
