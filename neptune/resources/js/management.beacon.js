var BeaconMessageManager;

BeaconMessageManager = function ($context) {
    this.context   = $context;
    this.loadedMap = {};

    setInterval($.proxy(this.updateAllTimestamps, this), 60000);
};

BeaconMessageManager.prototype.updateAllTimestamps = function () {
    var currentTimestamp = parseInt(new Date().getTime() / 1000, 10),
        previousTimestamp,
        previousType;

    this.context.children('li').each(function (i) {
        var $message  = $(this),
            type      = $message.attr('data-type'),
            timestamp = parseInt($message.attr('data-created'), 10),
            textTimestamp = whenAgo(timestamp, currentTimestamp);

        $message.attr(
            'data-when-ago',
            textTimestamp === previousTimestamp && previousType === type
                ? ''
                : textTimestamp
        );
        
        previousTimestamp = textTimestamp;
        previousType      = type;
    });
}

BeaconMessageManager.prototype.renderOne = function (message) {
    var $message = $(document.createElement('li'));

    $message
        .attr('data-id', message.id)
        .attr('data-type', message.type)
        .attr('data-created', message.created)
        .text(message.body);

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