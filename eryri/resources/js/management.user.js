UserRpcService = function (rpcUrl) {
    this.rpcUrl = rpcUrl;
    this.cachedResponse = null;
};

UserRpcService.prototype.query = function (query, successCallback) {
    $.ajax({
        url: this.rpcUrl,
        data: {
            query: query
        },
        success: function (response) {
            this.cachedResponse = response;

            successCallback(response.users);
        }
    });
};

UserList = function ($context) {
    this.context = $context;
};

UserList.prototype.add = function (user) {
    var block = $([
            '<li>',
                '<span class="avatar"><img src="', user.gravatar, '"/></span>',
                '<span class="name">', user.name, '</span>',
                '<span class="roles"></span>',
            '</li>'
        ].join('')),
        role;

    for (index in user.roles) {
        role = user.roles[index];

        block.find('.roles').append('<span class="role label">' + role + '</span>');
    }

    this.context.append(block);
}

UserList.prototype.reset = function () {
    this.context.empty();
}

$(document).ready(function () {
    var $queryIndicator = $('[data-user-query]'),
        $queryForm     = $('form.user.management.search'),
        $queryInput    = $queryForm.find('[name="query"]'),
        $userList      = $('ul.user.management.list'),
        previousQuery  = null,
        userRpcService = new UserRpcService(window.location.href),
        userList       = new UserList($userList);

    function handleQuery(e) {
        var query = $.trim($queryInput.val());

        e.preventDefault();

        $queryIndicator.attr('data-user-query', query);

        if (query.length === 0) {
            previousQuery = null;

            userList.reset();

            return;
        } else if (query === previousQuery) {
            return;
        }

        previousQuery = query;

        userRpcService.query(query, function (users) {
            userList.reset();

            for (index in users) {
                var user = users[index];

                userList.add(user);
            }
        });
    }

    $queryForm.on('submit', handleQuery);
    $queryInput.on('keyup', handleQuery);
});