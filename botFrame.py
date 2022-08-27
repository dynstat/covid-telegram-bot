
from datetime import date
import requests
import configparser as cfg

from cowinAPI import vaccineSlotsInfo

today = date.today()

# dd/mm/YY
thedate = today.strftime("%d-%m-%Y")
# ------------------------------------------------------------------------------


def read_API_fromConfig(config):
    parser = cfg.ConfigParser()
    parser.read(config)
    return parser.get('creds', 'APIKEY')


# create a config.cfg file to prevent API KEY to be visible in the main program
API_KEY = read_API_fromConfig('config.cfg')

# print(API_KEY)


class CovidStatsBot():
    def __init__(self, offset_value=None) -> None:
        self.base_url = f"https://api.telegram.org/bot{API_KEY}/"
        # to make the variables of get_updated() method accessable to all the other method of the class.
        self.get_updated()

    def get_updated(self, offset_value=None):
        try:
            if offset_value != None:
                self.full_url = f"{self.base_url}getUpdates?offset={offset_value}&timeout=100"
            else:
                self.full_url = f"{self.base_url}getUpdates?timeout=100"
            # print(self.full_url)  # to print the url n test it in the browser
            r = requests.get(self.full_url)
            self.rec_data = r.json()
            return self.rec_data
        except Exception:
            print("get_upated() got errors")

    def lastUpdate_id(self):
        try:
            self.update_id = self.rec_data["result"][-1]["update_id"]
            return self.update_id
        except Exception:
            return None

    def first_update_id(self):
        try:
            self.update_id = self.rec_data["result"][0]["update_id"]
            return self.update_id
        except Exception:
            return None

    def process(self, update_id, chat_id):
        rec_mssg_pincode = self.get_mssg_by_id(update_id)

        info = vaccineSlotsInfo(rec_mssg_pincode)
        if info:
            for x in info:
                # t = threading.Thread(target=self.mssg_send, args=(chat_id, x))
                # t.start()
                self.mssg_send(chat_id, x)
            print(
                f"\n\nAll mssgs sent to {chat_id}, update_id:{update_id} for pin:{rec_mssg_pincode}\n\n")
        else:
            print(
                f"\nmssgs probably not sent to {chat_id} for pincode: {rec_mssg_pincode}\n\n")

    def mssg_send(self, chatid, mssg):
        try:
            full_url = f"{self.base_url}sendMessage?chat_id={chatid}&text={mssg}"
            resp = requests.post(full_url)
            if str(resp) != "<Response [200]>":
                print(
                    f"mssg not sent successfully !!\n ERROR CODE is {resp}")
                return 0
            else:
                print("mssg sent")
                return 1
        except Exception:
            print("mss_send() didn't execute properly")
            return 0

    # def loop(self, first, last):
    #     try:
    #         for i in range(first, last+1):
    #             this_chat_id = 1  # ?????
    #             if i not in self.visited:
    #                 t = threading.Thread(
    #                     target=self.process, args=(i, this_chat_id))
    #                 t.start()
    #                 print(f"\n\n\nprocess thread started for id {i}\n\n\n")
    #     except Exception as err:
    #         print(err)

    def get_first_Chat_id(self):
        try:
            self.chat_id = self.rec_data["result"][0]["message"]["chat"]["id"]
            return self.chat_id
        except Exception:
            return None

    def get_mssg_by_id(self, update_id):
        try:
            for d in self.rec_data["result"]:
                if update_id == d["update_id"]:
                    recvd_mssg = d["message"]["text"]
            return recvd_mssg
        except Exception:
            print("Something wrong in receiving text from tg bot")
            return None

    def getLastmssg(self):
        try:
            self.last_recmssg = self.rec_data["result"][-1]["message"]["text"]
            return self.last_recmssg
        except Exception:
            print("Something wrong in receiving text from tg bot")
            return None

    def mssg_send(self, chatid, mssg):
        try:
            self.full_url = f"{self.base_url}sendMessage?chat_id={chatid}&text={mssg}"
            resp = requests.post(self.full_url)
            if str(resp) != "<Response [200]>":
                print(f"mssg not sent successfully !!\n ERROR CODE is {resp}")
                return 0
            else:
                print("mssg sent successfully")
                return 1
        except Exception:
            print("mss_send() didn't execute properly")
            return 0


if __name__ == "__main__":
    obj1 = CovidStatsBot()
    print(obj1.get_updated())
    obj1.loop()
