document.addEventListener('DOMContentLoaded', () => {
    const updateBtn = document.getElementById('update-btn');
    
    // 音声ファイルの読み込み（staticフォルダ内）
    const barkSound = new Audio('/static/bark.mp3');

    if (updateBtn) {
        updateBtn.addEventListener('click', () => {
            // 1. 音を鳴らす
            barkSound.play();

            // 2. ローディング演出
            updateBtn.style.opacity = '0.5';
            updateBtn.innerText = '更新中...';
            
            // 3. 少しだけ時間を置いてからリロード（音が鳴り終わるのを待つため）
            setTimeout(() => {
                window.location.reload();
            }, 20); // 0.02秒後にリロード
        });
    }
});