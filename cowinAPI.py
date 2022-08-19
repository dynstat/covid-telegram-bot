import requests
from datetime import date

today = date.today()

# dd/mm/YY
thedate = today.strftime("%d-%m-%Y")
# print("d1 =", thedate)
# https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode=110085&date=26-06-2021

pincode = '110085'


def vaccineSlotsInfo(pin, date=thedate):
    try:
        full_url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={pin}&date={date}"
        print("full url = ", full_url)
        req = requests.get(full_url)
        received_data = req.json()
        # print(received_data)
        info_list = []
        for list_items in received_data["sessions"]:
            slot = f'name = {list_items["name"]}\naddress = {list_items["address"]}\nstate name = {list_items["state_name"]}\ndistrict name = {list_items["district_name"]}\nblock name = {list_items["block_name"]}\npincode = {list_items["pincode"]}\nfrom {list_items["from"]} to {list_items["to"]}\nfee : {list_items["fee_type"]}\nvaccine type : {list_items["vaccine"]}\n'

            info_list.append(slot)
        return info_list
    except Exception:
        return None
