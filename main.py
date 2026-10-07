# To run and test the code you need to update 4 places:
# 1. Change MY_EMAIL/MY_PASSWORD to your own details.
# 2. Go to your email provider and make it allow less secure apps.
# 3. Update the SMTP ADDRESS to match your email provider.
# 4. Update birthdays.csv to contain today's month and day.
# See the solution video in the 100 Days of Python Course for explainations.


from datetime import datetime
import pandas
import random
import smtplib
import os
import requests


# import os and use it to get the Github repository secrets
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")
api_key = os.environ.get("OWM_API_KEY")
BOT_TOKEN = os.environ.get("WEATHER_BOT_TOKEN")
CHAT_ID = os.environ.get("WEATHER_CHAT_ID")

today = datetime.now()
today_tuple = (today.month, today.day)

data = pandas.read_csv("birthdays.csv")
birthdays_dict = {(data_row["month"], data_row["day"])                  : data_row for (index, data_row) in data.iterrows()}
if today_tuple in birthdays_dict:
    birthday_person = birthdays_dict[today_tuple]
    file_path = f"letter_templates/letter_{random.randint(1, 3)}.txt"
    with open(file_path) as letter_file:
        contents = letter_file.read()
        contents = contents.replace("[NAME]", birthday_person["name"])

    with smtplib.SMTP("YOUR EMAIL PROVIDER SMTP SERVER ADDRESS") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=birthday_person["email"],
            msg=f"Subject:Happy Birthday!\n\n{contents}"
        )

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message,
        },
    )

    response.raise_for_status()
    return response.json()

api_adress = 'https://api.openweathermap.org/data/2.5/forecast'
MY_LAT = 50.845100
MY_LNG = 4.264030

parameters = {
    "appid": api_key,
    "lat": MY_LAT,
    "lon": MY_LNG,
    "cnt": 4,
    "units": "metric",

}

connection = requests.get(url=api_adress, params=parameters)
connection.raise_for_status()

data = connection.json()

will_rain = False
for item in data['list']:
    weather_id = int((item['weather'][0]["id"]))
    if weather_id < 700:
        will_rain = True
    
if will_rain:
    send_telegram("It will rain today ☂️")
else:
    send_telegram("No rain predicted 🌞")

