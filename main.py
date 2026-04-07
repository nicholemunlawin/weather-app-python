from tkinter import *
import requests


# ---------------------------- FUNCTIONS ----------------------------


# Get latitude and longitude values based on location name
def get_location():
    lat, long = 0, 0
    location = search_input.get().strip().lower()

    # Checks if no search input
    if not location:
        input_label.config(
            text="Please enter a location to search",
            font=("Roboto", 14),
        )
        input_label.place(relx=0.175, rely=0.65)
        return
    else:
        input_label.config(
            text="",
            font=("Roboto", 14),
        )

    response = requests.get(
        f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=en&format=json"
    )
    if response.status_code == 200:
        data = response.json()
        try:
            lat = data["results"][0]["latitude"]
            long = data["results"][0]["longitude"]
        except:
            input_label.config(
                text="Location not found!",
                font=("Roboto", 14),
            )
            input_label.place(relx=0.3, rely=0.65)
            return
    else:
        print(f"An error occured: {response.status.code}")

    return lat, long


# Get weather data based on latitude and longitude
def get_weather(lat, long):
    temp = 0
    wind = 0
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )
    if response.status_code == 200:
        data = response.json()
        try:
            temp = data["current"]["temperature_2m"]
            wind = data["current"]["wind_speed_10m"]
        except:
            return
    else:
        print(f"An error occured: {response.status.code}")

    return temp, wind


# Function to choose logo based on temperature
def temp_logo(temp):
    global temp_icon
    if temp >= 27:
        temp_icon = PhotoImage(file="logo/hot.png")
    elif temp >= 20:
        temp_icon = PhotoImage(file="logo/cool.png")
    else:
        temp_icon = PhotoImage(file="logo/cold.png")

    return temp_icon


# Function to show wind scale in words
def wind_scale(wind):
    global wind_speed
    if wind >= 20:
        wind_speed = "Strong gale"
    elif wind >= 10:
        wind_speed = "Fresh breeze"
    else:
        wind_speed = "Gentle breeze"

    return wind_speed


# Function for input if pressed "Enter" key
def on_enter(event):
    on_click()


# Button function
def on_click():
    try:
        lat, long = get_location()
        temp, wind = get_weather(lat, long)
        temp_label.config(
            text=f"Temperature: {temp}°C", image=temp_logo(temp), compound="right"
        )
        wind_label.config(text=f"Wind: {wind}kph ({wind_scale(wind)})")
    except:
        temp_label.config(text="Temperature:", image="")
        wind_label.config(text="Wind:")


# ---------------------------- GUI ----------------------------

# Instantiate an instance of a window
window = Tk()
window.geometry("420x420")
window.title("Simple Weather App")


# Instantiate an instance of the logos
icon = PhotoImage(file="logo/weather.png")
search_logo = PhotoImage(file="logo/magnifier.png")


# Add logo to windows
window.iconphoto(True, icon)
window.config(background="light blue")


# Label of the application
main_label = Label(window, text="Simple Weather App")
main_label.config(
    font=("Roboto", 20, "bold"),
    fg="black",
    bg="light blue",
    image=icon,
    compound="right",
)
main_label.pack(padx=5, pady=20)


# Create search box input
search_input = Entry(window)
search_input.config(font=("Roboto", 20))
search_input.pack()


# Create temperature label
temp_label = Label(window, text="Temperature:")
temp_label.config(
    font=("Roboto", 14),
    fg="black",
    bg="light blue",
)
temp_label.place(relx=0.15, rely=0.4)


# Create wind label
wind_label = Label(window, text="Wind:")
wind_label.config(
    font=("Roboto", 14),
    fg="black",
    bg="light blue",
)
wind_label.place(relx=0.3, rely=0.5)


# Create status label for input
input_label = Label(window)
input_label.config(
    bg="light blue",
)
input_label.place(relx=0.3, rely=0.65)


# Bind search bar to function after "Enter" key press
search_input.bind("<Return>", on_enter)


# Add a search button
button = Button(window, text="Search")
button.config(
    command=on_click,
    font=("Roboto", 16, "bold"),
    bg="light blue",
    fg="black",
    activebackground="#62e9f3",
    image=search_logo,
    compound="right",
    padx=10,
)
button.pack(side=BOTTOM, pady=40)


# Create window on computer screen
window.mainloop()
