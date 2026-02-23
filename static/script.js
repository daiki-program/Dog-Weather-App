document.addEventListener('DOMContentLoaded', () => {
    const dogImage = document.getElementById('dog-image');
    const breedLabel = document.getElementById('dog-breed-label');
    const updateBtn = document.getElementById('update-btn');
    const loadingText = document.getElementById('loading-text');
    const barkSound = new Audio('static/bark.mp3');

    async function fetchDog() {
        try {
            const response = await fetch('https://dog.ceo/api/breeds/image/random');
            const data = await response.json();
            
            if (dogImage && data.status === "success") {
                const imageUrl = data.message;
                // 画像から犬種名を抽出（まだ画面には出さない）
                const breedName = imageUrl.split('/')[4].replace('-', ' ').toUpperCase();

                // 画像が完全に読み込まれたら「名前」と「写真」を同時に出す
                dogImage.onload = () => {
                    // 1. Loadingテキストを消す
                    if (loadingText) loadingText.style.display = 'none';
                    
                    // 2. 犬種名を書き換える（Loading...から実際の名前へ）
                    if (breedLabel) breedLabel.innerText = "🐶 " + breedName;
                    
                    // 3. 画像を表示する
                    dogImage.style.display = 'block';
                };

                // 画像のダウンロードを開始
                dogImage.src = imageUrl;
            }
        } catch (e) {
            if (loadingText) loadingText.innerText = "ワンコはお休み中です💤";
            if (breedLabel) breedLabel.innerText = "🐶 通信エラー";
            console.error("画像取得失敗", e);
        }
    }

    // 初回実行（ページを開いた時）
    fetchDog();

    if (updateBtn) {
        updateBtn.addEventListener('click', () => {
            // ボタンを無効化して「更新中」の見た目にする
            updateBtn.disabled = true;
            updateBtn.style.opacity = '0.5';
            updateBtn.innerText = '更新中...';

            // ワン！と鳴らす
            barkSound.play().catch(e => console.log("音声再生失敗"));

            // 1秒後にページをリロードして天気を最新にする
            setTimeout(() => {
                window.location.reload();
            }, 1000); 
        });
    }
});