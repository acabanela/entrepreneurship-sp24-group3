document.addEventListener('DOMContentLoaded', async function () {
    const video = document.getElementById('video');
    const submitButton = document.getElementById('submitButton');
    const nextButton = document.getElementById('nextButton'); // New: Get the "Next Scenario" button
    const emotionLabel = document.getElementById('emotionLabel');
    const emojiImg = document.getElementById('emojiImg');
    const capturedCanvas = document.getElementById('capturedCanvas');
    const ctx = capturedCanvas.getContext('2d');
    const scenarioText = document.getElementById('scenarioText');
    const messageDiv = document.getElementById('messageDiv'); // Get reference to the messageDiv

    let scenarioIndex = 0;

    const response = await fetch('static/scenarios.json');
    const scenarios = await response.json();

    const emojiDict = {
        "angry": "static/emojis/angry.png",
        "fear": "static/emojis/fear.png",
        "neutral": "static/emojis/neutral.png",
        "sad": "static/emojis/sad.png",
        "disgust": "static/emojis/disgust.png",
        "happy": "static/emojis/happy.png",
        "surprise": "static/emojis/surprised.png"
    };

    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        video.onloadedmetadata = () => {
            video.play();
        };
    } catch (error) {
        console.error('Error accessing webcam:', error);
    }

    function loadScenarioText() {
        scenarioText.textContent = scenarios[scenarioIndex]['Story'];
        scenarioName.textContent = scenarios[scenarioIndex]['Scenario Name'];
    }

    loadScenarioText();

    submitButton.addEventListener('click', async function () {
        if (submitButton.textContent === 'Submit') {
            video.style.display = 'none';
            capturedCanvas.style.display = 'block';
            emotionLabel.style.display = 'block';
            emojiImg.style.display = 'block';

            capturedCanvas.width = video.videoWidth;
            capturedCanvas.height = video.videoHeight;
            ctx.drawImage(video, 0, 0, capturedCanvas.width, capturedCanvas.height);

            const imgData = capturedCanvas.toDataURL('image/jpeg');

            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    body: JSON.stringify({ imgData }),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                if (!response.ok) {
                    throw new Error('Failed to analyze image');
                }

                const data = await response.json();

                const dominant_emotion = data[0]['dominant_emotion'];
                emotionLabel.textContent = 'Detected Emotion: ' + dominant_emotion;

                if (emojiDict.hasOwnProperty(dominant_emotion)) {
                    emojiImg.src = emojiDict[dominant_emotion];
                } else {
                    emojiImg.src = '';
                }

                // Check if the dominant emotion matches the scenario emotion
                const scenarioEmotion = scenarios[scenarioIndex]['Emotion'];
                if (dominant_emotion === scenarioEmotion) {
                    messageDiv.textContent = 'Correct!';
                    messageDiv.className = 'message-correct'; // Add correct message class
                } else {
                    messageDiv.textContent = 'Nope, incorrect!';
                    messageDiv.className = 'message-incorrect'; // Add incorrect message class
                }

                submitButton.textContent = 'Try Again';
                submitButton.disabled = false;
            } catch (error) {
                console.error('Error analyzing image:', error);
            }
        } else if (submitButton.textContent === 'Try Again') {
            video.style.display = 'block';
            capturedCanvas.style.display = 'none';
            emotionLabel.style.display = 'none';
            emojiImg.style.display = 'none';

            submitButton.textContent = 'Submit';
            messageDiv.textContent = '';
            messageDiv.className = ''; // Remove message class
        }
    });

    // Event listener for the "Next Scenario" button
    nextButton.addEventListener('click', function () {
        // Increment scenarioIndex to load the next scenario text
        scenarioIndex = (scenarioIndex + 1) % scenarios.length;
        loadScenarioText();
        // await resetWebcam(); // Call resetWebcam() here to reset the webcam feed
        // Show webcam feed
        submitButton.textContent = 'Submit';
        video.style.display = 'block';
        capturedCanvas.style.display = 'none';
        emotionLabel.style.display = 'none';
        emojiImg.style.display = 'none';
        // Hide the still capture canvas
        capturedCanvas.style.display = 'none';
        messageDiv.textContent = '';
        messageDiv.className = ''; // Remove message class
    });
});
