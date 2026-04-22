import tkinter as tk

from weather_service import WeatherAppError, get_location, get_weather


def temp_logo(temp: float) -> tk.PhotoImage:
    if temp >= 27:
        return hot_icon
    if temp >= 20:
        return cool_icon
    return cold_icon


def wind_scale(wind: float) -> str:
    if wind >= 20:
        return "Strong gale"
    if wind >= 10:
        return "Fresh breeze"
    return "Gentle breeze"


def reset_weather_labels() -> None:
    location_value.config(text="-")
    temp_value.config(text="Temperature: -", image="", compound="none")
    wind_value.config(text="Wind: -")
    humidity_value.config(text="Humidity: -")
    condition_value.config(text="Condition: -")
    forecast_value.config(text="Today's forecast: -")


def search_weather() -> None:
    status_label.config(text="", fg="#0f172a")

    try:
        location = get_location(search_input.get())
        weather = get_weather(location.latitude, location.longitude)
    except WeatherAppError as exc:
        reset_weather_labels()
        status_label.config(text=str(exc), fg="#b91c1c")
        return

    location_value.config(text=location.display_name)
    temp_value.config(
        text=f"Temperature: {weather.temperature_c:.1f} deg C",
        image=temp_logo(weather.temperature_c),
        compound="right",
    )
    wind_value.config(
        text=f"Wind: {weather.wind_speed_kph:.1f} km/h ({wind_scale(weather.wind_speed_kph)})"
    )
    humidity_value.config(text=f"Humidity: {weather.humidity_percent}%")
    condition_value.config(text=f"Condition: {weather.condition}")
    forecast_value.config(
        text=f"Today's forecast: H {weather.today_max_c:.1f} deg C / L {weather.today_min_c:.1f} deg C"
    )
    status_label.config(text="Weather updated successfully.", fg="#166534")


def on_enter(event: tk.Event) -> None:
    search_weather()


window = tk.Tk()
window.geometry("520x480")
window.resizable(False, False)
window.title("Simple Weather App")
window.config(background="#d9f1ff")

app_icon = tk.PhotoImage(file="logo/weather.png")
search_logo = tk.PhotoImage(file="logo/magnifier.png")
hot_icon = tk.PhotoImage(file="logo/hot.png")
cool_icon = tk.PhotoImage(file="logo/cool.png")
cold_icon = tk.PhotoImage(file="logo/cold.png")

window.iconphoto(True, app_icon)

header = tk.Frame(window, bg="#d9f1ff")
header.pack(pady=(20, 12))

main_label = tk.Label(
    header,
    text="Simple Weather App",
    font=("Roboto", 22, "bold"),
    fg="#0f172a",
    bg="#d9f1ff",
    image=app_icon,
    compound="right",
    padx=8,
)
main_label.pack()

search_frame = tk.Frame(window, bg="#d9f1ff")
search_frame.pack(pady=(0, 16))

search_input = tk.Entry(search_frame, font=("Roboto", 18), width=22, justify="center")
search_input.grid(row=0, column=0, padx=(0, 10))
search_input.bind("<Return>", on_enter)

search_button = tk.Button(
    search_frame,
    text="Search",
    command=search_weather,
    font=("Roboto", 14, "bold"),
    bg="#8bd3ff",
    fg="#0f172a",
    activebackground="#62e9f3",
    image=search_logo,
    compound="right",
    padx=10,
)
search_button.grid(row=0, column=1)

results_card = tk.Frame(window, bg="#f8fdff", bd=1, relief="solid", padx=18, pady=18)
results_card.pack(fill="both", expand=True, padx=24, pady=(0, 24))

location_value = tk.Label(
    results_card,
    text="-",
    font=("Roboto", 16, "bold"),
    fg="#0f172a",
    bg="#f8fdff",
    wraplength=420,
    justify="center",
)
location_value.pack(pady=(0, 14))

temp_value = tk.Label(
    results_card,
    text="Temperature: -",
    font=("Roboto", 14),
    fg="#0f172a",
    bg="#f8fdff",
)
temp_value.pack(anchor="w", pady=4)

wind_value = tk.Label(
    results_card,
    text="Wind: -",
    font=("Roboto", 14),
    fg="#0f172a",
    bg="#f8fdff",
)
wind_value.pack(anchor="w", pady=4)

humidity_value = tk.Label(
    results_card,
    text="Humidity: -",
    font=("Roboto", 14),
    fg="#0f172a",
    bg="#f8fdff",
)
humidity_value.pack(anchor="w", pady=4)

condition_value = tk.Label(
    results_card,
    text="Condition: -",
    font=("Roboto", 14),
    fg="#0f172a",
    bg="#f8fdff",
)
condition_value.pack(anchor="w", pady=4)

forecast_value = tk.Label(
    results_card,
    text="Today's forecast: -",
    font=("Roboto", 14),
    fg="#0f172a",
    bg="#f8fdff",
)
forecast_value.pack(anchor="w", pady=4)

status_label = tk.Label(
    results_card,
    text="Search for a city to load weather details.",
    font=("Roboto", 12),
    fg="#334155",
    bg="#f8fdff",
    wraplength=420,
    justify="center",
)
status_label.pack(side="bottom", pady=(18, 0))

window.mainloop()
