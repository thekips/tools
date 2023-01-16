# -*- coding: utf-8 -*-
import os
import sys
import time
from telethon import TelegramClient, events, sync

api_id = 26449713
api_hash = sys.argv[0]

session_name = "id_" + str(api_id)
# print(session_name, api_id, api_hash)

client = TelegramClient(session_name, api_id, api_hash)
client.start()

# Send to fnf_bot
client.send_message("@fooandfriends_bot", '/checkin')	#第一项是机器人ID，第二项是发送的文字
time.sleep(2)	#延时2秒，等待机器人回应（一般是秒回应，但也有发生阻塞的可能）
client.send_read_acknowledge("@fooandfriends_bot")	#将机器人回应设为已读
info = client.get_messages("@fooandfriends_bot") #获取消息
if len(info) >= 0:
    print(info[0].message)
else:
    print('ERR, NO MESSAGE..')

# Send to yellow_gif_bot
for i in range(3):
    info = client.get_messages("@yellow_gif_bot", 2) #获取消息
    
    if len(info) >= 0:
        print(info[0].message)
    else:
        print('ERR, NO MESSAGE..')
        
    client.send_message('@yellow_gif_bot', message=info[1])
    time.sleep(2)

os._exit(0)