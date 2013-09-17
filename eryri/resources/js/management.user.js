$(document).ready(function () {
    var $queryIndicator = $('[data-user-query]'),
        $queryForm     = $('form.user.management.search'),
        $queryInput    = $queryForm.find('[name="query"]'),
        $userList      = $('ul.user.management.list'),
        $userPane      = $('form.user.management.edit'),
        previousQuery  = null,
        userRpcService = new UserRpcService(window.location.href),
        userList       = new UserList($userList);

    function handleQueryOkResponse(users) {
        userList.reset();

        for (index in users) {
            var user = users[index];

            userList.add(user);
        }
    }

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

        userRpcService.query(query, handleQueryOkResponse);
    }

    $queryForm.on('submit', handleQuery);
    $queryInput.on('keyup', handleQuery);

    function handleUserRetrivalOk(user) {
        $userList
            .closest('.user-list')
            .removeClass('span12')
            .addClass('span3');

        $userPane
            .closest('.user-info')
            .removeClass('hidden');

        $userPane.find('h2').html(user.email.replace(/@/, ' at '));
        $userPane.find('img.avatar').attr('src', user.gravatar);
        $userPane.find('[name=name]').val(user.name);
        $userPane.find('[name=alias]').val(user.alias);
    }

    function showUserPane(e) {
        var $self = $(this),
            uid   = $self.attr('data-user-id');

        e.preventDefault();

        $self.closest('ul').children().removeClass('active');
        $self.addClass('active');

        userRpcService.get(uid, handleUserRetrivalOk);
    }

    $userList.on('click', 'li', showUserPane);
});