var BeaconMessageManager;

BeaconMessageManager = function ($context) {
    this.context   = $context;
    this.$list     = this.context.find('.messages');
    this.$count    = this.context.find('.count');
    this.loadedMap = {};

    setInterval($.proxy(this.updateAllTimestamps, this), 60000);

    this.context.on(
        'click',
        '.message .delete',
        $.proxy(this.onDelete, this)
    );
};

BeaconMessageManager.prototype.onDelete = function(e) {
    var self = this,
        $button = $(e.currentTarget),
        $container = $button.closest('.message');

    e.preventDefault();

    $.ajax({
        url: '/api/beacon/' + $container.attr('data-id'),
        type: 'delete',
        success: function (data) {
            self.load();
        }
    });
}

BeaconMessageManager.prototype.updateAllTimestamps = function () {
    var currentTimestamp = parseInt(new Date().getTime() / 1000, 10),
        previousTimestamp,
        previousType;

    this.$list.each(function (i) {
        previousTimestamp = null;
        previousType      = null;

        $(this).children('li').each(function (j) {
            var $message  = $(this),
                type      = $message.attr('data-type'),
                timestamp = parseInt($message.attr('data-created'), 10),
                textTimestamp = whenAgo(timestamp, currentTimestamp);

            $message.attr(
                'data-when-ago',
                textTimestamp === previousTimestamp && type === previousType
                    ? ''
                    : textTimestamp
            );

            previousTimestamp = textTimestamp;
            previousType      = type;
        });
    });
}

BeaconMessageManager.prototype.renderOne = function (message) {
    var $message = $(document.createElement('li')),
        $deleteButton = $(document.createElement('button'));

    $deleteButton
        .addClass('btn btn-danger delete')
        .html('&times;');

    $message
        .addClass('message')
        .attr('data-id', message.id)
        .attr('data-type', message.type)
        .attr('data-created', message.created)
        .text(message.body)
        .append($deleteButton);

    return $message;
};

BeaconMessageManager.prototype.load = function () {
    var self = this;

    this.$list.empty();

    $.ajax({
        url: '/api/beacon',
        success: function (data) {
            var i,
                message,
                unreadCount = data.meta.unread_count;

            self.$count.attr('data-count', unreadCount);
            self.$count.attr('title', unreadCount);
            self.$count.html(unreadCount > 10 ? '✻' : unreadCount);

            for (i in data.messages) {
                message = data.messages[i];

                self.loadedMap[message.id] = message;

                self.$list.append(self.renderOne(message));
            }

            self.updateAllTimestamps();
        }
    });
};

BeaconMessageManager.prototype.listen = function (caller) {
    var notifier  = new Notifier('Beacon'),
        $user = $('.user');
        bmm = new BeaconMessageManager($('.beacon')),
        ws = new WebSocket(wsUrl);

    ws.onopen = function (event) {
        $user.addClass('online');
        $user.removeClass('offline');
    };

    ws.onmessage = function (event) {
        var data = JSON.parse(event.data);

        data.message = JSON.parse(data.message);

        bmm.load();
        notifier.notify(data.message.body);
    };

    ws.onclose = function (event) {
        $user.removeClass('online');
        $user.addClass('offline');
    };

    // Initialization
    bmm.load();

    caller.beacon = bmm;
};