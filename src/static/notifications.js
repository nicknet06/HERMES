class NotificationManager {
    constructor() {
        this.hasPermission = false;
        this.initialize();
        // Add resize listener to update notification width
        window.addEventListener('resize', () => {
            const container = document.querySelector('.notification-container');
            if (container) {
                this.updateNotificationWidth(container);
            }
        });
    }

    updateNotificationWidth(container) {
        const browserWidth = window.innerWidth;
        const targetWidth = 740 * (3840 / browserWidth);
        container.style.width = `${targetWidth}px`;
    }

    showInAppNotification(title, message, duration) {
        // Remove any existing notifications
        const existingNotification = document.querySelector('.notification-container');
        if (existingNotification) {
            existingNotification.remove();
        }

        const notificationContainer = document.createElement('div');
        notificationContainer.className = 'notification-container';

        // Set initial width
        this.updateNotificationWidth(notificationContainer);

        const notification = document.createElement('div');
        notification.className = 'notification-window';
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

        notificationContainer.appendChild(notification);

        // Insert after the chat-box
        const chatBox = document.querySelector('.chat-box');
        chatBox.insertAdjacentElement('afterend', notificationContainer);

        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.onclick = () => {
            notification.classList.add('fade-out');
            setTimeout(() => notificationContainer.remove(), 500);
        };

        const progressBar = notification.querySelector('.notification-progress');
        progressBar.style.animation = `progress ${duration/1000}s linear forwards`;

        setTimeout(() => {
            if (notification.parentNode) {
                notification.classList.add('fade-out');
                setTimeout(() => notificationContainer.remove(), 500);
            }
        }, duration);
    }

    // Rest of your NotificationManager class remains the same
}

// Initialize notification manager
const notificationManager = new NotificationManager();