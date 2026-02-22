document.addEventListener('DOMContentLoaded', () => {
    const dogImage = document.getElementById('dog-image'); // IDを合わせる
    const breedLabel = document.getElementById('dog-breed-label'); // IDを合わせる
    const updateBtn = document.getElementById('update-btn');
    const barkSound = new Audio('/static/bark.mp3');

    // --- 犬の画像をフェッチする関数 ---
    async function fetchDog() {
        try {
            const response = await fetch('https://dog.ceo/api/breeds/image/random');
            const data = await response.json();
            
            if (dogImage) {
                dogImage.src = data.message;
                // URLから犬種を抜き出し（例: /breeds/shiba/n02106734_3427.jpg）
                const breed = data.message.split('/')[4].replace('-', ' ');
                if (breedLabel) breedLabel.innerText = breed.toUpperCase();
            }
        } catch (e) {
            console.error("画像取得失敗", e);
            if (breedLabel) breedLabel.innerText = "ワンちゃんが来ませんでした…";
        }
    }

    // 初回読み込み時に実行
    fetchDog();

    // --- 更新ボタン & 音声再生 ---
    if (updateBtn) {
        updateBtn.addEventListener('click', () => {
            updateBtn.style.opacity = '0.5';
            updateBtn.innerText = '更新中...';

            const reloadPage = () => window.location.reload();

            // 音声が終わったらリロード
            barkSound.addEventListener('ended', reloadPage, { once: true });

            barkSound.play().catch(err => {
                console.log("音声再生がブロックされました:", err);
                reloadPage(); // 再生できなくてもリロードはする
            });

            // 念のため2秒後に強制リロード
            setTimeout(reloadPage, 2000);
        });
    }
});