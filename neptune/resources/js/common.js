var Notifier;

function whenAgo(time, currentTime) {
    var diffInSecond = currentTime - time,
        diffInMinute = Math.floor(diffInSecond / 60),
        diffInHour   = Math.floor(diffInSecond / 60 / 60),
        diffInDay    = Math.floor(diffInSecond / 60 / 60 / 24);
    currentTime = currentTime || parseInt(new Date().getTime() / 1000, 10);

    switch (true) {
    case diffInDay > 0:
        return diffInDay + 'd';
    case diffInHour > 0:
        return diffInHour + 'h';
    case diffInMinute > 0:
        return diffInMinute + 'm';
    default:
        return 'now';
    }
}

Notifier = function (namespace) {
    var $body = $('body'),
        modalTemplate = [
            '<div class="modal hide wizard notifier-setup">',
            '<div class="modal-header"><h3>Notification Settings</h3></div>',
            '<div class="modal-body">',
            '<p>Do you want to use the desktop notification?</p>',
            '</div>',
            '<div class="modal-footer">',
            '<button type="button" class="btn btn-primary notification-activator" data-type="desktop">OS Notification</button>',
            '<button type="button" class="btn notification-activator" data-type="no">No</button>',
            '</div>',
            '</div>'
        ].join('');

    this.namespace       = namespace;
    this.hasNotification = false;
    this.dialog          = null;
    this.activators      = null;

    if (window.webkitNotifications && window.Notification === undefined) {
        window.Notification = window.webkitNotifications;
    }

    if (window.Notification !== undefined) {
        this.hasNotification = true;

        $body.append(modalTemplate);
    }

    localStorage.notification = this.hasNotification && localStorage.notification && localStorage.notification.length > 0
        ? localStorage.notification
        : '';

    if (localStorage.notification.length === 0) {
        this.dialog = $body.find('.wizard.notifier-setup');
        this.dialog.modal('show');
    }

    this.activators = $body.find('.notification-activator');

    this.activators.on('click', $.proxy(this.activateNotification, this));
};

Notifier.prototype.activateNotification = function (e) {
    var $target = $(e.currentTarget),
        type = $target.attr('data-type');

    e.preventDefault();

    if (!this.hasNotification || $target.attr('disabled')) {
        return;
    }

    localStorage.notification = type;

    this.dialog.modal('hide');
    this.activators.attr('disabled', true);

    if (type === 'desktop') {
        return Notification.requestPermission();
    }
};

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