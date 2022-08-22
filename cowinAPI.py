import requests
from datetime import date

flag = 1


def vaccineSlotsInfo(pin, date=(date.today()).strftime("%d-%m-%Y")):
    global flag
    try:
        if str(type(int(pin))) == "<class 'int'>":
            flag = 1
        else:
            flag = 0
    except Exception:
        return ["probably Not a pincode"]
    if not flag:
        return ["did not work"]
    try:
        full_url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={pin}&date={date}"
        # print("full url = ", full_url)
        req = requests.get(full_url)
        received_data = req.json()
        # print(received_data)
        info_list = []
        for list_items in received_data["sessions"]:
            slot = f'name = {list_items["name"]}\naddress = {list_items["address"]}\nstate name = {list_items["state_name"]}\ndistrict name = {list_items["district_name"]}\nblock name = {list_items["block_name"]}\npincode = {list_items["pincode"]}\nfrom {list_items["from"]} to {list_items["to"]}\nfee : {list_items["fee_type"]}\nvaccine type : {list_items["vaccine"]}\n'

            info_list.append(slot)

        if info_list:
            return info_list
        else:
            return ["No data found for this pincode, try another one"]
    except Exception:
        return ["Probably some error occured due to wrong ipnut"]


if __name__ == "__main__":
    today = date.today()

    # dd/mm/YY
    thedate = today.strftime("%d-%m-%Y")
    # print("d1 =", thedate)

    pincode = '110085'

    print(vaccineSlotsInfo(pincode))
