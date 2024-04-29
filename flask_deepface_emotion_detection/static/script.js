document.addEventListener('DOMContentLoaded', function () {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');

    async function setupCamera() {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    }

    async function detectEmotion() {
        setInterval(async () => {
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            const imgData = canvas.toDataURL('image/jpeg');

            await fetch('/analyze', {
                method: 'POST',
                body: JSON.stringify({ imgData: imgData }),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                const dominant_emotion = data[0]['dominant_emotion']; // Assuming result is a list
                const emotionLabel = document.getElementById('emotionLabel');
                emotionLabel.textContent = 'Emotion: ' + dominant_emotion;
            })
            .catch(error => console.error('Error:', error));
        }, 3000); // Adjusted interval for testing
    }

    setupCamera();
    detectEmotion();
});
