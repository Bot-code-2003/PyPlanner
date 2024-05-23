#app.py
import requests 
from time import sleep
from tabulate import tabulate 
import csv
import os
from datetime import date
import bcrypt 

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

def main():
  keyflow("1. Register\n2. Login\n3. Logout\n")
  keyflow("Choose option: ")
  choice = input()
  match choice:
      
      case "1": 
          if register():
            username, password, city = login()
          if username is not None:
              keyflow("Login success!\n", Color.GREEN)
              keyflow(f"Hello ")
              keyflow(f"{username}", Color.MAGENTA)
              keyflow(", I am Robin, your personal productivity manager.\n")
              fetch_weather(city)
              task_manager(username)
      case "2": 
          username, password, city = login()
          if username is not None:
              keyflow("Login success!\n", Color.GREEN)
              keyflow(f"Hello ")
              keyflow(f"{username.upper()}, ", Color.CYAN) 
              keyflow("I am Robin, your personal productivity manager.\n")
              fetch_weather(city)
              task_manager(username)
      case "3":
          keyflow("Good Bye\n")
# Typing effect
def keyflow(Title, color=Color.WHITE):
  for char in Title:
    sleep(0.01)
    print(color + char, end="")
  print(Color.RESET, end="")

# Load the user info
def load_info_from_csv():
    personal_info = []
    try:
        with open('personal_info.csv', "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                personal_info.append(row)    
    except FileNotFoundError:
        pass
    return personal_info

# Save the first time user info.
def save_info_to_csv(personal_info):
    file_exists = os.path.isfile('personal_info.csv')
    with open('personal_info.csv', "a", newline="") as file:
        fieldnames = ['username', 'password', 'city']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:  # Check if file exists and is empty
            writer.writeheader()
        writer.writerows(personal_info) 

personal_info = []
def register():
    keyflow("REGISTER\n")
    keyflow("Welcome user! I am ")
    keyflow("Robin, ", Color.MAGENTA)
    keyflow("your personal productivity manager.\n")
    username = input("Username: ")
    password = input("Password: ")
    city = input("City: ")
    hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    # print("Hashed pass: ",hashed_password)
    password = hashed_password.decode('utf8')
    # print("Password: ", password)
    personal_info.append({"username": username, "password": password, "city": city})
    save_info_to_csv(personal_info)
    return True

def login():
    personal_info = load_info_from_csv()
    keyflow("LOGIN\n", Color.GREEN)
    keyflow("Welcome user! I am Robin, your personal productivity manager.\n")
    username = input("Username: ")
    password = input("Password: ")
    for info in personal_info:
        hashed_password = info['password']
        try:
            if info['username'] == username and bcrypt.checkpw(password.encode('utf8'), hashed_password.encode('utf8')):
                return info['username'], info['password'], info['city']
        except:
            pass
    keyflow("Invalid username or password. Please try again.",Color.RED)
    return None, None, None

# Fetch weather and respond accordingly
def display_weather_info(city, weather_main, temp):
    if weather_main.lower() == "rain":
        keyflow(f"☔☔ The weather currently in {city} is {weather_main} and its {temp}°F. Carry an umbrella. ☔☔",Color.YELLOW)
    elif weather_main.lower() == "thunderstorm":
        keyflow(f"⛈️⛈️ Be cautious There's a {weather_main} in {city}. The temperature is {temp}°F. Prefer staying indoor! ⛈️⛈️",Color.YELLOW)
    elif weather_main.lower() == "drizzle":
        keyflow(f"🌧️ It's drizzling in {city}. The temperature is {temp}°F. You might need an umbrella. ☂️",Color.YELLOW)
    elif weather_main.lower() == "snow":
        keyflow(f"🌨️🌨️ It's snowing in {city}! The temperature is {temp}°F. Enjoy the snow! ⛄⛄",Color.YELLOW)
    elif weather_main.lower() == "mist":
        keyflow(f"🌫️🌫️ There's mist in {city}. The temperature is {temp}°F. Drive safely! 🌫️🌫️",Color.YELLOW)
    elif weather_main.lower() == "smoke":
        keyflow(f"🚫 There's smoke in {city}. The temperature is {temp}°F. Be cautious of fire hazards. 🚫",Color.YELLOW)
    elif weather_main.lower() == "haze":
        keyflow(f"😶‍🌫️ {city} is experiencing haze. The temperature is {temp}°F. Air quality may be affected. 😶‍🌫️",Color.YELLOW)
    elif weather_main.lower() == "dust":
        keyflow(f"💨💨 Dusty conditions in {city}. The temperature is {temp}°F. Stay indoors if possible. 💨💨",Color.YELLOW)
    elif weather_main.lower() == "fog":
        keyflow(f"🌁 Watch out for fog in {city}. The temperature is {temp}°F. Drive with caution. 🌫️🌫️",Color.YELLOW)
    elif weather_main.lower() == "sand":
        keyflow(f"🟨🟨 There's sand in the air in {city}. The temperature is {temp}°F. Protect your eyes! 🟨🟨",Color.YELLOW)
    elif weather_main.lower() == "tornado":
        keyflow(f"🌪️🌪️ A tornado warning in {city}! Seek shelter immediately. The temperature is {temp}°F. 🌪️🌪️",Color.YELLOW)
    elif weather_main.lower() == "ash":
        keyflow(f"☁☁ Ash is falling in {city}. The temperature is {temp}°F. Protect yourself from ash inhalation. ☁☁",Color.YELLOW)
    elif weather_main.lower() == "squall":
        keyflow(f"A squall is expected in {city}. The temperature is {temp}°F. Secure loose items!",Color.YELLOW)
    elif weather_main.lower() == "clouds":
        keyflow(f"☁️☁️ It's cloudy in {city}. The temperature is {temp}°F. Hope for some sunshine soon! ☁️☁️",Color.YELLOW)
    else:
        keyflow(f"The weather in {city} is {weather_main}. The temperature is {temp}°F.",Color.YELLOW)
    return True

def fetch_weather(city):
    api_key = "fed93326c16e64a95eae94565cc60a22"
    while True:
        weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city.lower()}&unit=imperial&APPID={api_key}")
        weather_json = weather_data.json()
        if "cod" in weather_json and weather_json["cod"] == 200:
            if "weather" in weather_json and len(weather_json["weather"]) > 0:
                weather_main = weather_json["weather"][0]["main"]
            else:
                weather_main = "Not available!"
            if "main" in weather_json and "temp" in weather_json["main"]:
                temp = round(weather_json["main"]["temp"])
            else:
                temp = "Not available!"
                
            return display_weather_info(city, weather_main, temp)
        else:
            keyflow(f"Sorry, I'm unable to get weather info for {city}. Please try again.\n", Color.RED)
            city = input("Enter a different city: ")

# Load the tasks of user from tasks.csv if exists
def load_tasks_from_csv(name):
    tasks = []
    try:
        with open('tasks.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['User'] == name:
                    tasks.append(row)
    except FileNotFoundError:
        pass
    return tasks

# Save the user tasks to tasks.csv
def save_tasks_to_csv(tasks):
    file_exists = os.path.isfile('tasks.csv')
    with open('tasks.csv', 'a', newline='') as file: 
        fieldnames = ['Task', 'Progress', 'User']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerows(tasks)

# All the task manager working
def task_manager(name):
    today = date.today()
    print("\n--------------------")
    print("Productivity Manager")
    print("--------------------")
    while True:
        keyflow(f"{name.upper()}",Color.CYAN)
        keyflow("! These are some ways I can assist you with.\n")
        keyflow("1. Task manager\n2. Exit\n")
        choice = input("Enter your choice: ")
        if choice == "1":
            tasks = load_tasks_from_csv(name)
            newTasks = []
            while True:
                keyflow("\nMENU\n1. Add task\n2. Delete task\n3. Display\n4. Exit\n")
                todoChoice = input("Enter your choice: ")
                if todoChoice == "1":
                    task = input("Task: ")
                    progress = today.strftime("%B %d, %Y")  # Default progress
                    newTasks.append({'Task': task, 'Progress': progress, 'User': name})
                    keyflow("Task added successfully.\n", Color.GREEN)
                elif todoChoice == "2":
                    if len(tasks) == 0:
                        keyflow("No tasks to delete.\n")
                    else:
                        keyflow("DELETE TASK\n")
                        headers = ["S.no", "Task", "Progress"]
                        all_tasks = tasks + newTasks
                        table = [(i, task['Task'], task['Progress']) for i, task in enumerate(all_tasks, start=1)]
                        print(tabulate(table, headers, tablefmt="grid"))
                        choice = int(input("\nChoose the task number to delete: "))
                        if choice in range(1, len(all_tasks) + 1):
                            del all_tasks[choice - 1]
                            keyflow("Task deleted successfully.\n", Color.GREEN)
                        else:
                            keyflow("Invalid task number.", Color.RED)
                elif todoChoice == "3":
                    # print(newTasks)
                    if len(tasks)==0 and len(newTasks) == 0:
                        keyflow("No tasks to display.\n")
                    else:
                        all_tasks = newTasks + tasks
                        headers = ["S.no", "Task", "Date"]
                        table = [(i, task['Task'], task['Progress']) for i, task in enumerate(all_tasks, start=1)]
                        print("\n")
                        print(tabulate(table, headers, tablefmt="pretty"))
                        print("\n")
                elif todoChoice == "4":
                    save_tasks_to_csv(newTasks)
                    break
                else:
                    keyflow("Invalid Choice\n",Color.RED)
        elif choice == "2":
            keyflow(f"Goodbye, {name.upper()}. Have a great day!\n", Color.YELLOW)
            break
        else:
            keyflow("Invalid choice\n", Color.RED)  
            
if __name__ == "__main__":
    main()