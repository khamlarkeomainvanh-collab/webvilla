// static/sw.js
self.addEventListener('push', function(event) {
    const data = event.data.json();
    const options = {
        body: data.body,
        icon: '/static/img/logo.png', // ຮູບ Icon ຮ້ານ
        badge: '/static/img/badge.png',
        vibrate: [200, 100, 200], // ສັ່ນ (ສຳລັບມືຖື)
        silent: false, // ປິດໂໝດງຽບ
        data: { url: data.url }
    };

    event.waitUntil(
        self.registration.showNotification(data.title, options)
    );
});

// ເມື່ອກົດແຈ້ງເຕືອນໃຫ້ເປີດໜ້າເວັບ
self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    event.waitUntil(
        clients.openWindow(event.notification.data.url)
    );
});
