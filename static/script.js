document.addEventListener('DOMContentLoaded', function () {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');

    // Define the dictionary mapping emotions to emoji image paths
    const emojiDict = {
        "angry": "static/emojis/angry.png",
        "fear": "static/emojis/fear.png",
        "neutral": "static/emojis/neutral.png",
        "sad": "static/emojis/sad.png",
        "disgust": "static/emojis/disgust.png",
        "happy": "static/emojis/happy.png",
        "surprise": "static/emojis/surprised.png"
    };

    // Get the webcam feed from the browser
    async function setupCamera() {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    }

    async function detectEmotion() {
        setInterval(async () => {
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            const imgData = canvas.toDataURL('image/jpeg');
    
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    body: JSON.stringify({ imgData }),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
    
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
    
                const data = await response.json();
                const dominant_emotion = data[0]['dominant_emotion'];
                const emotionLabel = document.getElementById('emotionLabel');
                const emojiImg = document.getElementById('emojiImg');
    
                // Set the text content of the emotion label
                emotionLabel.textContent = 'Emotion: ' + dominant_emotion;
    
                // Set the source of the emoji image based on the dominant emotion
                if (emojiDict.hasOwnProperty(dominant_emotion)) {
                    emojiImg.src = emojiDict[dominant_emotion];
                } else {
                    emojiImg.src = ''; // Clear the image source if emotion is not found in the dictionary
                }
                // Show the emojiImg
                emojiImg.style.display = 'inline-block';
            } catch (error) {
                console.error('Error:', error);
            }
        }, 5000); // Adjusted interval for capturing webcam img to be analyzed - 5 seconds
    }

    setupCamera();
    setTimeout(detectEmotion, 5000);
});
