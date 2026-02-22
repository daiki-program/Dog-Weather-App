import os
import requests
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

app = Flask(__name__)

# --- 設定値 ---
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
DOG_URL = "https://dog.ceo/api/breeds/image/random"
TARGET_HOURS = [9, 15]
REQUEST_TIMEOUT = 5

CITIES = {
    "23区": "Chiyoda",
    "多摩地区": "Hachioji"
}

# --- ヘルパー関数：常に日本時間を取得 ---
def get_now_tokyo():
    """OSの環境に依存せず、常に日本標準時(JST)の現在時刻を返す"""
    #
    return datetime.now(timezone(timedelta(hours=9), 'JST'))

def format_datetime(dt_txt):
    """APIの時刻文字列を『今日・明日・明後日』形式に変換"""
    dt = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")
    
    # 比較用にタイムゾーン情報を持たない日本時間を取得
    now = get_now_tokyo().replace(tzinfo=None) 
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
    # 日本時間の「今」を基準にする
    now = get_now_tokyo().replace(tzinfo=None)
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ja"
    }

    try:
        res = requests.get(FORECAST_URL, params=params, timeout=REQUEST_TIMEOUT)
        res.raise_for_status()
        response = res.json()

        results = []
        if "list" in response:
            for item in response["list"]:
                dt = datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S")
                # 過去の予報はスキップし、特定の時間帯(9, 15時)のみ抽出
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
    current_month = get_now_tokyo().month # ここも日本時間で判定

    # 代表として「23区」の最初の予報を元にコメントを生成
    if "23区" in all_weather and len(all_weather["23区"]) > 0:
        target_forecast = all_weather["23区"][0]
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

    # 犬画像の取得
    try:
        d_res = requests.get(DOG_URL, timeout=REQUEST_TIMEOUT)
        d_res.raise_for_status()
        d_data = d_res.json()
        dog_img = d_data['message']
        breed_raw = dog_img.split('/')[-2]
        breed_name = breed_raw.replace('-', ' ').title()
    except requests.exceptions.RequestException:
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