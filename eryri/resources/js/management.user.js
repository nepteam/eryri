$(document).ready(function () {
    var $queryIndicator = $('[data-user-query]'),
        $queryForm  = $('form.user.management.search'),
        $queryInput = $queryForm.find('[name="query"]'),
        $userList = $('ul.user.management.list'),
        $userPane = $('.user.management.pane'),
        userRpcService = new UserRpcService(window.location.href),
        userList = new UserList($userList),
        lastQueryKeyPress = null,
        previousQuery  = null
    ;

    function handleQueryOkResponse(response) {
        var users = response.users,
            count = users.length,
            user,
            index;

        if (previousQuery !== response.query) {
            return;
        }

        userList.reset();

        for (index in users) {
            user = users[index];

            user.gravatar = null;

            userList.add(user);
        }

        NProgress.done();
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

        lastQueryKeyPress = new Date();

        setTimeout(function () {
            now = new Date();

            if (now - lastQueryKeyPress < 400) {
                return;
            }

            previousQuery = query;

            userRpcService.query(query, handleQueryOkResponse);
        }, 400);
    }

    function handleUserRetrivalOk(user) {
        var email = user.email.replace(/@/, ' at ');

        $userPane.attr('data-id', user.id);

        $userPane.removeClass('disabled');

        $userPane.find('h2').html(user.alias + ' <small>' + email + '</small>');
        $userPane.find('img.avatar').attr('src', user.gravatar + '?s=100');
        $userPane.find('[name=name]').val(user.name);

        NProgress.done();
    }

    function showUserPane(e) {
        var $self = $(this),
            uid   = $self.attr('data-user-id');

        e.preventDefault();
        NProgress.start();

        userRpcService.get(uid, handleUserRetrivalOk);
    }

    function handleUserPaneUpdated(e) {
        var $form = $(this),
            uid   = $form.closest('article').attr('data-id'),
            data  = {};

        e.preventDefault();
        NProgress.start();

        $form.find('input').each(function (index) {
            var $input = $(this),
                value  = $.trim($input.val())
            ;

            data[$input.attr('name')] = value.length > 0
                ? value
                : null
            ;
        });

        userRpcService.put(uid, data, handleUserRetrivalOk);
    }

    function onCloseButtonClickHideUserPane(e) {
        e.preventDefault();
        $userPane.addClass('disabled');
    }

    $queryForm.on('submit', handleQuery);
    $queryInput.on('keyup', handleQuery);
    $userList.on('click', 'li', showUserPane);
    $userPane.on('click', '.close', onCloseButtonClickHideUserPane);
    $userPane.on('submit', 'form', handleUserPaneUpdated);
});