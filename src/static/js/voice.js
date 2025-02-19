document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const methodBtns = document.querySelectorAll('.method-btn');
    const inputSections = document.querySelectorAll('.input-section');
    const recordButton = document.getElementById('recordButton');
    const timer = document.getElementById('timer');
    const audioPreview = document.getElementById('audioPreview');
    const audioFilename = document.getElementById('audioFilename');
    const emergencyForm = document.getElementById('emergencyForm');

    // Recording state variables
    let mediaRecorder;
    let audioChunks = [];
    let startTime;
    let timerInterval;
    let isRecording = false;
    let stream;

    // Method switching (Text/Voice toggle)
    methodBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            methodBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            inputSections.forEach(section => {
                section.classList.remove('active');
            });

            const method = btn.dataset.method;
            document.getElementById(method + 'Input').classList.add('active');
        });
    });

    // Timer update function
    function updateTimer() {
        const elapsed = new Date() - startTime;
        const seconds = Math.floor(elapsed / 1000);
        const minutes = Math.floor(seconds / 60);
        const formattedTime =
            `${minutes.toString().padStart(2, '0')}:${(seconds % 60).toString().padStart(2, '0')}`;
        timer.textContent = formattedTime;
    }

    // Show notification function
    function showNotification(options = {}) {
        const {
            title = 'Emergency Response',
            message = 'Help is on the way.',
            type = 'success',
            duration = 2000000
        } = options;

        // Create notification container if it doesn't exist
        let notificationContainer = document.querySelector('.notification-container');
        if (!notificationContainer) {
            notificationContainer = document.createElement('div');
            notificationContainer.className = 'notification-container';
            document.body.appendChild(notificationContainer);
        }

        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification-window ${type}`;
        notification.innerHTML = `
            <div class="notification-header">
                <h3>${title}</h3>
                <button class="notification-close">&times;</button>
            </div>
            <div class="notification-body">
                <p>${message}</p>
            </div>
            <div class="notification-progress"></div>
        `;

        // Add to container
        notificationContainer.appendChild(notification);

        // Add close button functionality
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.onclick = () => notification.remove();

        // Auto remove after duration

    }

    // Stop recording function
    async function stopRecording() {
        if (mediaRecorder && isRecording) {
            mediaRecorder.stop();
            clearInterval(timerInterval);
            isRecording = false;
            recordButton.classList.remove('recording');
            recordButton.innerHTML = '<i class="fas fa-microphone"></i> Start Recording';

            // Stop all tracks in the stream
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
            }
        }
    }

    // Upload audio with form data function
    async function uploadAudioWithFormData(audioBlob) {
    const formData = new FormData();

    // Add the audio file
    formData.append('audio', audioBlob, 'emergency_recording.wav');

    // Add form fields
    formData.append('name', document.getElementById('name').value || 'Anonymous');
    formData.append('contact', document.getElementById('contact').value || 'Not provided');
    formData.append('latitude', document.getElementById('latitude').value || '');
    formData.append('longitude', document.getElementById('longitude').value || '');
    formData.append('description', document.getElementById('description').value || '');

    // Get selected language or default to Greek
    const language = document.getElementById('language')?.value || 'el-GR';
    formData.append('language', language);

    try {
        showNotification({
            title: 'Processing',
            message: 'Transcribing audio...',
            type: 'info',
            duration: 5000
        });

        const response = await fetch('/upload-audio', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        audioFilename.value = data.filename;

        // Update description field with transcription if available
        if (data.transcription) {
            const descriptionField = document.getElementById('description');
            if (descriptionField) {
                const transcriptionText = `
Service Used: ${data.transcription.service}
Language: ${data.transcription.detected_language}
Transcribed Text:
${data.transcription.text}`;

                descriptionField.value = transcriptionText;
            }
        }

        showNotification({
            title: 'Emergency Report Created',
            message: `${data.message}`,
            type: 'success',
            duration: 2000000
        });

        // Don't clear the form immediately so user can see the transcription
        if (!data.transcription) {
            if (emergencyForm) {
                emergencyForm.reset();
            }
        }

        // Hide audio preview
        if (audioPreview) {
            audioPreview.style.display = 'none';
        }

    } catch (error) {
        console.error('Error uploading audio:', error);
        showNotification({
            title: 'Error',
            message: 'Failed to submit emergency report. Please try again.',
            type: 'error',
            duration: 10000
        });
    }
}

    // Record button click handler
    if (recordButton) {
        recordButton.addEventListener('click', async () => {
            if (!isRecording) {
                try {
                    // Request microphone access
                    stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                    mediaRecorder = new MediaRecorder(stream);
                    audioChunks = [];

                    // Handle data available event
                    mediaRecorder.ondataavailable = (event) => {
                        audioChunks.push(event.data);
                    };

                    // Handle recording stop event
                    mediaRecorder.onstop = async () => {
                        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                        const audioUrl = URL.createObjectURL(audioBlob);
                        audioPreview.src = audioUrl;
                        audioPreview.style.display = 'block';

                        // Upload audio with form data
                        await uploadAudioWithFormData(audioBlob);
                    };

                    // Start recording
                    mediaRecorder.start();
                    startTime = new Date();
                    timerInterval = setInterval(updateTimer, 1000);
                    isRecording = true;
                    recordButton.classList.add('recording');
                    recordButton.innerHTML = '<i class="fas fa-stop"></i> Stop Recording';

                    // Auto-stop recording after 3 minutes
                    setTimeout(() => {
                        if (isRecording) {
                            stopRecording();
                        }
                    }, 180000); // 3 minutes in milliseconds

                } catch (error) {
                    console.error('Error accessing microphone:', error);
                    showNotification({
                        title: 'Microphone Error',
                        message: 'Could not access microphone. Please ensure you have given permission.',
                        type: 'error',
                        duration: 10000
                    });
                }
            } else {
                await stopRecording();
            }
        });
    }

    // Handle form submission (now optional as audio upload automatically creates report)
    if (emergencyForm) {
        emergencyForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            if (isRecording) {
                await stopRecording();
            }

            // Only proceed if there's a text description (audio reports handled separately)
            if (document.getElementById('description').value) {
                const formData = new FormData(emergencyForm);

                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    });
                    const data = await response.json();
                    console.log(data);
                    if (response.ok) {
                        showNotification({
                            title: 'Emergency Report Created',
                            message: data.message,
                            type: 'success'
                        });
                        emergencyForm.reset();
                        if (audioPreview) {
                            audioPreview.style.display = 'none';
                        }
                    } else {
                        throw new Error('Failed to submit emergency report');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    showNotification({
                        title: 'Error',
                        message: 'Failed to submit emergency report. Please try again.',
                        type: 'error'
                    });
                }
            }
        });
    }

    // Cleanup on page unload
    window.addEventListener('beforeunload', () => {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
    });

    // Handle visibility change (e.g., when user switches tabs)
    document.addEventListener('visibilitychange', () => {
        if (document.hidden && isRecording) {
            stopRecording();
        }
    });
});