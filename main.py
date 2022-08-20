# importing the CovidStatsBot class from the botFame module
from requests.api import request
from botFrame import CovidStatsBot as cbot
from pprint import pprint
from cowinAPI import vaccineSlotsInfo
import requests

bot = cbot()  # created the object of CovidStatsBot Class
# data = bot.get_updated()
currentchat_id = bot.getCurrentChat_id()   # to get the latest chat_id
lastMssgSentByUser = bot.getLastmssg()
# data = bot.get_updated()
last_update_id = bot.lastUpdate_id()
lastData = bot.get_updated(offset_value=last_update_id)

# info = vaccineSlotsInfo(lastMssgSentByUser)

# for item in info:
#     print(item)
# pprint(data) # testing received data
# print("outer", Currentchat_id, lastMssgSentByUser)
pinUpdateid_List = []
pinChatid_List = []
pinFlagDict = {}  # chatid:flagValue     flagValue = 1 if pincode is waiting
pinFlagValue = 0
while True:
    try:
        last_unseenData = bot.get_updated(offset_value=last_update_id)
        currentchat_id = bot.getCurrentChat_id()
        # lastData = bot.get_updated(offset_value=bot.lastUpdate_id())
        # pinFlagValue = 0
        newUpdates = last_unseenData["result"]
        if newUpdates:
            for item in newUpdates:
                item_chatid = item["message"]["chat"]["id"]
                print("\n\n\n", type(item_chatid), "type of itemchatid")
                item_Updateid = item["update_id"]
                item_username = item["message"]["from"]["username"]
                userText = item["message"]["text"].lower()

                print(userText, "for testing purposes", "type is ",
                      type(userText), "length is ", len(userText))
                print(f"Update_id = {item_Updateid}")
                print(f"chat_id = {item_chatid}")

                # tem_dict = {item_chatid: pinFlagValue}
                # pinFlagDict.update(tem_dict)
                # tem_dict.clear()

                if userText != "pincode" and userText != "/pincode":
                    if pinFlagValue != 1:
                        bot.mssg_send(item_chatid,
                                      "Invalid Input, use commands")
                    # pinFlagValue = 0
                    # pinFlagDict.update(item_chatid=pinFlagValue)

                else:
                    pinFlagValue = 1    # meaning that pincode has to be entered for this currentchatid
                    bot.mssg_send(item_chatid, "Okay, Now Enter the Pincode..")
                    pinUpdateid_List.append(item["update_id"])
                    # pinChatid_List.append(item["message"]["chat"]["id"])
                    # pinFlagDict[f"{str(item_chatid)}"] = pinFlagValue

                # dictionary prunt for debugging
                print(f"pinFlagDict is... {pinFlagDict}")
                if pinFlagDict:
                    if pinFlagDict[item_chatid] == 1:
                        print(f"inside flag one")
                        try:
                            if len(userText) == 6 and type(int(userText)) == type(int()):
                                print(
                                    "Yes..length and values are satisfied.. trying to send info now..\n")
                                info = vaccineSlotsInfo(pin=userText)
                                # print(f"\ninfo = {info}\n")

                                for i in info:
                                    bot.mssg_send(item_chatid, i)
                                    # log
                                    print(
                                        f'Vaccine info item has been sent to the user successfully')
                                pinFlagValue = 0
                        except:
                            print(
                                f'Mssg Sent to the username {item_username} : Unable to fetch the information right now !!\nTry again')
                            bot.mssg_send(item_chatid,
                                          "Unable to fetch the required information right now !!\nTry again")
                            pinFlagValue = 0

                else:
                    bot.mssg_send(
                        item_chatid, r"Please enter the command '/pincode' or 'pincode' ")
                    print(
                        f'Mssg sent to the user {item_username} Please enter the command "/pincode" or "pincode"')

            last_update_id = last_update_id + 1
    except Exception:
        print("Update is empty...\n\n")


print("hmm..")
