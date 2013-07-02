var Notifier = function (namespace) {
    this.namespace       = namespace
    this.hasNotification = true;

    if (window.webkitNotifications && window.Notification === undefined) {
        window.Notification = window.webkitNotifications;
    }

    if (window.Notification === undefined) {
        this.hasNotification = false;
    }
}

Notifier.prototype.init = function () {
    if (this.hasNotification) {
        return;
    }

    Notification.requestPermission();
}

Notifier.prototype.notify = function (title, options) {
    var n;

    if (this.hasNotification === false) {
        alert(title);
    }

    options = options || {};

    if (!options.notificationType) {
        options.notificationType = 'simple';
    }

    if (!options.tag) {
        options.tag = 'common';
    }

    if (!options.body) {
        options.body = title;
        title        = this.namespace;
    }

    n = new Notification(title, options);

    n.onclick = function() {
        this.close();
    };
};