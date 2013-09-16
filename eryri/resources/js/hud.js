UserCard = function () {
    this.context = $('.hud.user');

    this.context.on('click', $.proxy(this.onExpand, this));
    this.context.find('.hide-button').on('click', $.proxy(this.onHide, this));

    this.adjustMessageBox();

    $(window).on('resize', $.proxy(this.adjustMessageBox, this));

    BeaconMessageManager.prototype.listen(this);
};

UserCard.prototype.fixedHeightComponents = [
    '.avatar',
    '.name',
    '.mode'
];

UserCard.prototype.adjustMessageBox = function () {
    var i,
        offsetTop = 0;

    for (i in this.fixedHeightComponents) {
        offsetTop += this.context.children(this.fixedHeightComponents[i]).outerHeight();
    }

    this.context
        .find('.beacon .messages')
        .css(
            'max-height',
            $(window).innerHeight()
            - parseInt(this.context.css('top'), 10) * 2
            - offsetTop
        );
};

UserCard.prototype.onExpand = function (e) {
    var self = this;
    
    this.context.removeClass('stand-by');
    setTimeout($.proxy(this.adjustMessageBox, this), 500);

    $.ajax({
        url: '/beacon',
        type: 'put',
        success: function (data) {
            self.beacon.load();
        }
    });
};

UserCard.prototype.onHide = function (e) {
    e.preventDefault();
    e.stopPropagation();
    this.context.addClass('stand-by');
};