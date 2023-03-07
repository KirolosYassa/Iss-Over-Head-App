from email.message import EmailMessage
import os
from dotenv import load_dotenv
import requests
import datetime
import smtplib
import time


load_dotenv()

email = os.getenv('EMAIL')
passWord = os.getenv('PASSWORD')
to_mail = os.getenv('TO_MAIL')
MY_LAT = os.getenv('MY_LAT')
MY_LONG = os.getenv('MY_LONG')
MY_LAT = float(MY_LAT)
MY_LONG = float(MY_LONG)
print(MY_LAT, MY_LONG)

def is_above():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    print(data)
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    #Your position is within +5 or -5 degrees of the ISS position.
    # is_above_me = True if (MY_LAT + 5 > iss_latitude or MY_LAT - 5 < iss_latitude) and (MY_LONG + 5 > iss_longitude or MY_LONG - 5 < iss_longitude) else False
    is_above_me = True if (MY_LAT + 5 >= iss_latitude >= MY_LAT - 5 and MY_LONG + 5 >= iss_longitude >= MY_LONG - 5) else False
    return is_above_me


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.datetime.now()
    hour_now = time_now.hour
    print(sunrise)
    print(sunset)
    print(hour_now)
    is_dark = True if hour_now < sunrise or hour_now > sunset else False
    return is_dark



def run():

    subject = f"Look Up! Iss is now over you"
    message = f"""

    <html>
        <body>
            <div>
                <h3> 
                    Your Location is around:
                    <br>
                    Latitude: {MY_LAT}
                    <br>
                    Longitude: {MY_LONG}
                </h3>
            </div>
            <hr>
            <h2>
                Look Up! The ISS is now over you, enjoy it!
            </h2>
        </body>
    </html>
    """


    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email 
    msg['To'] = to_mail
    msg.set_content(message, subtype='html')


    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=email, password=passWord)
        connection.send_message(msg)


while True:
    is_dark_and_above_me = True if is_night() and is_above() else False
    print(f"is_dark_and_above_me = {is_dark_and_above_me}")
    if not is_dark_and_above_me:
        run()
    time.sleep(60)