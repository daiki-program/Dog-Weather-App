# 🐶 ワンコ天気予報 (Doggy Weather App)

「明日、散歩に行けるかな？」がひと目でわかる、愛犬家のための天気予報Webアプリです。
天気データと犬の画像を組み合わせ、季節に応じた愛犬視点のアドバイスを提供します。

## 🌐 ライブデモ
**[https://dog-weather-app.onrender.com/](https://dog-weather-app.onrender.com/)**
> ※無料プランを使用しているため、最初のアクセス時にアプリの起動で30秒〜1分ほど時間がかかる場合があります。

## 🌟 主な機能
- **リアルタイム天気予報**: 23区・多摩地区の天気を表示。
- **動的コメントシステム**: 天気・気温・季節を考慮した独自のアドバイスを表示。
- **癒やしの画像**: Dog APIと連携し、リロードのたびに異なる犬種を表示。

## 🛠 技術スタック
- **Backend**: Python 3.12 / Flask
- **Frontend**: HTML / CSS / JavaScript
- **Deployment**: Render (Auto-deploy)
- **APIs**: OpenWeatherMap API, Dog API

## 💡 技術的な工夫
1. **実用的なロジック**: 犬の飼育における「夏のアスファルト熱」などの知見を反映。
2. **エラーハンドリング**: APIのタイムアウト設定や例外処理を実装。

---

## 🚀 使い方（ローカル実行）

本アプリの動作には [OpenWeatherMap](https://home.openweathermap.org/users/sign_up) の無料APIキーが必要です。キーを取得後、以下の手順で実行してください。


### 1. リポジトリをクローン（ターミナルで操作）
デスクトップなどでターミナルを開き、以下のコマンドを打ちます。


```bash
git clone https://github.com/あなたのユーザー名/リポジトリ名.git
```

### 2. 必要なライブラリをインストール（ターミナルで操作）

```bash
pip install -r requirements.txt
```

### 3. `.env`ファイルを作成してAPIキーを設定

プロジェクトのルートディレクトリに`.env` ファイルを作成し、以下を記述してください。

```
OPENWEATHER_API_KEY=あなたのキー
```

### 4. アプリケーションを起動（ターミナルで操作）

```bash
python dogWeather.py
```

### 5. URLにアクセス
起動後、ブラウザで以下のURLにアクセスしてください。

[http://127.0.0.1:5000](http://127.0.0.1:5000)
