import tkinter as tk
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk
import requests
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def get_weather(city):
    API_key = "f313b4029cda41ba41fda9d8b2c83e4b"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        messagebox.showerror("HTTP Error", f"HTTP Error: {errh}")
        return None
    except requests.exceptions.ConnectionError as errc:
        messagebox.showerror("Error Connecting", f"Error Connecting: {errc}")
        return None
    except requests.exceptions.Timeout as errt:
        messagebox.showerror("Timeout Error", f"Timeout Error: {errt}")
        return None
    except requests.exceptions.RequestException as err:
        messagebox.showerror("Error", f"An Error Occurred: {err}")
        return None

    weather = res.json()
    if res.status_code == 404:
        messagebox.showerror("Error", "City not found.")
        return None

    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp'] - 273.15
    description = weather['weather'][0]['description']
    city = weather['name']
    country = weather['sys']['country']
    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return icon_url, temperature, description, city, country

def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return
    icon_url, temperature, description, city, country = result
    location_label.configure(text=f"{city}, {country}")
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon
    temperature_label.configure(text=f"Temperature: {temperature:.2f} ˚C")
    description_label.configure(text=f"Description: {description}")

root = ttk.Window(themename="darkly")
root.title("Weather App")
root.geometry("400x400")
root_icon = PhotoImage(file="icon.png")
root.iconphoto (False, root_icon)

city_entry = ttk.Entry(root, font="Helvetica, 18")
city_entry.pack(pady=10)

search_button = ttk.Button(root, text="Search", bootstyle=PRIMARY, command=search)
search_button.pack(pady=10)

location_label = ttk.Label(root, font="Helvetica, 25")
location_label.pack(pady=20)

icon_label = ttk.Label(root)
icon_label.pack()

temperature_label = ttk.Label(root, font="Helvetica, 20")
temperature_label.pack()

description_label = ttk.Label(root, font="Helvetica, 20")
description_label.pack()

root.mainloop()
