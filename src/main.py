import tkinter as tk
import time
import math
import requests


class AnalogClock:
    def __init__(self, root, api_key):
        self.root = root
        self.api_key = api_key
        self.root.title("Riga Analog Clock")
        self.canvas = tk.Canvas(root, width=400, height=500, bg="white")
        self.canvas.pack()

        self.center_x = 200
        self.center_y = 200
        self.clock_radius = 190

        self.draw_face()
        self.update_clock()
        self.update_weather()
        self.draw_city_name()

    def draw_face(self):
        # Рисуем круг лицевой стороны часов
        self.canvas.create_oval(self.center_x - self.clock_radius,
                                self.center_y - self.clock_radius,
                                self.center_x + self.clock_radius,
                                self.center_y + self.clock_radius,
                                outline="black", width=5)

        # Рисуем метки и цифры
        for i in range(60):
            angle = math.pi / 30 * i
            x_start = self.center_x + math.cos(angle) * (self.clock_radius - 10)
            y_start = self.center_y + math.sin(angle) * (self.clock_radius - 10)
            if i % 5 == 0:
                x_end = self.center_x + math.cos(angle) * (self.clock_radius - 20)
                y_end = self.center_y + math.sin(angle) * (self.clock_radius - 20)
                hour = (i // 5) or 12
                x_text = self.center_x + math.cos(angle - math.pi / 2) * (self.clock_radius - 40)
                y_text = self.center_y + math.sin(angle - math.pi / 2) * (self.clock_radius - 40)
                self.canvas.create_text(x_text, y_text, text=str(hour), font=("Helvetica", 20, "bold"), anchor="center")
            else:
                x_end = self.center_x + math.cos(angle) * (self.clock_radius - 15)
                y_end = self.center_y + math.sin(angle) * (self.clock_radius - 15)

            self.canvas.create_line(x_start, y_start, x_end, y_end, width=2, fill="black")

    def update_clock(self):
        self.canvas.delete("hands")

        current_time = time.localtime()
        hours = current_time.tm_hour % 12
        minutes = current_time.tm_min
        seconds = current_time.tm_sec

        second_angle = math.pi / 30 * seconds - math.pi / 2
        minute_angle = math.pi / 30 * minutes - math.pi / 2 + math.pi / 1800 * seconds
        hour_angle = math.pi / 6 * hours - math.pi / 2 + math.pi / 360 * minutes

        self.draw_hand(self.center_x, self.center_y, hour_angle, self.clock_radius * 0.5, width=8, color="black")
        self.draw_hand(self.center_x, self.center_y, minute_angle, self.clock_radius * 0.7, width=6, color="black")
        self.draw_hand(self.center_x, self.center_y, second_angle, self.clock_radius * 0.9, width=2, color="red")

        self.root.after(1000, self.update_clock)

    def update_weather(self):
        self.canvas.delete("weather")
        weather_info = get_weather(self.api_key)
        self.canvas.create_text(self.center_x, self.center_y + self.clock_radius + 20,
                                text=weather_info, font=("Helvetica", 12), anchor="center", tags="weather")

        self.root.after(600000, self.update_weather)

    def draw_city_name(self):
        self.canvas.create_text(self.center_x, self.center_y + self.clock_radius + 60,
                                text="Riga", font=("Helvetica", 16, "bold"), anchor="center", tags="city")

    def draw_hand(self, x, y, angle, length, width=2, color="black"):
        x_end = x + math.cos(angle) * length
        y_end = y + math.sin(angle) * length
        self.canvas.create_line(x, y, x_end, y_end, width=width, fill=color, tags="hands")


def get_weather(api_key, city="Riga"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()

        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']

        return f"{temperature}°C, {description.capitalize()}"
    except requests.exceptions.HTTPError as err:
        return f"Error: {err}"
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    root = tk.Tk()
    api_key = 'b571467ac02141716798e4555baa2768'  # Замените на свой актуальный API ключ
    clock = AnalogClock(root, api_key)
    root.mainloop()
