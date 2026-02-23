# 🐶 ワンコ天気予報 (Doggy Weather App)

「明日、散歩に行けるかな？」がひと目でわかる、愛犬家のための天気予報Webアプリです。
天気データと犬の画像を組み合わせ、季節に応じた愛犬視点のアドバイスを提供します。

## 🌐 【本番環境】
**[https://dog-weather-app.onrender.com/](https://dog-weather-app.onrender.com/)**

**👆RenderのStarterプランを利用し、常時稼働させています。**

## 📂 ディレクトリ構成
```text
.
├── dogWeather.py       # Flaskメインロジック
├── requirements.txt    # 依存ライブラリ
├── runtime.txt         # Pythonのバージョン指定
├── render.yaml         # Renderデプロイ用設定
├── .env                # 環境変数（Git管理外）
├── .gitignore          #
├── README.md           # 
├── static/             # 
│   ├── style.css       #
│   ├── script.js       #
│   ├── favicon.png     #
│   └── bark.mp3        # ワンコの鳴き声
└── templates/          # 
    └── index.html      # 
```

## 🌟 主な機能
- リアルタイム予報の高速表示: 23区・多摩地区の特定の時間帯（9時・15時）に絞った実用的な予報。
- サーバーサイド・キャッシュ: 天気データを10分間保持することで、API制限の回避と高速なレスポンスを実現。
- 非同期画像読み込み: JavaScript Fetch APIにより、ページ全体のロードを待たずに犬の画像をスムーズに表示。
- 愛犬家向けロジック: 夏の肉球火傷注意喚起など、実際の飼育に役立つコメントシステム。
- 音声エフェクト: 更新ボタンを押すとワンコが鳴いてお知らせ。

## 🛠 技術スタック
- **Backend**: Python 3.12 / Flask
- **Frontend**: HTML / CSS / JavaScript
- **Deployment**: Render (Auto-deploy)
- **APIs**: OpenWeatherMap API, Dog API

## 💡 技術的な工夫
1. **パフォーマンス最適化 (Caching)**: Python側で独自にキャッシュロジックを実装。10分以内の連続アクセス時はAPIリクエストをスキップし、システム全体の負荷と待ち時間を大幅に削減しました。
2. **フロントエンドとバックエンドの分離**: 重くなりがちな画像取得処理をJavaScriptに移譲。サーバー側の処理（天気計算）とブラウザ側の処理（画像描画）を分けることで、ユーザー体験を向上させています。
3. **レスポンシブデザイン**: スマホ画面でも使いやすいレイアウトを維持します。

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

---
Developed by D. S.
