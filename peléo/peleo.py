from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import *
import requests
import pytz
from PIL import Image, ImageTk
import schedule
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

root = Tk()
root.title("Peleo")
root.geometry("890x470+300+200")
root.configure(bg="#57adff")
root.resizable(False, False)


def sendWeatherAlert(city, weather_alerts):
    if any(weather_alerts.values()):
        sender_email = "xxxxxxx@gmail.com"
        sender_password = "xxxxxxx"
        receiver_email = "xxxxxxx@gmail.com"

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = "Peleo Hava Durumu Uyarısı"

        body = f"Sayın Kullanıcı;\n\n{city.capitalize()} şehrinde bugün, "

        for weather, recommendation in weather_alerts.items():
            if recommendation:
                body += f"{weather}: {recommendation} "

        body += "\n\nİyi günler dileriz.\n-Peleo"

        message.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())


def getWeather():
    city = textfield.get()

    geolocator = Nominatim(user_agent="weatherApp")
    location = geolocator.geocode(city)

    if location is None:
        messagebox.showerror("Hata", f"{city} bulunamadı. Lütfen geçerli bir şehir adı girin.")
        return

    obj = TimezoneFinder()

    result = obj.timezone_at(lng=location.longitude, lat=location.latitude)

    timezone.config(text=result)
    long_lat.config(text=f"{round(location.latitude, 4)}°N, {round(location.longitude, 4)}°E")
    home = pytz.timezone(result)
    local_time = datetime.now(home)
    current_time = local_time.strftime("%I:%M %p")
    clock.config(text=current_time)

    api = "https://api.openweathermap.org/data/3.0/onecall?lat=" + str(location.latitude) + "&lon=" + str(
        location.longitude) + "&units=metric&exclude=hourly&appid=xxxxxxxxxx&lang=tr"
    json_data = requests.get(api).json()

    temp = json_data['current']['temp']
    humidity = json_data['current']['humidity']
    pressure = json_data['current']['pressure']
    wind = json_data['current']['wind_speed']
    description = json_data['current']['weather'][0]['description']
    t.config(text=(temp, "°C"))
    h.config(text=(humidity, "%"))
    p.config(text=(pressure, "hPa"))
    w.config(text=(wind, "m/s"))
    d.config(text=description)

    weather_alerts = {
        "kar yağışı bekleniyor": "Bot, eldiven ve bere giymeyi unutmayınız." if 'snow' in json_data['daily'][0] and
                                                                                  json_data['daily'][0][
                                                                                      'snow'] > 0.5 else None,
        "toz seviyesinin yüksek olması bekleniyor": "Maske takmayı unutmayınız." if 'dust' in json_data['daily'][0] and
                                                                                    json_data['daily'][0][
                                                                                        'dust'] > 50 else None,
        "fırtına bekleniyor": "Sıkı giyinmenizi ve dikkatli olmanızı öneririz." if 'Thunderstorm' in
                                                                                   json_data['daily'][0]['weather'][0][
                                                                                       'main'] == 'Thunderstorm' else None,
        "şiddetli rüzgar bekleniyor": "Açık alanda dikkatli olmanızı öneririz." if json_data['daily'][0][
                                                                                       'wind_speed'] > 15 else None,
        "uv seviyesinin yüksek olması bekleniyor": "Güneş gözlüğü takmayı ve güneş kremi kullanılmayı unutmayınız." if
        json_data['daily'][0]['uvi'] > 7 else None,
        "yağmur bekleniyor": "Şemsiyenizi almayı unutmayınız." if 'rain' in json_data['daily'][0] and
                                                                  json_data['daily'][0]['rain'] > 0.5 else None
    }

    sendWeatherAlert(city, weather_alerts)

    #gün1
    firstdayimage = json_data['daily'][0]['weather'][0]['icon']

    photo1 = ImageTk.PhotoImage(file=f"icon/{firstdayimage}@2x.png")
    firstimage.config(image=photo1)
    firstimage.image = photo1

    tempday1 = json_data['daily'][0]['temp']['day']
    tempnight1 = json_data['daily'][0]['temp']['night']

    day1temp.config(text=f"Gün:{tempday1}°C\n Gece:{tempnight1}°C")

    #gün2
    seconddayimage = json_data['daily'][1]['weather'][0]['icon']

    img = Image.open(f"icon/{seconddayimage}@2x.png")
    resized_image = img.resize((50, 50))
    photo2 = ImageTk.PhotoImage(resized_image)
    secondimage.config(image=photo2)
    secondimage.image = photo2

    tempday2 = json_data['daily'][1]['temp']['day']
    tempnight2 = json_data['daily'][1]['temp']['night']

    day2temp.config(text=f"Gün:{tempday2}°C\n Gece:{tempnight2}°C")

    #gün3
    thirddayimage = json_data['daily'][2]['weather'][0]['icon']

    img = Image.open(f"icon/{thirddayimage}@2x.png")
    resized_image = img.resize((50, 50))
    photo3 = ImageTk.PhotoImage(resized_image)
    thirdimage.config(image=photo3)
    thirdimage.image = photo3

    tempday3 = json_data['daily'][2]['temp']['day']
    tempnight3 = json_data['daily'][2]['temp']['night']

    day3temp.config(text=f"Gün:{tempday3}°C\n Gece:{tempnight3}°C")

    #gün4
    fourthdayimage = json_data['daily'][3]['weather'][0]['icon']

    img = Image.open(f"icon/{fourthdayimage}@2x.png")
    resized_image = img.resize((50, 50))
    photo4 = ImageTk.PhotoImage(resized_image)
    fourthimage.config(image=photo4)
    fourthimage.image = photo4

    tempday4 = json_data['daily'][3]['temp']['day']
    tempnight4 = json_data['daily'][3]['temp']['night']

    day4temp.config(text=f"Gün:{tempday4}°C\n Gece:{tempnight4}°C")

    #gün5
    fifthdayimage = json_data['daily'][4]['weather'][0]['icon']

    img = Image.open(f"icon/{fifthdayimage}@2x.png")
    resized_image = img.resize((50, 50))
    photo5 = ImageTk.PhotoImage(resized_image)
    fifthimage.config(image=photo5)
    fifthimage.image = photo5

    tempday5 = json_data['daily'][4]['temp']['day']
    tempnight5 = json_data['daily'][4]['temp']['night']

    day5temp.config(text=f"Gün:{tempday5}°C\n Gece:{tempnight5}°C")

    #gün6
    sixthdayimage = json_data['daily'][5]['weather'][0]['icon']

    img = Image.open(f"icon/{sixthdayimage}@2x.png")
    resized_image = img.resize((50, 50))
    photo6 = ImageTk.PhotoImage(resized_image)
    sixthimage.config(image=photo6)
    sixthimage.image = photo6

    tempday6 = json_data['daily'][5]['temp']['day']
    tempnight6 = json_data['daily'][5]['temp']['night']

    day6temp.config(text=f"Gün:{tempday6}°C\n Gece:{tempnight6}°C")

    #gün7
    seventhdayimage = json_data['daily'][6]['weather'][0]['icon']

    img = Image.open(f"icon/{seventhdayimage}@2x.png")
    resized_image = img.resize((50, 50))
    photo7 = ImageTk.PhotoImage(resized_image)
    seventhimage.config(image=photo7)
    seventhimage.image = photo7

    tempday7 = json_data['daily'][6]['temp']['day']
    tempnight7 = json_data['daily'][6]['temp']['night']

    day7temp.config(text=f"Gün:{tempday7}°C\n Gece:{tempnight7}°C")

    first = datetime.now()
    day1.config(text=first.strftime("%A"))  # İngilizce gün adı
    turkish_days = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
    day1.config(text=turkish_days[first.weekday()])  # Türkçe gün adı

    second = first + timedelta(days=1)
    day2.config(text=second.strftime("%A"))  # İngilizce gün adı
    day2.config(text=turkish_days[second.weekday()])  # Türkçe gün adı

    third = first + timedelta(days=2)
    day3.config(text=third.strftime("%A"))  # İngilizce gün adı
    day3.config(text=turkish_days[third.weekday()])  # Türkçe gün adı

    fourth = first + timedelta(days=3)
    day4.config(text=fourth.strftime("%A"))  # İngilizce gün adı
    day4.config(text=turkish_days[fourth.weekday()])  # Türkçe gün adı

    fifth = first + timedelta(days=4)
    day5.config(text=fifth.strftime("%A"))  # İngilizce gün adı
    day5.config(text=turkish_days[fifth.weekday()])  # Türkçe gün adı

    sixth = first + timedelta(days=5)
    day6.config(text=sixth.strftime("%A"))  # İngilizce gün adı
    day6.config(text=turkish_days[sixth.weekday()])  # Türkçe gün adı

    seventh = first + timedelta(days=6)
    day7.config(text=seventh.strftime("%A"))  # İngilizce gün adı
    day7.config(text=turkish_days[seventh.weekday()])  # Türkçe gün adı


#iconlar vs
image_icon = PhotoImage(file="Images/logo.png")
root.iconphoto(False, image_icon)

Round_box = PhotoImage(file="Images/Rounded Rectangle 1.png")
Label(root, image=Round_box, bg="#57adff").place(x=40, y=110)

peleologo = PhotoImage(file="Images/peleologo.png")
Label(image=peleologo, bg="#57adff").place(x=700, y=100)

#günlük bilgi
label1 = Label(root, text="Sıcaklık", font=('Helvetica', 11), fg="white", bg="#141f3d")
label1.place(x=50, y=115)

label2 = Label(root, text="Nem", font=('Helvetica', 11), fg="white", bg="#141f3d")
label2.place(x=50, y=135)

label3 = Label(root, text="Basınç", font=('Helvetica', 11), fg="white", bg="#141f3d")
label3.place(x=50, y=155)

label4 = Label(root, text="Rüzgar Hızı", font=('Helvetica', 11), fg="white", bg="#141f3d")
label4.place(x=50, y=175)

label5 = Label(root, text="Açıklama", font=('Helvetica', 11), fg="white", bg="#141f3d")
label5.place(x=50, y=195)


Search_image = PhotoImage(file="Images/Rounded Rectangle 3.png")
myimage = Label(image=Search_image, bg="#57adff")
myimage.place(x=270, y=115)

weat_image = PhotoImage(file="Images/Layer 7.png")
weatherimage = Label(root, image=weat_image, bg="#141f3d")
weatherimage.place(x=288, y=123)

textfield = tk.Entry(root, justify='center', width=15, font=('poppins', 25, 'bold'), bg="#141f3d", border=0, fg="white")
textfield.place(x=370, y=130)
textfield.focus()

Search_icon = PhotoImage(file="Images/Layer 6.png")
myimage_icon = Button(image=Search_icon, borderwidth=0, cursor="hand2", bg="#141f3d", command=getWeather)
myimage_icon.place(x=630, y=125)

#alt kutular
frame = Frame(root, width=900, height=180, bg="#212120")
frame.pack(side=BOTTOM)

firstbox = PhotoImage(file="Images/Rounded Rectangle 2.png")
secondbox = PhotoImage(file="Images/Rounded Rectangle 2 copy.png")

Label(frame, image=firstbox, bg="#212120").place(x=30, y=20)
Label(frame, image=secondbox, bg="#212120").place(x=290, y=30)
Label(frame, image=secondbox, bg="#212120").place(x=390, y=30)
Label(frame, image=secondbox, bg="#212120").place(x=490, y=30)
Label(frame, image=secondbox, bg="#212120").place(x=590, y=30)
Label(frame, image=secondbox, bg="#212120").place(x=690, y=30)
Label(frame, image=secondbox, bg="#212120").place(x=790, y=30)

clock = Label(root, font=("Helvetica", 30, 'bold'), fg="white", bg="#57adff")
clock.place(x=30, y=20)

timezone = Label(root, font=("Helvetica", 20), fg="white", bg="#57adff")
timezone.place(x=650, y=20)

long_lat = Label(root, font=("Helvetica", 10), fg="white", bg="#57adff")
long_lat.place(x=650, y=50)

#günlük açıklama
t = Label(root, font=("Helvetica", 11), fg="white", bg="#141f3d")
t.place(x=150, y=115)
h = Label(root, font=("Helvetica", 11), fg="white", bg="#141f3d")
h.place(x=150, y=135)
p = Label(root, font=("Helvetica", 11), fg="white", bg="#141f3d")
p.place(x=150, y=155)
w = Label(root, font=("Helvetica", 11), fg="white", bg="#141f3d")
w.place(x=150, y=175)
d = Label(root, font=("Helvetica", 11), fg="white", bg="#141f3d")
d.place(x=150, y=195)

#gün1
firstframe = Frame(root, width=230, height=127, bg="#282829")
firstframe.place(x=35, y=315)

day1 = Label(firstframe, font="arial 20", bg="#282829", fg="#fff")
day1.place(x=100, y=5)

firstimage = Label(firstframe, bg="#282829")
firstimage.place(x=1, y=15)

day1temp = Label(firstframe, bg="#282829", fg="#57adff", font="arial 15 bold")
day1temp.place(x=100, y=50)

#gün2
secondframe = Frame(root, width=80, height=115, bg="#282829")
secondframe.place(x=294, y=325)

day2 = Label(secondframe, bg="#282829", fg="#fff")
day2.place(x=10, y=5)

secondimage = Label(secondframe, bg="#282829")
secondimage.place(x=7, y=20)

day2temp = Label(secondframe, bg="#282829", fg="#fff")
day2temp.place(x=10, y=70)

#gün3
thirdframe = Frame(root, width=80, height=115, bg="#282829")
thirdframe.place(x=394, y=325)

day3 = Label(thirdframe, bg="#282829", fg="#fff")
day3.place(x=10, y=5)

thirdimage = Label(thirdframe, bg="#282829")
thirdimage.place(x=7, y=20)

day3temp = Label(thirdframe, bg="#282829", fg="#fff")
day3temp.place(x=10, y=70)

#gün4
fourthframe = Frame(root, width=80, height=115, bg="#282829")
fourthframe.place(x=494, y=325)

day4 = Label(fourthframe, bg="#282829", fg="#fff")
day4.place(x=10, y=5)

fourthimage = Label(fourthframe, bg="#282829")
fourthimage.place(x=7, y=20)

day4temp = Label(fourthframe, bg="#282829", fg="#fff")
day4temp.place(x=10, y=70)

#gün5
fifthframe = Frame(root, width=80, height=115, bg="#282829")
fifthframe.place(x=594, y=325)

day5 = Label(fifthframe, bg="#282829", fg="#fff")
day5.place(x=10, y=5)

fifthimage = Label(fifthframe, bg="#282829")
fifthimage.place(x=7, y=20)

day5temp = Label(fifthframe, bg="#282829", fg="#fff")
day5temp.place(x=10, y=70)

#gün6
sixthframe = Frame(root, width=80, height=115, bg="#282829")
sixthframe.place(x=694, y=325)

day6 = Label(sixthframe, bg="#282829", fg="#fff")
day6.place(x=10, y=5)

sixthimage = Label(sixthframe, bg="#282829")
sixthimage.place(x=7, y=20)

day6temp = Label(sixthframe, bg="#282829", fg="#fff")
day6temp.place(x=10, y=70)

#gün7
seventhframe = Frame(root, width=80, height=115, bg="#282829")
seventhframe.place(x=794, y=325)

day7 = Label(seventhframe, bg="#282829", fg="#fff")
day7.place(x=10, y=5)

seventhimage = Label(seventhframe, bg="#282829")
seventhimage.place(x=7, y=20)

day7temp = Label(seventhframe, bg="#282829", fg="#fff")
day7temp.place(x=10, y=70)

root.mainloop()
