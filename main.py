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

# for item in info:
#     print(item)
# pprint(data) # testing received data
# print("outer", Currentchat_id, lastMssgSentByUser)
pinUpdateid_List = []
pinChatid_List = []
pinVisitSet = set()  # chatid:flagValue     flagValue = 1 if pincode is waiting
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

#  Processing function


# def process(update_id, chat_id):
#     rec_mssg_pincode = self.get_mssg_by_id(update_id)
#     pinVisitSet.add(update_id)
#     info = vaccineSlotsInfo(rec_mssg_pincode)
#     for x in info:
#         self.mssg_send(chat_id, x)
#     print(f"mssg sent to {chat_id} for pincode: {rec_mssg_pincode} ")

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
                    # for list_indx in range(index, index+total_items):
                    #     this_update_id = bot.rec_data['result'][list_indx]['update_id']
                    #     this_chat_id = bot.rec_data['result'][0]["chat"]['id']
                    #     t = threading.Thread(target=bot.process, args=(
                    #         this_update_id, this_chat_id))
                    #     pinVisitSet.add(this_update_id)
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
                    ##################################### old code #####################################
                    # last_unseenData = bot.get_updated(offset_value=last_update_id)
                    # currentchat_id = bot.getCurrentChat_id()
                    # # lastData = bot.get_updated(offset_value=bot.lastUpdate_id())
                    # # pinFlagValue = 0
                    # newUpdates = last_unseenData["result"]
                    # if newUpdates:
                    #     for item in newUpdates:
                    #         item_chatid = item["message"]["chat"]["id"]
                    #         print("\n\n\n", type(item_chatid), "type of itemchatid")
                    #         item_Updateid = item["update_id"]
                    #         item_username = item["message"]["from"]["username"]
                    #         userText = item["message"]["text"].lower()

                    #         print(userText, "for testing purposes", "type is ",
                    #               type(userText), "length is ", len(userText))
                    #         print(f"Update_id = {item_Updateid}")
                    #         print(f"chat_id = {item_chatid}")

                    #         # tem_dict = {item_chatid: pinFlagValue}
                    #         # pinFlagDict.update(tem_dict)
                    #         # tem_dict.clear()

                    #         if userText != "pincode" and userText != "/pincode":
                    #             if pinFlagValue != 1:
                    #                 bot.mssg_send(item_chatid,
                    #                               "Invalid Input, use commands")
                    #             # pinFlagValue = 0
                    #             # pinFlagDict.update(item_chatid=pinFlagValue)

                    #         else:
                    #             pinFlagValue = 1    # meaning that pincode has to be entered for this currentchatid
                    #             bot.mssg_send(item_chatid, "Okay, Now Enter the Pincode..")
                    #             pinUpdateid_List.append(item["update_id"])
                    #             # pinChatid_List.append(item["message"]["chat"]["id"])
                    #             # pinFlagDict[f"{str(item_chatid)}"] = pinFlagValue

                    #         # dictionary prunt for debugging
                    #         print(f"pinFlagDict is... {pinFlagDict}")
                    #         if pinFlagDict:
                    #             if pinFlagDict[item_chatid] == 1:
                    #                 print(f"inside flag one")
                    #                 try:
                    #                     if len(userText) == 6 and type(int(userText)) == type(int()):
                    #                         print(
                    #                             "Yes..length and values are satisfied.. trying to send info now..\n")
                    #                         info = vaccineSlotsInfo(pin=userText)
                    #                         # print(f"\ninfo = {info}\n")

                    #                         for i in info:
                    #                             bot.mssg_send(item_chatid, i)
                    #                             # log
                    #                             print(
                    #                                 f'Vaccine info item has been sent to the user successfully')
                    #                         pinFlagValue = 0
                    #                 except:
                    #                     print(
                    #                         f'Mssg Sent to the username {item_username} : Unable to fetch the information right now !!\nTry again')
                    #                     bot.mssg_send(item_chatid,
                    #                                   "Unable to fetch the required information right now !!\nTry again")
                    #                     pinFlagValue = 0

                    #         else:
                    #             bot.mssg_send(
                    #                 item_chatid, r"Please enter the command '/pincode' or 'pincode' ")
                    #             print(
                    #                 f'Mssg sent to the user {item_username} Please enter the command "/pincode" or "pincode"')

                    #     last_update_id = last_update_id + 1
        except Exception:
            print("Update is empty...\n\n")


print("hmm..")
