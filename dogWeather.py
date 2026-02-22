import os
import time
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, render_template

# --- タイムゾーンの設定 ---
os.environ['TZ'] = 'Asia/Tokyo'
try:
    time.tzset()
except AttributeError:
    pass

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

app = Flask(__name__)

# --- 設定値 ---
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
DOG_URL = "https://dog.ceo/api/breeds/image/random"
TARGET_HOURS = [9, 15]  # ← ハードコード回避
REQUEST_TIMEOUT = 5     # ← timeout追加

CITIES = {
    "23区": "Chiyoda",
    "多摩地区": "Hachioji"
}

# --- APIキー未設定チェック ---
if not API_KEY:
    app.logger.error("OPENWEATHER_API_KEY is not set.")


def format_datetime(dt_txt):
    dt = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    today = now.date()
    tomorrow = today + timedelta(days=1)
    day_after_tomorrow = today + timedelta(days=2)

    if dt.date() == today:
        day_str = "今日"
    elif dt.date() == tomorrow:
        day_str = "明日"
    elif dt.date() == day_after_tomorrow:
        day_str = "明後日"
    else:
        day_str = dt.strftime("%m/%d")

    ampm = "午前" if dt.hour < 12 else "午後"
    return f"{day_str}の{ampm}"


def get_weather_info(icon_code):
    icon_id = icon_code[:2]
    emoji_map = {
        "01": "☀️", "02": "🌤️", "03": "☁️", "04": "☁️",
        "09": "🌧️", "10": "☔️", "11": "⛈️", "13": "⛄️", "50": "🌫️"
    }
    return emoji_map.get(icon_id, "🌈"), icon_id


def get_target_forecast(city_name):
    now = datetime.now()
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ja"
    }

    try:
        res = requests.get(FORECAST_URL, params=params, timeout=REQUEST_TIMEOUT)
        res.raise_for_status()  # ← ステータスコード確認
        response = res.json()

        results = []
        if "list" in response:
            for item in response["list"]:
                dt = datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S")
                if dt > now and dt.hour in TARGET_HOURS:
                    emoji, icon_id = get_weather_info(item["weather"][0]["icon"])
                    results.append({
                        "time": format_datetime(item["dt_txt"]),
                        "desc": emoji,
                        "icon_id": icon_id,
                        "temp": round(item["main"]["temp"])
                    })
                if len(results) >= 6:
                    break
        return results

    except requests.exceptions.RequestException as e:
        app.logger.error(f"Weather API request failed: {e}")
        return []


@app.route('/')
def home():
    all_weather = {}
    for display_name, city_name in CITIES.items():
        all_weather[display_name] = get_target_forecast(city_name)

    comment = "今日も一日頑張るワン！"
    current_month = datetime.now().month

    if "23区" in all_weather and len(all_weather["23区"]) > 0:
        forecast_list = all_weather["23区"]
        target_forecast = forecast_list[0]

        for f in forecast_list:
            if "午前" in f["time"] or "午後" in f["time"]:
                target_forecast = f
                break

        time_label = target_forecast["time"]
        icon_id = target_forecast["icon_id"]

        if icon_id == "01":
            if 6 <= current_month <= 9:
                comment = f"{time_label}は晴れだワン…でも夏のアスファルトはアチアチだワン！散歩は控えるワン。"
            else:
                comment = f"{time_label}はお散歩日和だワン！日差しが気持ちいいワン！"

        elif icon_id in ["02", "03", "04", "50"]:
            if 6 <= current_month <= 9:
                comment = f"{time_label}は曇りだワン。夏はこれくらいが散歩しやすいワン！"
            else:
                comment = f"{time_label}は雲が出るワン。過ごしやすいワン。"

        elif icon_id in ["09", "10", "11"]:
            comment = f"{time_label}は雨っぽいワン。散歩は中止か短めだワン。"

        elif icon_id == "13":
            comment = f"{time_label}は雪だワン！肉球が冷たくて震えるワン！"

        else:
            comment = f"{time_label}も元気に過ごすワン！"

    try:
        d_res = requests.get(DOG_URL, timeout=REQUEST_TIMEOUT)
        d_res.raise_for_status()
        d_data = d_res.json()
        dog_img = d_data['message']
        breed_raw = dog_img.split('/')[-2]
        breed_name = breed_raw.replace('-', ' ').title()
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Dog API request failed: {e}")
        dog_img = ""
        breed_name = "Unknown Dog"

    return render_template(
        'index.html',
        weather_data=all_weather,
        dog_url=dog_img,
        breed_name=breed_name,
        dog_comment=comment
    )


if __name__ == "__main__":
    app.run(debug=True)