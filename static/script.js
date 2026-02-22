document.addEventListener('DOMContentLoaded', () => {
    const updateBtn = document.getElementById('update-btn');
    
    // idで要素をしっかり特定する
    const dogImg = document.getElementById('dog-img');
    const breedText = document.getElementById('breed-name');
    
    const barkSound = new Audio('/static/bark.mp3');

    async function fetchDogImage() {
        try {
            const response = await fetch('https://dog.ceo/api/breeds/image/random');
            const data = await response.json();
            
            // 画像のURLをセット
            if (dogImg) {
                dogImg.src = data.message;
            }
            
            // 犬種名をセット
            if (breedText) {
                const urlParts = data.message.split('/');
                const breedRaw = urlParts[4]; // URLの5番目が犬種名
                breedText.innerText = '🐶 ' + breedRaw.replace('-', ' ').toUpperCase();
            }
        } catch (error) {
            console.error("取得失敗:", error);
            if (breedText) breedText.innerText = "ワンコが迷子だワン...";
        }
    }

    // ページを開いた瞬間に一回実行
    fetchDogImage();

    if (updateBtn) {
        updateBtn.addEventListener('click', () => {
            barkSound.play();
            // 画像だけ更新
            fetchDogImage();
        });
    }
});