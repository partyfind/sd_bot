import requests
import csv
import time
from datetime import datetime

date = '2023-03-13'#input("Enter date (YYYY-MM-DD): ")
cities = [1,2,99]#input("Enter cities (separated by commas): ").split(",")
keywords = ["рок", "туса", "концерт"]

found_events = []
for city in cities:
    for keyword in keywords:
        time.sleep(0.5)
        params = {
            "access_token": 'vk1.a.aqPe2HFk_9Ses4Qk4I5BEv89MK6gIaz_SjhYdy1M1rXWzrnOkCao6janBvI97wLk1NY-V-q9HJf2bEFMfSIZKFVA6z7VWLAwFFR50xUMD-4WDwYTAGFYw9QyKVK3qtmO9SQGvf8NkYEa_97qAbNZFm6FH1xdmT9qoPsKT7HQLoXSuciaRsVRp3uO0zSjtgvTFOK7eTHpN_9uFVgeJwiDeA',
            "v": '5.131',
            "q": keyword,
            "type": "event",
            "start_time": '2023-03-13',
            "future": '1',
            "city_id": city,
            "count": 5
        }
        response = requests.get("https://api.vk.com/method/groups.search", params)
        print(keyword)
        print(city)
        if response.status_code == 200:
            data = response.json()
            if "response" in data:
                found_events.extend(data["response"]["items"])
            else:
                print("Error: No response data found")
        else:
            print("Error: API request failed")
print(len(found_events))
get_by_id_params = {
    "fields": "start_date,finish_date,description,city",
    "access_token": 'vk1.a.aqPe2HFk_9Ses4Qk4I5BEv89MK6gIaz_SjhYdy1M1rXWzrnOkCao6janBvI97wLk1NY-V-q9HJf2bEFMfSIZKFVA6z7VWLAwFFR50xUMD-4WDwYTAGFYw9QyKVK3qtmO9SQGvf8NkYEa_97qAbNZFm6FH1xdmT9qoPsKT7HQLoXSuciaRsVRp3uO0zSjtgvTFOK7eTHpN_9uFVgeJwiDeA',
    "v": "5.131"  # VKontakte API version
}
group_details = []
for event in found_events:
    get_by_id_params["group_ids"] = int(event["id"])
    response = requests.get("https://api.vk.com/method/groups.getById", params=get_by_id_params)
    time.sleep(0.5)
    response_json = response.json()
    group_details.append(response_json["response"][0])

#Write the found events data to a CSV file
with open("events.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Event Title", "City", "Description", "Start Time"])
    for party in group_details:
        print(party)
        if party.get('city'):
            s = party["screen_name"]
            writer.writerow([party["city"]["title"],
                             party["name"],
                             "=HYPERLINK(\"https://vk.com/"+s+"\";\""+s+"\")",
                             datetime.fromtimestamp(party["start_date"]).strftime("%d.%m.%Y"),
                             '',
                             party["description"]])
        else:
            print(party['id'])

print("Events data has been written to events.csv file.")