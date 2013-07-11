var BeaconMessageManager;

BeaconMessageManager = function ($context) {
    this.context   = $context;
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

    this.context.each(function (i) {
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

    this.context.empty();

    $.ajax({
        url: '/api/beacon',
        success: function (data) {
            var i, message;

            for (i in data.messages) {
                message = data.messages[i];

                self.loadedMap[message.id] = message;

                self.context.append(self.renderOne(message));
            }

            self.updateAllTimestamps();
        }
    });
};

$(document).ready(function () {
    var notifier  = new Notifier('Beacon'),
        $user = $('.user');
        bmm = new BeaconMessageManager($('.beacon.messages')),
        ws = new WebSocket(wsUrl);

    ws.onopen = function (event) {
        $user.addClass('online');
    };

    ws.onmessage = function (event) {
        var data = JSON.parse(event.data);

        data.message = JSON.parse(data.message);

        bmm.load();
        notifier.notify(data.message.body);
    };

    ws.onclose = function (event) {
        $user.removeClass('online');
    };

    // Initialization
    bmm.load();
});