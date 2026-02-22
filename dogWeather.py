import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv  # .envを読み込むためのライブラリ
from flask import Flask, render_template, request

# .envファイルから環境変数を読み込む
load_dotenv()

# APIキーを環境変数から取得
API_KEY = os.getenv("OPENWEATHER_API_KEY")

app = Flask(__name__) 

CITIES = {
    "23区": "Chiyoda",
    "多摩地区": "Hachioji"
}
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
DOG_URL = "https://dog.ceo/api/breeds/image/random"

# --- キャッシュ管理用 ---
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
    
    # 1. キャッシュチェック (前回取得から1時間以内ならAPIを叩かない)
    if last_update_time and (now - last_update_time) < timedelta(hours=1):
        if city_name in weather_cache:
            print(f"[{city_name}] キャッシュを使用します")
            return weather_cache[city_name]

    # 2. キャッシュがない、または1時間以上経過した場合はAPI取得
    print(f"[{city_name}] APIから最新情報を取得します...")
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
                # 未来のデータ、かつ9時or15時のみ
                if dt > now and dt.hour in [9, 15]:
                    results.append({
                        "time": format_datetime(item["dt_txt"]),
                        "desc": get_weather_emoji(item["weather"][0]["icon"]),
                        "temp": round(item["main"]["temp"])
                    })
                if len(results) >= 4:
                    break
        
        # 取得したデータを保存
        weather_cache[city_name] = results
        # 最終更新として記録
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
    
    # --- セリフ決定ロジック ---
    comment = "今日も一日頑張るワン！"# デフォルトのコメント
    
    if "23区" in all_weather and len(all_weather["23区"]) > 0:
        target_forecast = all_weather["23区"][0]
        weather_icon = target_forecast["desc"]
        time_label = target_forecast["time"]
        
        if weather_icon == "☀️":
            comment = f"{time_label}はお散歩日和だワン！"
        elif weather_icon in ["☁️", "🌤️", "🌫️"]:
            comment = f"{time_label}は雲がでるワン"
        elif weather_icon in ["🌧️", "☔️"]:
            comment = f"{time_label}は雨っぽいワン。散歩は短めだワン。"
        elif weather_icon == "⛄️":
            comment = f"{time_label}は雪だワン！肉球が冷たいワン！"
        elif weather_icon == "⛈️":
            comment = f"{time_label}はカミナリは怖いワン..."

    # --- 犬画像取得 (こちらはリロードのたびに新しくする) ---
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