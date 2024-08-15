import tkinter as tk
import time
import math
import requests
import json
import calendar
import os


class AnalogClock:
    def __init__(self, root, api_key):
        self.root = root
        self.api_key = api_key
        self.lang = 'en'
        self.translations = self.load_translations(self.lang)

        # Устанавливаем название окна сразу после инициализации
        self.root.title(self.translations.get('app_title', 'Analog Clock'))

        self.canvas = tk.Canvas(root, width=800, height=500, bg="white")
        self.canvas.pack()

        self.center_x = 200
        self.center_y = 200
        self.clock_radius = 190

        self.create_menu()
        self.draw_face()
        self.update_clock()
        self.update_weather()
        self.display_holidays()
        self.draw_city_name()

    def load_translations(self, lang):
        """Загрузка перевода для текущего языка"""
        try:
            translation_file = f"{lang}.json"
            if os.path.exists(translation_file):
                with open(translation_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            return {}  # Возвращаем пустой словарь, если файл не найден
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Ошибка при загрузке файла перевода {lang}.json: {e}")
            return {}  # Пустой словарь при ошибке загрузки файла

    def create_menu(self):
        """Создание меню для выбора языка"""
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        lang_menu = tk.Menu(menu)
        menu.add_cascade(label=self.translations.get('language_menu', 'Language'), menu=lang_menu)
        lang_menu.add_command(label=self.translations.get('english', 'English'),
                              command=lambda: self.change_language('en'))
        lang_menu.add_command(label=self.translations.get('russian', 'Русский'),
                              command=lambda: self.change_language('ru'))

    def change_language(self, lang):
        """Изменение языка приложения"""
        self.lang = lang
        self.translations = self.load_translations(lang)
        self.root.title(self.translations.get('app_title', 'Analog Clock'))  # Обновляем название окна
        self.display_holidays()
        self.draw_city_name()

    def draw_face(self):
        # лицевой круг стороны часов
        self.canvas.create_oval(self.center_x - self.clock_radius,
                                self.center_y - self.clock_radius,
                                self.center_x + self.clock_radius,
                                self.center_y + self.clock_radius,
                                outline="blue", width=5)

        # метки и цифры
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

    def display_holidays(self):
        self.canvas.delete("holidays")
        current_month = time.localtime().tm_mon
        holidays = self.translations.get('holidays', {}).get(str(current_month), [])
        month_name = self.translations.get('month_names', {}).get(str(current_month), calendar.month_name[current_month])
        holidays_text = f"{self.translations.get('holidays_title', 'Holidays in')} {month_name}:\n\n" + \
                        "\n".join(
                            [f"{day}. {name}" for day_name_pair in holidays for day, name in day_name_pair.items()])
        self.canvas.create_text(self.center_x + 400, self.center_y - 120, text=holidays_text,
                                font=("Helvetica", 12), anchor="center", tags="holidays")

    def draw_city_name(self):
        self.canvas.delete("city")
        self.canvas.create_text(self.center_x, self.center_y + self.clock_radius + 60,
                                text=self.translations.get('city_name', 'Riga'), font=("Helvetica", 16, "bold"),
                                anchor="center", tags="city")

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

        temperature = round(weather_data['main']['temp'])
        description = weather_data['weather'][0]['description']

        return f"{temperature}°C, {description.capitalize()}"
    except requests.exceptions.RequestException:
        return "Weather data unavailable"
    except KeyError:
        return "Invalid weather data format"
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    root = tk.Tk()
    api_key = 'b571467ac02141716798e4555baa2768'  # актуальный API ключ
    clock = AnalogClock(root, api_key)
    root.mainloop()
