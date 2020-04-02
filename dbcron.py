import requests
import sqlite3
import datetime
import config
import time

conn = sqlite3.connect(config.database["filename"], check_same_thread=False)


def global_stats():
    now = datetime.datetime.now()
    response = requests.get("https://corona.lmao.ninja/all")
    data = response.json()
    c = conn.cursor()
    with conn:
        c.execute("DELETE FROM stats")
        c.execute(f"""INSERT INTO stats VALUES (
                    '{data['cases']}', 
                    '{data['deaths']}', 
                    '{data['recovered']}', 
                    '{data['active']}',
                    '{convert_updated(data['updated'])}')""")

    print(f'General data updated: {now.strftime("%Y-%m-%d %H:%M:%S")}')


def top_countries():
    response = requests.get("https://corona.lmao.ninja/countries?sort=cases")
    data = response.json()
    c = conn.cursor()
    with conn:
        c.execute("DELETE FROM countries")
        for country in data:
            c.execute(f"""INSERT INTO countries VALUES (
                        '{country['country']}', 
                        '{country['cases']}', 
                        '{country['deaths']}', 
                        '{country['recovered']}',
                        '{country['active']}',
                        '{convert_updated(country['updated'])}')""")
    now = datetime.datetime.now()
    print(f'Data for countries updated: {now.strftime("%Y-%m-%d %H:%M:%S")}')


def convert_updated(milliseconds):
    seconds, _ = divmod(milliseconds, 1000)
    timedate = datetime.datetime.fromtimestamp(seconds)
    return timedate


global_stats()
time.sleep(3)
top_countries()