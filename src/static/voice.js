document.addEventListener('DOMContentLoaded', function() {
    const methodBtns = document.querySelectorAll('.method-btn');
    const inputSections = document.querySelectorAll('.input-section');
    const recordButton = document.getElementById('recordButton');
    const timer = document.getElementById('timer');
    const audioPreview = document.getElementById('audioPreview');
    const audioFilename = document.getElementById('audioFilename');
    const submitBtn = document.getElementById('submitBtn');
    const emergencyForm = document.getElementById('emergencyForm');

    let mediaRecorder;
    let audioChunks = [];
    let startTime;
    let timerInterval;
    let isRecording = false;
    let stream;

    // Method switching
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
    function showNotification() {
        // Create notification container if it doesn't exist
        let notificationContainer = document.querySelector('.notification-container');
        if (!notificationContainer) {
            notificationContainer = document.createElement('div');
            notificationContainer.className = 'notification-container';
            document.body.appendChild(notificationContainer);
        }

        // Create notification element
        const notification = document.createElement('div');
        notification.className = 'notification-window';
        notification.innerHTML = `
            <div class="notification-header">
                <h3>Emergency Response Dispatched</h3>
                <button class="notification-close">&times;</button>
            </div>
            <div class="notification-body">
                <p>Help is on the way. Estimated arrival time: 20 minutes.</p>
            </div>
            <div class="notification-progress"></div>
        `;

        // Add to container
        notificationContainer.appendChild(notification);

        // Add close button functionality
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.onclick = () => notification.remove();

        // Auto remove after 20 seconds
        setTimeout(() => {
            notification.classList.add('fade-out');
            setTimeout(() => notification.remove(), 500);
        }, 20000);
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

    // Record button click handler
    if (recordButton) {
        recordButton.addEventListener('click', async () => {
            if (!isRecording) {
                try {
                    stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                    mediaRecorder = new MediaRecorder(stream);
                    audioChunks = [];

                    mediaRecorder.ondataavailable = (event) => {
                        audioChunks.push(event.data);
                    };

                    mediaRecorder.onstop = async () => {
                        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                        const audioUrl = URL.createObjectURL(audioBlob);
                        audioPreview.src = audioUrl;
                        audioPreview.style.display = 'block';

                        // Upload the audio file
                        const formData = new FormData();
                        formData.append('audio', audioBlob, 'emergency_recording.wav');

                        try {
                            const response = await fetch('/upload-audio', {
                                method: 'POST',
                                body: formData
                            });

                            if (!response.ok) {
                                throw new Error('Network response was not ok');
                            }

                            const data = await response.json();
                            audioFilename.value = data.filename;
                            submitBtn.disabled = false;
                            showNotification();
                        } catch (error) {
                            console.error('Error uploading audio:', error);
                            alert('Error uploading audio. Please try again.');
                        }
                    };

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
                    alert('Could not access microphone. Please ensure you have given permission.');
                }
            } else {
                await stopRecording();
            }
        });
    }

    // Handle form submission
    if (emergencyForm) {
        emergencyForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            if (isRecording) {
                await stopRecording();
            }

            // Get form data
            const formData = new FormData(emergencyForm);

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                if (response.ok) {
                    showNotification();
                    emergencyForm.reset();
                    if (audioPreview) {
                        audioPreview.style.display = 'none';
                    }
                } else {
                    throw new Error('Failed to submit emergency report');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error submitting emergency report. Please try again.');
            }
        });
    }

    // Cleanup on page unload
    window.addEventListener('beforeunload', () => {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
    });

    // Handle visibility change
    document.addEventListener('visibilitychange', () => {
        if (document.hidden && isRecording) {
            stopRecording();
        }
    });
});