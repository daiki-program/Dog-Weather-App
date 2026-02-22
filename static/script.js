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
                // URLから犬種を抜き出し
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
        // ボタンを無効化して連打を防ぐ
        updateBtn.disabled = true;
        updateBtn.style.opacity = '0.5';
        updateBtn.innerText = 'サーバー起動中...';

        barkSound.play().catch(e => console.log("音は出せなかったけど進むワン"));

        // 2. 「音が終わるのを待たず」に、5秒〜10秒後くらいにリロードさせる
        setTimeout(() => {
            window.location.reload();
        }, 10000); 
    });
}