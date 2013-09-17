UserList = function ($context) {
    this.context = $context;
};

UserList.prototype.add = function (user) {
    var $block = $([
            '<li>',
                '<span class="avatar"><img src="', user.gravatar, '"/></span>',
                '<span class="name">', user.name, '</span>',
                '<span class="roles"></span>',
            '</li>'
        ].join('')),
        role;

    $block.attr('data-user-id', user.id);
    $block.find('.avatar img').attr('src', user.gravatar);
    $block.find('.name').text(user.name);

    for (index in user.roles) {
        role = user.roles[index];

        $block.find('.roles').append('<span class="role label label-inverse">' + role + '</span>');
    }

    this.context.append($block);
}

UserList.prototype.reset = function () {
    this.context.empty();
}