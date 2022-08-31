# importing the CovidStatsBot class from the botFame module
import threading
from time import sleep
from requests.api import request
from botFrame import CovidStatsBot as cbot
from pprint import pprint
from cowinAPI import vaccineSlotsInfo
import requests

bot = cbot()  # created the object of CovidStatsBot Class
# data = bot.get_updated()
# currentchat_id = bot.getCurrentChat_id()   # to get the latest chat_id
# lastMssgSentByUser = bot.getLastmssg()
# # data = bot.get_updated()
# last_update_id = bot.lastUpdate_id()
# lastData = bot.get_updated(offset_value=last_update_id)

# info = vaccineSlotsInfo(lastMssgSentByUser)


pinUpdateid_List = []
pinChatid_List = []
pinVisitSet = set()  # set for storing update ids
pinFlagValue = 0


def loop_large_items(index, total_items):
    global pinVisitSet
    for list_indx in range(index, index+total_items):
        this_update_id = bot.rec_data['result'][list_indx]['update_id']
        this_chat_id = bot.rec_data['result'][list_indx]['message']["chat"]['id']
        t = threading.Thread(target=bot.process, args=(
            this_update_id, this_chat_id))
        t.start()
        pinVisitSet.add(this_update_id)


last_id = bot.lastUpdate_id()
while True:
    sleep(1)
    # updating for any new data
    data_rec = bot.get_updated(offset_value=last_id)
    if data_rec:
        try:
            index = 0
            first_id = bot.first_update_id()
            if first_id:
                last_id = bot.lastUpdate_id()
                total_items = last_id - first_id
                if total_items == 0:
                    firstchat_id = bot.get_first_Chat_id()
                    if first_id not in pinVisitSet:
                        # sending mssg to the user
                        bot.process(first_id, firstchat_id)
                        pinVisitSet.add(first_id)
                        last_id += 1
                        continue
                    elif first_id in pinVisitSet:
                        while True:
                            if first_id in pinVisitSet:
                                first_id += 1
                                index += 1
                            else:
                                pinVisitSet.add(first_id)
                                break

                    total_items = (last_id - first_id)+1
                    loop_large_items(index, total_items)

                    last_id += 1
                elif total_items > 0:
                    if first_id not in pinVisitSet:
                        loop_large_items(index, total_items)
                    elif first_id in pinVisitSet:
                        while True:
                            if first_id in pinVisitSet:
                                first_id += 1
                                index += 1
                            else:
                                pinVisitSet.add(first_id)
                                break

                        total_items = (last_id - first_id)+1
                        loop_large_items(index, total_items)
                        last_id += 1

        except Exception:
            print("Update is empty...\n\n")

# should not reach here !!
print("Should not print this.")
