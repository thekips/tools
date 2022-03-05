# telegram bot test program
from telebot import logger
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests

def start(update, context):
    text = '我只要有一个人喜欢我就够了\n' \
        '就算全世界都嫌弃我，只要那个人需要我\n' \
        '我就能活下去\n'
    update.message.reply_text(text)

def help(update, context):
    update.message.reply_text('会购物，还会发猫猫图（=￣ω￣=）\n不要想着我可以给你通知到所有的低价产品，哼~')

def cat(update, context):
    update.message.reply_photo('https://thiscatdoesnotexist.com/', caption='诶嘿嘿，猫猫yyds!')

def download(update, context):
    update.message.reply_video(update.message.text.split()[1])

def echo(update, context):
    print(update.message.text)
    res = requests.get('http://api.qingyunke.com/api.php?key=free&appid=0&msg=%s' % update.message.text)
    res = eval(res.text)['content']
    update.message.reply_text(res)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

if __name__ == '__main__':
    TOKEN = 'YOUR_TOKEN'
    updater = Updater(TOKEN, use_context=True, request_kwargs={
        'proxy_url': 'HTTPS://127.0.0.1:7890/'
    })
    res = requests.get('http://api.qingyunke.com/api.php?key=free&appid=0&msg=%s' % '泥头车')
    print(res.text)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("cat", cat))
    dispatcher.add_handler(CommandHandler("download", download))

    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()
