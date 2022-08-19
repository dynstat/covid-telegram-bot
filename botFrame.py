
import requests
import configparser as cfg
# ------------------------------------------------------------------------------


def read_API_fromConfig(config):
    parser = cfg.ConfigParser()
    parser.read(config)
    return parser.get('creds', 'APIKEY')


API_KEY = read_API_fromConfig('config.cfg')

print(API_KEY)


class CovidStatsBot():
    def __init__(self, offset_value=None) -> None:
        self.base_url = f"https://api.telegram.org/bot{API_KEY}/"
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

    def getCurrentChat_id(self):
        try:
            self.chat_id = self.rec_data["result"][-1]["message"]["chat"]["id"]
            return self.chat_id
        except Exception:
            return None

    def getLastmssg(self):
        try:
            self.last_recmssg = self.rec_data["result"][-1]["message"]["text"]
            return self.last_recmssg
        except Exception:
            print("Something wrong in Vaccineinfo()")
            return None

    def mssg_send(self, chatid, mssg):
        try:
            self.full_url = f"{self.base_url}sendMessage?chat_id={chatid}&text={mssg}"
            resp = requests.post(self.full_url)
            if str(resp) != "<Response [200]>":
                print(f"mssg not sent successfully !!\n ERROR CODE is {resp}")
            else:
                print(f"mssg sent successfully: {mssg}")
        except Exception:
            print("mss_send() didn't execute properly")


obj1 = CovidStatsBot()
