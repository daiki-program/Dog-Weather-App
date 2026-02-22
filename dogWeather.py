import os
import time
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request

# --- タイムゾーンの設定 ---
os.environ['TZ'] = 'Asia/Tokyo'
try:
    time.tzset()
except AttributeError:
    pass

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

app = Flask(__name__) 

CITIES = {
    "23区": "Chiyoda",
    "多摩地区": "Hachioji"
}
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
DOG_URL = "https://dog.ceo/api/breeds/image/random"

weather_cache = {}
last_update_time = None

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

def get_weather_emoji(icon_code):
    emoji_map = {
        "01": "☀️", "02": "🌤️", "03": "☁️", "04": "☁️",
        "09": "🌧️", "10": "☔️", "11": "⛈️", "13": "⛄️", "50": "🌫️"
    }
    return emoji_map.get(icon_code[:2], "🌈")

def get_target_forecast(city_name):
    global last_update_time, weather_cache
    now = datetime.now()
    
    if last_update_time and (now - last_update_time) < timedelta(hours=1):
        if city_name in weather_cache:
            return weather_cache[city_name]

    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ja"
    }
    
    try:
        response = requests.get(FORECAST_URL, params=params).json()
        results = []
        if "list" in response:
            for item in response["list"]:
                dt = datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S")
                # 未来のデータかつ、散歩の目安になる9時・15時のみを抽出
                if dt > now and dt.hour in [9, 15]:
                    results.append({
                        "time": format_datetime(item["dt_txt"]),
                        "desc": get_weather_emoji(item["weather"][0]["icon"]),
                        "temp": round(item["main"]["temp"])
                    })
                # 深夜でも翌々日までカバーできるよう少し多めに取得（最大6個）
                if len(results) >= 6:
                    break
        
        weather_cache[city_name] = results
        last_update_time = now
        return results
    except Exception as e:
        print(f"Error: {e}")
        return []

@app.route('/')
def home():
    all_weather = {}
    for display_name, city_name in CITIES.items():
        all_weather[display_name] = get_target_forecast(city_name)
    
    # --- セリフ決定ロジック（堅牢版） ---
    comment = "今日も一日頑張るワン！"

    if "23区" in all_weather and len(all_weather["23区"]) > 0:
        forecast_list = all_weather["23区"]
        
        # デフォルトはリストの先頭（一番近い未来）
        target_forecast = forecast_list[0]

        # リストを順に見て、最初に見つかった「午前」または「午後」の予報をターゲットにする
        # これにより、15時を過ぎて「今日の午後」がAPIから消えれば自動で「明日の午前」が選ばれる
        for f in forecast_list:
            if "午前" in f["time"] or "午後" in f["time"]:
                target_forecast = f
                break

        time_label = target_forecast["time"]
        weather_icon = target_forecast["desc"]
        
        comment_map = {
            "☀️": f"{time_label}はお散歩日和だワン！",
            "🌧️": f"{time_label}は雨っぽいワン。散歩は短めだワン。",
            "☔️": f"{time_label}は雨っぽいワン。散歩は短めだワン。",
            "☁️": f"{time_label}は雲がでるワン",
            "🌤️": f"{time_label}は雲がでるワン",
            "🌫️": f"{time_label}は雲がでるワン",
            "⛄️": f"{time_label}は雪だワン！肉球が冷たいワン！",
            "⛈️": f"{time_label}はカミナリは怖いワン..."
        }
        comment = comment_map.get(weather_icon, f"{time_label}も元気に過ごすワン！")

    # --- 犬画像取得 ---
    try:
        d_data = requests.get(DOG_URL).json()
        dog_img = d_data['message']
        breed_raw = dog_img.split('/')[-2]
        breed_name = breed_raw.replace('-', ' ').title()
    except:
        dog_img = ""; breed_name = "Unknown Dog"
    
    return render_template(
        'index.html',
        weather_data=all_weather,
        dog_url=dog_img,
        breed_name=breed_name,
        dog_comment=comment
    )

if __name__ == "__main__":
    app.run(debug=True)